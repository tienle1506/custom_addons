# -*- coding:utf-8 -*-
import base64
import tempfile
import xlrd
import xlsxwriter
import time
import calendar
import json
from odoo.addons import decimal_precision as dp
from io import BytesIO
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import Warning, ValidationError


def get_weekend_days(start_date, end_date):
    weekend_days = []
    current_date = start_date
    total_days = 0

    while current_date <= end_date:
        if current_date.weekday() in [5, 6]:
            weekend_days.append(current_date)
        current_date += timedelta(days=1)
        total_days += 1

    return weekend_days, total_days

class DATNHrChamCong(models.Model):
    _name = 'datn.hr.chamcong'
    _inherit = ['mail.thread']
    _description = u'Chấm công theo tháng'
    _order = "date_from DESC"

    def _default_date_from(self):
        return datetime.today().strftime('%Y-%m-01')

    def _default_date_to(self):
        return (datetime.today() + relativedelta(months=+1, day=1, days=-1)).strftime('%Y-%m-%d')


    name = fields.Char(string=u'Bảng chấm công tháng', size=128, track_visibility='always', )
    date_from = fields.Date(u'Từ ngày', required=True, default=_default_date_from,)
    date_to = fields.Date(u'Đến ngày', required=True, default=_default_date_to, track_visibility='always', )
    department_id = fields.Many2one('hr.department',ondelete='cascade', string=u'Đơn vị/ Phòng ban', required=True)
    item_ids = fields.One2many('datn.hr.chamcong.line', 'chamcong_id')
    state = fields.Selection([('draft', u'Soạn thảo'), ('confirmed', u'Xác nhận')],
                             string=u'Trạng thái', default='draft', track_visibility='always')
    # Lưu dữ liệu các bản ghi chấm công khi onchange phục vụ chức năng export
    backup = fields.Text(string="")
    # Import
    datn_file = fields.Binary(u'Đường dẫn tập tin', filters="*.xls,*.xlsx")
    file_name = fields.Char(u'Tên tệp tin')
    is_import = fields.Boolean(u'Import dữ liệu')

    is_show_ngay29 = fields.Boolean(string=u"Có ngày 29", compute='_compute_date', store=True)
    is_show_ngay30 = fields.Boolean(string=u"Có ngày 30", compute='_compute_date', store=True)
    is_show_ngay31 = fields.Boolean(string=u"Có ngày 31", compute='_compute_date', store=True)

    @api.onchange('date_from', 'department_id')
    def onchange_name(self):
        name = 'Bảng chấm công tháng %s năm %s Đơn vị/ phòng ban %s' % (
            str(self.date_from.month), str(self.date_from.year), self.department_id.name)
        self.name = name
        self.item_ids.unlink()
    @api.onchange('date_from')
    def onchange_date_from(self):
        if self.date_from:
            date_from_str = self.date_from.strftime('%Y-%m-%d')
            year, month, _ = map(int, date_from_str.split('-'))
            _, last_day = calendar.monthrange(year, month)
            date_to = f'{year}-{month:02d}-{last_day:02d}'
            date_from = datetime.strptime(str(self.date_from), '%Y-%m-%d').replace(day=1)
            self.date_to = date_to
            self.date_from = date_from
    @api.depends('date_from', 'date_to')
    def _compute_date(self):
        if not self.date_from and not self.date_to:
            return
        else:
            date = self.date_from
            self.is_show_ngay29 = False
            self.is_show_ngay30 = False
            self.is_show_ngay31 = False
            # Lấy số ngày trong tháng
            _, days_in_month = calendar.monthrange(date.year, date.month)
            if days_in_month == 29:
                self.is_show_ngay29 = True
            elif days_in_month == 30:
                self.is_show_ngay29 = True
                self.is_show_ngay30 = True
            elif days_in_month == 31:
                self.is_show_ngay29 = True
                self.is_show_ngay30 = True
                self.is_show_ngay31 = True


    @api.constrains('file_name')
    def _check_filename(self):
        if self.datn_file:
            if not self.file_name:
                raise ValidationError(_(u"Không có tập tin!"))
            else:
                # Check the file's extension
                tmp = self.file_name.split('.')
                ext = tmp[len(tmp) - 1]
                if ext != 'xls' and ext != 'xlsx':
                    raise ValidationError(_(u"Tệp tin tải lên phải là định dạng file excel. Vui lòng xem lại."))

    def action_loaddata(self):
        self.item_ids.unlink()

        if self.department_id:
            cr = self.env.cr
            SQL = ''
            SQL += '''SELECT ckl.* FROM datn_hr_checkin_checkout_line ckl
                    LEFT JOIN datn_hr_checkin_checkout ck ON ck.id = ckl.checkin_checkout_id
                    LEFT JOIN hr_employee emp ON emp.id = ckl.employee_id
                    WHERE emp.department_id = ANY(ARRAY(SELECT child_ids FROM child_department WHERE parent_id = %s)) AND ck.date_from = '%s'
                    AND  ck.date_to = '%s' AND ck.state = 'confirmed' AND ckl.state='approved'
                    AND ckl.employee_id not in (SELECT ccl.employee_id FROM datn_hr_chamcong cc INNER JOIN datn_hr_chamcong_line ccl ON ccl.chamcong_id = cc.id 
            where date_from >= '%s' and date_to <= '%s')
                    ORDER BY ckl.employee_id
            '''%(self.department_id.id, self.date_from, self.date_to, self.date_from, self.date_to)
            cr.execute(SQL)
            employees = cr.dictfetchall()
            SQL = ''
            SQL += '''SELECT ckl.* FROM datn_tangca ckl WHERE ckl.department_id = ANY
                      (ARRAY(SELECT child_ids FROM child_department WHERE parent_id = %s))
                       AND ckl.date_from >= '%s' AND  ckl.date_to <= '%s' AND ckl.state = 'approved'
                       AND ckl.employee_id not in (SELECT ccl.employee_id FROM datn_hr_chamcong cc INNER JOIN datn_hr_chamcong_line ccl ON ccl.chamcong_id = cc.id 
                        where date_from >= '%s' and date_to <= '%s')''' % (self.department_id.id, self.date_from, self.date_to,self.date_from,self.date_to)
            cr.execute(SQL)
            tangca = cr.dictfetchall()
            if employees:
                for i in range(0, len(employees)):
                    ngay = employees[i].get('day').day
                    ngayx = 'ngay%s'%(ngay)
                    if employees[i].get('timeofday') and float(employees[i].get('timeofday')) >= 8:
                        time = 1
                    elif employees[i].get('timeofday') and float(employees[i].get('timeofday')) < 8:
                        time = round(float(employees[i].get('timeofday')) / 8, 2)
                    else:
                        time = 0
                    cr = self.env.cr
                    filtered_employees = self.item_ids.employee_id.filtered(lambda emp: emp.id == employees[i].get('employee_id'))
                    if not filtered_employees:
                        lines = []
                        lines.append((0, 0, {
                            'employee_id': employees[i].get('employee_id'),
                            ngayx: time
                        }))
                        self.item_ids = (lines)
                    else:
                        for item in self.item_ids:
                            if item['employee_id'].id == employees[i].get('employee_id'):
                                item[ngayx] = time

            if tangca:
                tangca = tangca
                for i in range(0, len(tangca)):
                    delta = tangca[i].get('date_to') - tangca[i].get('date_from')
                    num_days = delta.days
                    for j in range(0,num_days+1):
                        ngay = (self.date_from + timedelta(days=j)).day
                        ngayx = 'ngay%s' % (ngay)
                        filtered_employees = self.item_ids.employee_id.filtered(lambda emp: emp.id == tangca[i].get('employee_id'))
                        if not filtered_employees:
                            lines = []
                            lines.append((0, 0, {
                                'employee_id': tangca[i].get('employee_id'),
                                ngayx: round(float(tangca[i].get('so_gio_tang_ca'))/8,2)
                            }))
                            self.item_ids = (lines)
                        else:
                            for item in self.item_ids:
                                if item['employee_id'].id == tangca[i].get('employee_id'):
                                    item[ngayx] = item[ngayx] + round(float(tangca[i].get('so_gio_tang_ca'))/8,2)

            #Đồng bộ dữ liệu quan site công thực tê
            weekend_days, total_days = get_weekend_days(self.date_from, self.date_to)

            cong_chuan = total_days - len(weekend_days) if weekend_days else 0

            list_ccs = self.env['datn.hr.chamcong.line'].search([('chamcong_id.date_from', '>=', self.date_from), ('chamcong_id.date_to', '>=', self.date_to),
                                                      ('chamcong_id.id', '=', self.id)])

            cc_id = self.id if self.id else 0
            SQL = ''
            SQL += ''' SELECT emp.* FROM hr_employee emp WHERE emp.department_id = ANY(ARRAY(SELECT child_ids FROM child_department WHERE parent_id = %s)) AND emp.work_start_date <= '%s'
                                                        AND emp.id not in (SELECT ccl.employee_id FROM datn_hr_chamcong cc INNER JOIN datn_hr_chamcong_line ccl ON ccl.chamcong_id = cc.id 
                                                        where date_from >= '%s' and date_to <= '%s' and cc.id != %s) '''%(self.department_id.id,self.date_to, self.date_from, self.date_to, cc_id)
            cr.execute(SQL)
            employees = cr.dictfetchall()
            self.env['datn.congthucte'].sudo().search([('chamcong_id', '=', self.id)]).unlink()
            new_record = self.env['datn.congthucte'].sudo().create({
                'department_id': self.department_id.id,
                'name': 'Bảng công thực tế đơn vị/ phòng ban %s từ ngày %s đến ngày %s'%(self.department_id.name, self.date_from, self.date_to),
                'date_from': self.date_from,
                'date_to': self.date_to,
                'chamcong_id': self.id,
                'state': 'draft'
            })

            if employees:
                for i in range(0, len(employees)):
                    cong_thuc_te = 0
                    for item in list_ccs:
                        if item.employee_id.id == employees[i].get('id'):
                            cong_thuc_te = 0
                            for k in range(1, 32):
                                ngayx = 'ngay%s'%(k)
                                cong_thuc_te += round(float(getattr(item, ngayx)),2) if getattr(item, ngayx) else 0
                    dk_nghis = self.env['datn.dangkynghi'].search([('date_from', '>=', self.date_from),
                                                        ('date_to', '<=', self.date_to),
                                                        ('employee_id', '=', employees[i].get('id')),
                                                                   ('state', '=', 'approved')])
                    cong_phep = 0
                    cong_khong_luong = 0
                    cong_co_luong = 0
                    #Công lễ tết - > cong_co_luong
                    SQL = ''
                    SQL += ''' SELECT ltl.* from datn_hrm_le_tet lt INNER JOIN datn_hrm_le_tet_line ltl ON ltl.le_tet_id = lt.id
                                WHERE lt.date_from >= '%s' AND lt.date_to <= '%s' AND ltl.employee_id = %s AND lt.state = 'confirmed' '''%(self.date_from,self.date_to,employees[i].get('id'))
                    cr.execute(SQL)
                    le_tets = cr.dictfetchall()
                    if le_tets:
                        for h in range(0, len(le_tets)):
                            delta = le_tets[h].get('date_to') - le_tets[h].get('date_from')
                            num_days = delta.days
                            cong_co_luong += num_days + 1
                    if dk_nghis:
                        for h in range(0, len(dk_nghis)):
                            if dk_nghis[h].loai_nghi.loai_nghi == 'nghiphep':
                                cong_phep += round(dk_nghis[h].so_ngay_nghi, 2)
                            elif dk_nghis[h].loai_nghi.loai_nghi == 'nghicoluong':
                                cong_co_luong += round(dk_nghis[h].so_ngay_nghi, 2)
                            elif dk_nghis[h].loai_nghi.loai_nghi == 'khongluong':
                                cong_khong_luong += round(dk_nghis[h].so_ngay_nghi, 2)
                    #Công tăng ca
                    tang_cas = self.env['datn.tangca'].search([('date_from', '>=', self.date_from),
                                                                   ('date_to', '<=', self.date_to),
                                                                   ('employee_id', '=', employees[i].get('id')),
                                                                   ('state', '=', 'approved')])
                    cong_tang_ca = 0
                    if tang_cas:
                        for h in range(0, len(tang_cas)):
                            delta = tang_cas[h].date_to - tang_cas[h].date_from
                            num_days = delta.days
                            cong_tang_ca += round((float(tang_cas[h].so_gio_tang_ca)* float(num_days + 1)) / 8, 2)
                    #Nghỉ không lý do
                    SQL = ''
                    SQL += ''' select count(*) as nghi_khong_ly_do from datn_hr_checkin_checkout_line where day BETWEEN '%s' AND '%s' AND employee_id = %s'''%(self.date_from,self.date_to,employees[i].get('id'))
                    cr.execute(SQL)
                    nghi_khong_ly_do = cr.dictfetchall()
                    if nghi_khong_ly_do:
                        nghi_khong_ly_do = cong_chuan - nghi_khong_ly_do[0].get('nghi_khong_ly_do')

                    self.env['datn.congthucte.line'].sudo().create(
                        {
                            'congthucte_id': new_record.id,
                            'employee_id': employees[i].get('id'),
                            'date_from': self.date_from,
                            'date_to': self.date_to,
                            'cong_chuan': cong_chuan,
                            'cong_thuc_te': cong_thuc_te,
                            'cong_phep': cong_phep,
                            'cong_co_luong': cong_co_luong,
                            'cong_khong_luong': cong_khong_luong,
                            'cong_tang_ca': cong_tang_ca,
                            'cong_nghi_khong_ly_do': nghi_khong_ly_do,
                            'department_id': employees[i].get('department_id')
                        }
                    )

    def action_draft(self):
        self.env['datn.congthucte'].search([('chamcong_id', '=', self.id)]).write({'state': 'draft'})
        self.state = 'draft'
    def action_confirmed(self):
        self.env['datn.congthucte'].search([('chamcong_id', '=', self.id)]).write({'state': 'confirmed'})
        self.state = 'confirmed'

    def unlink(self):
        # Kiểm tra điều kiện trước khi thực hiện unlink
        can_unlink = True
        for record in self:
            if record.state != 'draft':
                can_unlink = False
                # Xử lý khi điều kiện không đúng
                # ví dụ:
                raise ValidationError("Không thể xoá bản ghi do bản ghi đã được ghi nhận.")

        if can_unlink:
            for record in self:
                self.env['datn.congthucte'].search([('chamcong_id', '=', record.id)]).unlink()
            # Thực hiện unlink chỉ khi điều kiện đúng
            return super(DATNHrChamCong, self).unlink()
