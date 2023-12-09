# -*- coding:utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import Warning, ValidationError
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

def get_weekend_days(start_date, end_date):
    weekend_days = []
    current_date = start_date

    while current_date <= end_date:
        if current_date.weekday() in [5, 6]:
            weekend_days.append(current_date)
        current_date += timedelta(days=1)

    return weekend_days
class DATNDangKyNghi(models.Model):
    _name = "datn.dangkynghi"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = u'Đăng ký nghỉ phép'
    _order = "date_from DESC, date_to DESC"

    name = fields.Char(string='Name', required=True, default='')
    nguoi_duyet = fields.Many2many('hr.employee', 'employee_duyet_nghi_them_rel', 'nghi_id', 'employee_id', string="Người duyệt")
    employee_id = fields.Many2one('hr.employee', string="Nhân viên", ondelete='cascade', default=lambda self: self._default_employee())
    department_id = fields.Many2one('hr.department', string="Đơn vị/ phòng ban", ondelete='cascade', related='employee_id.department_id', store=True)
    date_from = fields.Date(u'Từ ngày', widget='date', format='%Y-%m-%d')
    date_to = fields.Date(u'Đến ngày', widget='date', format='%Y-%m-%d', attrs={'readonly': ['|', ('state', '!=', 'draft'),('loai_nghi.loai_nghi', '=', 'nghicoluong')]})
    state = fields.Selection([('draft', u'Gửi phê duyệt'), ('confirmed', u'Chờ phê duệt'), ('approved', u'Phê duyệt'), ('refused', u'Từ chối')],
                             string=u'Trạng thái', default='draft', track_visibility='always')
    ly_do = fields.Text(u"Lý do")
    so_ngay_nghi = fields.Float(u"Số ngày nghỉ", compute='_compute_so_ngay_nghi', store=True)
    loai_nghi = fields.Many2one(u"datn.loai.nghi", 'Loại nghỉ')
    so_ngay_da_nghi = fields.Float(u"Số ngày phép đã nghỉ", related='employee_id.so_ngay_da_nghi', store=True)
    so_ngay_duoc_phan_bo = fields.Float(u"Số ngày phép được phân bổ", related='employee_id.so_ngay_duoc_phan_bo', store=True)
    create_date = fields.Date(u'Từ ngày', widget='date', format='%Y-%m-%d', default=fields.Date.today)
    @api.depends('loai_nghi', 'date_from', 'date_to')
    def _compute_so_ngay_nghi(self):
        mang_cuoi_tuan = get_weekend_days(self.date_from, self.date_to)
        if mang_cuoi_tuan:
            ngay_ct = len(mang_cuoi_tuan)
        if self.loai_nghi and self.date_from and self.date_to:
            date_from = fields.Date.from_string(self.date_from)
            date_to = fields.Date.from_string(self.date_to)
            delta = date_to - date_from
            num_days = delta.days + 1
            self.so_ngay_nghi = self.loai_nghi.ngay_ap_dung * num_days - ngay_ct

    @api.constrains('date_from', 'date_to')
    def _check_date_hientai(self):
        current_date = fields.Date.today()
        for record in self:
            if record.date_from and record.date_to:
                if record.date_from < current_date:
                    raise ValidationError(_(u"Bạn không thể tạo nghỉ phép cho các tháng trước đó."))
                if record.date_from.year > record.date_from.year and record.loai_nghi == 'nghiphep':
                    raise ValidationError(_(u"Bạn không thể tạo nghỉ phép cho các năm sau."))
        if self.id:
            SQL = ''
            SQL += '''SELECT * FROM datn_dangkynghi WHERE id != %s and employee_id = %s AND ((date_from BETWEEN '%s' AND '%s') 
            OR (date_to BETWEEN '%s' AND '%s')) '''%(self.id, self.employee_id.id, self.date_from, self.date_to,self.date_from, self.date_to)
            self.env.cr.execute(SQL)
            employees = self.env.cr.dictfetchall()
        else:
            SQL = ''
            SQL += '''SELECT * FROM datn_dangkynghi WHERE employee_id = %s AND ((date_from BETWEEN '%s' AND '%s') 
                        OR (date_to BETWEEN '%s' AND '%s')) ''' % (
            self.employee_id.id, self.date_from, self.date_to, self.date_from, self.date_to)
            self.env.cr.execute(SQL)
            employees = self.env.cr.dictfetchall()
        if employees:
            raise ValidationError("Ngày xin nghỉ của bạn đang tạo có một ngày khác đã được tạo, năm trong khoảng này")

    @api.onchange('date_from', 'date_to')
    def _check_date_from_To(self):
        for record in self:
            if record.date_from and record.date_to:
                if record.date_from > record.date_to:
                    raise ValidationError(_(u"Đến ngày phải nhỏ hơn từ ngày."))
    def read(self, fields=None, load='_classic_read'):
        self.check_access_rule('read')
        return super(DATNDangKyNghi, self).read(fields, load=load)

    def search(self, args, offset=0, limit=None, order=None, count=False):
        domain = []
        return super(DATNDangKyNghi, self).search(domain + args, offset, limit, order, count=count)

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        emp_domain = self.check_employee_view()
        return super(DATNDangKyNghi, self)._name_search(name, args=args + emp_domain, operator=operator,
                                                                  limit=limit)


    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        emp_domain = self.check_employee_view()
        return super(DATNDangKyNghi, self).search_read(domain=domain + emp_domain, fields=fields,
                                                                  offset=offset, limit=limit, order=order)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        emp_domain = self.check_employee_view()
        return super(DATNDangKyNghi, self).read_group(domain + emp_domain, fields, groupby, offset=offset,
                                                                 limit=limit, orderby=orderby, lazy=lazy)
    def check_employee_view(self):
        context = self.env.context or {}
        emp_domain = []
        user = self.env.user
        employee_id = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
        if context.get('view_from_action', False):
            emp_domain = [('employee_id', '=', employee_id.id)]
        if context.get('view_from_action_phe_duyet', False):
            emp_domain = [('nguoi_duyet', '=', employee_id.id), ('state', '!=', 'draft')]
        return emp_domain
    @api.model
    def _default_employee(self):
        user = self.env.user
        employee = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
        return employee
    @api.constrains('so_ngay_nghi')
    def _check_date_duong(self):
        if self.loai_nghi.ngay_toi_da and self.loai_nghi.ngay_toi_da > 0 and self.so_ngay_nghi > self.loai_nghi.ngay_toi_da:
            vai = 'Không đăng ký vượt quá ngày nghỉ tối đa của loại nghỉ đã lựa chọn (%s ngày)' % (
                self.loai_nghi.ngay_toi_da)
            raise ValidationError(vai)
        if self.so_ngay_nghi < 0:
            raise ValidationError(_(u"Số ngày nghỉ phải lớn hơn 0, yêu cầu nhập lại."))

    def action_draft(self):
        self.state = 'draft'
    def action_send_approve(self):
        if self.loai_nghi.loai_nghi == 'nghiphep':
            if self.so_ngay_duoc_phan_bo - self.so_ngay_da_nghi - self.so_ngay_nghi < 0:
                raise ValidationError('Số ngày nghỉ phép không thể vượt quá ngày phép còn lại.')
        nguoi_duyet = []
        for emp in self.nguoi_duyet:
            if emp.personal_email:
                nguoi_duyet.append(emp.personal_email.strip())
        header = '''Thông báo phê duyệt đơn đăng ký nghỉ của %s'''%(self.employee_id.name)
        content =u'Nhân viên %s tạo đơn xin nghỉ \nLý do: %s \nNghỉ số ngày:%s \nLoại nghỉ: %s \nTừ ngày: %s - đến ngày: %s \nTrang web: http://localhost:8088/web'%(str(self.employee_id.name), str(self.ly_do), str(self.so_ngay_nghi), str(self.loai_nghi.name), self.date_from.strftime('%d/%m/%Y'), self.date_to.strftime('%d/%m/%Y'))
        if nguoi_duyet and len(nguoi_duyet) > 0:
            self.env['my.mail.sender'].send_mail_to_customer(nguoi_duyet, header, content)
        self.state = 'confirmed'

    def action_refuse(self):
        delta = self.date_to - self.date_from
        num_days = delta.days
        for i in range(0, num_days + 1):
            day = self.date_from + timedelta(days=i)
            mang_cuoi_tuan = get_weekend_days(self.date_from, self.date_to)
            if day not in mang_cuoi_tuan:
                employee_checkin = self.env['datn.hr.checkin.checkout.line'].search(
                    [('employee_id', '=', self.employee_id.id), ('day', '=', day)]).id
                if employee_checkin:
                    SQL = ''
                    SQL += '''DELETE FROM datn_hr_checkin_checkout_line WHERE id = %s''' % (employee_checkin)
                    self.env.cr.execute(SQL)
        nghi = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
        self.so_ngay_da_nghi = nghi.so_ngay_da_nghi - self.so_ngay_nghi
        nghi.write(
            {
                'so_ngay_da_nghi': nghi.so_ngay_da_nghi - self.so_ngay_nghi
            }
        )
        self.state = 'refused'

    def action_approve(self):
        cr = self.env.cr
        # Thêm vào check in check out của nhân viên
        date_format = '%Y-%m-%d'
        # Tính số ngày giữa hai ngày
        delta = self.date_to - self.date_from
        num_days = delta.days
        formatted_date = datetime(self.date_from.year, self.date_to.month, 1).date()
        SQL1 = ''
        SQL1 += '''SELECT ck.id FROM datn_hr_checkin_checkout_line ckl
                                        LEFT JOIN datn_hr_checkin_checkout ck ON ck.id = ckl.checkin_checkout_id
                                        WHERE ckl.employee_id = %s AND to_char(ck.date_from, 'mmYYYY') = to_char('%s'::date, 'mmYYYY')
                                        LIMIT 1
                            ''' % (self.employee_id.id, self.date_from)
        self.env.cr.execute(SQL1)
        results = self.env.cr.dictfetchone()
        if not results:
            SQL = ''
            SQL += '''SELECT datn_hr_checkin_checkout.id FROM datn_hr_checkin_checkout
                                            LEFT JOIN hr_department ON hr_department.id = datn_hr_checkin_checkout.department_id
                                            WHERE date_from = '%s' AND department_id in (select unnest(get_list_parent_department(%s)))
                                            ORDER BY hr_department.department_level
                                            LIMIT 1
                                ''' % (formatted_date, self.department_id.id)
            self.env.cr.execute(SQL)
            results = self.env.cr.dictfetchone()
        # Lấy giá trị đầu tiên thoả mãn
        if results:
            first_result = results.get('id')
        else:
            SQL3 = ''
            SQL3 += '''SELECT id,name from hr_department WHERE department_level = 1 AND id in (select unnest(get_list_parent_department(%s)))''' % (self.department_id.id)
            self.env.cr.execute(SQL3)
            results = self.env.cr.dictfetchone()
            first_result = results.get('id')
            name_dp = results.get('name')
            # Lấy ngày đầu tiên của tháng
            first_day = self.date_from.replace(day=1)
            # Lấy ngày cuối cùng của tháng
            next_month = (datetime.strptime(str(self.date_from), "%Y-%m-%d") + relativedelta(months=1)).replace(day=1)
            last_day = (next_month - timedelta(days=1)).date()
            name = 'Bảng thanh check-in check-out của %s từ ngày %s đến ngày %s' % (name_dp,first_day, last_day)
            SQL4 = ''
            SQL4 += '''INSERT INTO datn_hr_checkin_checkout (department_id, date_from, date_to, name, state)
                                                           VALUES(%s,'%s','%s', '%s', 'draft')''' % (
            first_result, first_day, last_day, name)
            self.env.cr.execute(SQL4)

            SQL5 = ''
            SQL5 += '''SELECT id from datn_hr_checkin_checkout WHERE department_id = %s and date_from >= '%s'and date_to <= '%s' LIMIT 1''' % (
            first_result, first_day, last_day)
            self.env.cr.execute(SQL5)
            results = self.env.cr.dictfetchone()
            first_result = results.get('id')
        for i in range(0, num_days+1):
            date_from = self.date_from + timedelta(days=i)
            mang_cuoi_tuan = get_weekend_days(self.date_from, self.date_to)
            if date_from not in mang_cuoi_tuan:
                if self.loai_nghi.loai_nghi == 'nghicoluong':
                    day = date_from
                    time_of_day = float(self.loai_nghi.ngay_ap_dung)*8
                    lydo = 'nghi_co_luong'
                if self.loai_nghi.loai_nghi == 'nghiphep':
                    day = date_from
                    time_of_day = float(self.loai_nghi.ngay_ap_dung)*8
                    lydo = 'nghi_phep'
                if self.loai_nghi.loai_nghi == 'nghikhongluong':
                    time_of_day = 0
                    lydo = 'nghi_khong_luong'
                employee_checkin = self.env['datn.hr.checkin.checkout.line'].search([('employee_id','=', self.employee_id.id), ('day', '=', day)]).id
                if not employee_checkin:
                    SQL = ''
                    SQL += '''INSERT INTO datn_hr_checkin_checkout_line (day,timeofday,state,ly_do,note,checkin_checkout_id,employee_id, color)
                            VALUES('%s',%s,'approved','%s','%s', %s, %s, %s)'''%(day, time_of_day, lydo,'',first_result,self.employee_id.id,255)
                    self.env.cr.execute(SQL)
        nghi = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
        ngaynghi = nghi.so_ngay_da_nghi + self.so_ngay_nghi
        nghi.write(
                {
                    'so_ngay_da_nghi': ngaynghi
                }
        )
        self.so_ngay_da_nghi = ngaynghi
        self.state = 'approved'

    def unlink(self):
        # Kiểm tra điều kiện trước khi thực hiện unlink
        if self.state == 'draft':
            # Thực hiện unlink chỉ khi điều kiện đúng
            super().unlink()  # Gọi phương thức unlink gốc
        else:
            # Xử lý khi điều kiện không đúng
            # ví dụ:
            raise ValidationError("Không thể xoá bản ghi do bản ghi đã được ghi nhận.")