class DATNHrChamCongLine(models.Model):
    _name = 'datn.hr.chamcong.line'
    _description = u'Chấm công nhân sự'
    _rec_name = 'employee_id'

    def _get_decimal_precision(name_precision):
        # TODO: defaul config: Cấu trúc Cơ sở dữ liệu -> Độ chính xác thập phân
        result = dp.get_precision(name_precision)
        # Get user dang nhap => department id
        # def change_digit(cr):
        #     user_depart = openerp.registry(cr.dbname)['res.users']
        #     res = user_depart.department_id_get(cr, SUPERUSER_ID, name_precision)
        #     print res
        #     return (16, res)
        # if department vp = cau hinh return x1 else default
        return result

    employee_id = fields.Many2one('hr.employee', string=u'Nhân sự', ondelete='cascade')
    chamcong_id = fields.Many2one('datn.hr.chamcong', string=u'Bảng chấm công', ondelete='cascade', required=True)
    # playslip_id = fields.Many2one('hr.payslip', string='Payslip', ondelete='cascade')
    ngay_cong = fields.Float(string=u'Ngày công', digits=_get_decimal_precision("Timesheets"))

    # end
    department_id = fields.Many2one('hr.department',ondelete='cascade', string=u'Đơn vị/ phòng ban')

    # Ngay cong trong thang
    ngay1 = fields.Float(string=u"01", range=True)
    ngay2 = fields.Float(string=u"02", range=True)
    ngay3 = fields.Float(string=u"03", range=True)
    ngay4 = fields.Float(string=u"04", range=True)
    ngay5 = fields.Float(string=u"05", range=True)
    ngay6 = fields.Float(string=u"06", range=True)
    ngay7 = fields.Float(string=u"07", range=True)
    ngay8 = fields.Float(string=u"08", range=True)
    ngay9 = fields.Float(string=u"09", range=True)
    ngay10 = fields.Float(string=u"10", range=True)
    ngay11 = fields.Float(string=u"11", range=True)
    ngay12 = fields.Float(string=u"12", range=True)
    ngay13 = fields.Float(string=u"13", range=True)
    ngay14 = fields.Float(string=u"14", range=True)
    ngay15 = fields.Float(string=u"15", range=True)
    ngay16 = fields.Float(string=u"16", range=True)
    ngay17 = fields.Float(string=u"17", range=True)
    ngay18 = fields.Float(string=u"18", range=True)
    ngay19 = fields.Float(string=u"19", range=True)
    ngay20 = fields.Float(string=u"20", range=True)
    ngay21 = fields.Float(string=u"21", range=True)
    ngay22 = fields.Float(string=u"22", range=True)
    ngay23 = fields.Float(string=u"23", range=True)
    ngay24 = fields.Float(string=u"24", range=True)
    ngay25 = fields.Float(string=u"25", range=True)
    ngay26 = fields.Float(string=u"26", range=True)
    ngay27 = fields.Float(string=u"27", range=True)
    ngay28 = fields.Float(string=u"28", range=True)
    ngay29 = fields.Float(string=u"29", range=True)
    ngay30 = fields.Float(string=u"30", range=True)
    ngay31 = fields.Float(string=u"31", range=True)