class DATNLoaiNghi(models.Model):
    _name = 'datn.loai.nghi'
    _description = 'Cấu hình loại nghỉ'

    name = fields.Text(string="Tên loại nghỉ")
    code = fields.Text(string="Mã loại nghỉ")
    ngay_ap_dung = fields.Float(string="Ngày áp dụng", default='1')
    ngay_toi_da = fields.Float(string="Ngày nghỉ tối đa", default='0')
    trang_thai_ap_dung = fields.Boolean(string="Trạng thái áp dụng")
    loai_nghi = fields.Selection([('khongluong', u'Nghỉ không lương'), ('nghicoluong', u'Nghỉ có lương'), ('nghiphep', u'Nghỉ phép')],
                             string=u'Loại nghỉ', default='khongluong', track_visibility='always', required=True)
    note = fields.Text(string="Chú thích")

    _sql_constraints = [('code_loai_nghi_unique', 'unique(code)', 'Mã loại nghỉ đã tồn tại!')]

    @api.constrains('ngay_ap_dung')
    def _check_date_duong(self):
        if self.ngay_ap_dung < 0:
            raise ValidationError(_(u"Ngày áp dụng phải lớn hơn 0, yêu cầu nhập lại."))

    @api.constrains('ngay_toi_da')
    def _check_date_duong_td(self):
        if self.ngay_toi_da < 0:
            raise ValidationError(_(u"Ngày nghỉ tối đa phải lớn hơn 0, yêu cầu nhập lại."))


class HrEmplyee(models.Model):
    _inherit = "hr.employee"
    so_ngay_da_nghi = fields.Float(u"Số ngày phép đã nghỉ")
    so_ngay_duoc_phan_bo = fields.Float(u"Số ngày phép được phân bổ")

    @api.constrains('so_ngay_duoc_phan_bo', 'so_ngay_da_nghi')
    def check_date_duong_td(self):
        if self.so_ngay_da_nghi and self.so_ngay_duoc_phan_bo:
            if float(self.so_ngay_duoc_phan_bo) - float(self.so_ngay_da_nghi) < 0:
                raise ValidationError(_(u"Ngày nghỉ phép không thế vượt quá ngày nghỉ phân bổ."))





