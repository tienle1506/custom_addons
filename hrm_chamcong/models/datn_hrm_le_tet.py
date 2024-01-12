# -*- coding:utf-8 -*-
import calendar
from datetime import datetime, timedelta, date
from odoo import api, fields, models, _
from odoo.exceptions import Warning, ValidationError
import xlrd
import tempfile
import base64
import xlsxwriter
from io import BytesIO
from . import style_excel_wb
from dateutil.relativedelta import relativedelta
from ...hrm.models import constraint

def get_weekend_days(start_date, end_date):
    weekend_days = []
    current_date = start_date

    while current_date <= end_date:
        if current_date.weekday() in [5, 6]:
            weekend_days.append(current_date)
        current_date += timedelta(days=1)

    return weekend_days
class DATNHrmLeTet(models.Model):
    _name = "datn.hrm.le.tet"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = u'Quản lý ngày lễ tết'
    _order = "date_from DESC, date_to DESC"

    name = fields.Char(string=u'Tên ngày lễ tết', size=128, track_visibility='always', )
    department_id = fields.Many2many('hr.department', 'department_le_tet_rel', 'department_id', 'le_tet_id', string="Đơn vị/ phòng ban")
    data = fields.Binary('File', readonly=True)
    date_from = fields.Date(u'Từ ngày', widget='date', format='%Y-%m-%d')
    date_to = fields.Date(u'Đến ngày', widget='date', format='%Y-%m-%d')
    item_ids = fields.One2many('datn.hrm.le.tet.line', string='Items', inverse_name='le_tet_id',
                               track_visibility='always')
    state = fields.Selection([('draft', u'Soạn thảo'), ('confirmed', u'Xác nhận')],
                             string=u'Trạng thái', default='draft', track_visibility='always')

    # Import
    datn_file = fields.Binary(u'Đường dẫn tập tin', filters="*.xls,*.xlsx")
    file_name = fields.Char(u'Tên tệp tin')
    is_import = fields.Boolean(u'Import dữ liệu')



    def check_format_file_excel(self, file_name):
        if file_name.endswith('.xls') is False and file_name.endswith('.xlsx') is False and file_name.endswith(
                '.xlsb') is False:
            self.datn_file = None
            self.file_name = None
            raise ValidationError(_("File phải là định dạng 'xlsx' hoặc 'xlsb' hoặc 'xls'"))

    def import_data(self):
        if not self.is_import:
            return
        if not self.datn_file and self.is_import:
            raise ValidationError('Bạn phải chọn file nếu sử dụng import!')

    def action_loaddata(self):
        self.item_ids.unlink()
        if self.department_id:
            for department_id in self.department_id:
                employees = self.env['hr.employee'].search([('department_id', 'child_of', department_id.id), ('work_start_date', '<=', self.date_to)])
                for employee in employees:
                    lines = []
                    vals = {
                        'employee_id': employee.id,
                        'department_id': employee.department_id.id,
                        'date_from': self.date_from,
                        'date_to': self.date_to
                    }
                    lines.append((0, 0, vals))
                    self.item_ids = lines

    @api.onchange('department_id','date_from', 'date_to')
    def onchange_item_ids(self):
        self.item_ids.unlink()

    def import_data(self):
        if not self.is_import:
            return
        if not self.datn_file and self.is_import:
            raise ValidationError('Bạn phải chọn file nếu sử dụng import!')
        self.check_format_file_excel(self.file_name)
        self.item_ids.unlink()
        if self.department_id:
            self.item_ids.unlink()

            # xử lý nếu import file
            data = base64.b64decode(self.datn_file)
            _obj = tempfile.NamedTemporaryFile(delete=False)
            fname = _obj.name
            _obj.write(data)
            _obj.close()

            workbook = xlrd.open_workbook(fname)
            sheet = workbook.sheet_by_index(0)
            sheet.cell_value(0, 0)

            if sheet.nrows <= 6:
                raise ValidationError('File import đang không có dữ liệu. Vui lòng kiểm tra lại!')

            for row in range(6, sheet.nrows):
                lines = []
                code_employee = sheet.cell_value(row, 1).strip()
                employee = self.env['hr.employee'].sudo(2).search([('employee_code', '=', code_employee)])

                if not employee:
                    raise ValidationError(f'Không tồn tại nhân viên có mã {code_employee}')

                try:
                    date_from = sheet.cell_value(row, 3)
                    if date_from:
                        date_from = datetime.strptime(date_from, '%Y-%m-%d')
                    else:
                        date_from = None
                except ValueError:
                    raise ValidationError(f'Không đúng định dạng của DateTime %Y-%m-%d dòng {row}')

                try:
                    date_to = sheet.cell_value(row, 4)
                    if date_to:
                        date_to = datetime.strptime(date_to, '%Y-%m-%d')
                    else:
                        date_to = None
                except ValueError:
                    raise ValidationError(f'Không đúng định dạng của DateTime %Y-%m-%d dòng {row}')

                lines.append((0, 0, {
                    'employee_id': employee.id,
                    'date_from': date_from,
                    'date_to': date_to,
                    'note': sheet.cell_value(row, 5).strip()
                }))

                # cập nhật item_ids
                self.item_ids = lines

    #Todo Tải file mẫu import
    def download_template_file(self):
        try:
            buf = BytesIO()
            workbook = xlsxwriter.Workbook(buf, {'in_memory': True})
            style_excel = style_excel_wb.get_style(workbook)
            style_title = workbook.add_format({
                'bold': True,
                'font_size': '14',
                'font_color': 'black',
                'align': 'center',
                'valign': 'vcenter',
                'font_name': 'Times New Roman',
                'text_wrap': True,
                'border': False
            })
            style_title_danger = workbook.add_format({
                'bold': True,
                'font_size': '12',
                'font_color': 'red',
                'align': 'left',
                'valign': 'vcenter',
                'font_name': 'Times New Roman',
                'text_wrap': True,
                'border': False
            })
            style_1_require = workbook.add_format({
                'bold': True,
                'font_size': '12',
                'font_color': 'black',
                'align': 'center',
                'valign': 'vcenter',
                'font_name': 'Times New Roman',
                'text_wrap': True,
                'border': True,
                'bg_color': '#FFFF00'
            })
            style_note = workbook.add_format({
                'font_size': '12',
                'font_color': 'black',
                'align': 'left',
                'valign': 'vcenter',
                'font_name': 'Times New Roman',
                'text_wrap': True,
            })
            style_1 = workbook.add_format({
                'bold': True,
                'font_size': '12',
                'font_color': 'black',
                'align': 'center',
                'valign': 'vcenter',
                'font_name': 'Times New Roman',
                'text_wrap': True,
                'border': True
            })
            style_1_left = workbook.add_format({
                'font_size': '12',
                'font_color': 'black',
                'align': 'left',
                'valign': 'vcenter',
                'font_name': 'Times New Roman',
                'text_wrap': True,
                'border': True
            })

            # Content
            worksheet = workbook.add_worksheet('Danh sách nhân sự hưởng lễ tết')
            worksheet.set_row(4, 30)
            department_name = ''
            list_department=[]
            for bl in self.department_id:
                list = self.env['hr.department'].search([('id', 'child_of', bl.id)])
                if list:
                    for j in range(0, len(list)):
                        list_department.append(list[j].id)
                department_name += bl.name
            worksheet.merge_range(0, 0, 0, 2, 'Đơn vị/ phòng ban : %s'%(department_name), style_excel['style_12_bold_left'])
            worksheet.merge_range(2, 0, 2, 6, 'Danh sách nhân sự hưởng lễ tết', style_title)

            worksheet.merge_range(4, 0, 5, 0, 'STT', style_1)
            worksheet.merge_range(4, 1, 5, 1, 'Mã Nhân Viên', style_1_require)
            worksheet.merge_range(4, 2, 5, 2, 'Tên Nhân Viên', style_1_require)
            worksheet.merge_range(4, 3, 5, 3, 'ngày bắt đầu', style_1)
            worksheet.merge_range(4, 4, 5, 4, 'ngày kê thúc', style_1)
            worksheet.merge_range(4, 5, 5, 5, 'Note', style_1)

            for i in range(1, 7):
                worksheet.set_column(i, 4, 20)

            SQL = ''

            # Lấy chức vụ của người tạo đơn đăng ký nghỉ
            SQL += '''SELECT id, employee_code, name  FROM hr_employee where work_start_date <= '%s'::date and department_id = ANY (ARRAY %s)''' % (self.date_from, list_department)

            self.env.cr.execute(SQL)
            employees = self.env.cr.dictfetchall()
            worksheet_object = workbook.add_worksheet('Danh sách nhân sự')

            worksheet_object.set_column(0, 0, 7)
            worksheet_object.set_column(1, 1, 30)
            worksheet_object.set_column(2, 2, 50)
            worksheet_object.set_column(3, 3, 50)
            i = 1
            lst_employees = []
            worksheet_object.write(0, 0, 'STT', style_1)
            worksheet_object.write(0, 1, 'Mã nhân viên', style_1)
            worksheet_object.write(0, 2, 'Tên nhân viên', style_1)
            for item in employees:
                lst_employees.append(item['employee_code'])
                worksheet_object.write(i, 0, i, style_1)
                worksheet_object.write(i, 1, item['employee_code'], style_1_left)
                worksheet_object.write(i, 2, item['name'], style_1_left)
                i = i + 1

            worksheet.data_validation('B6:B50', {'validate': 'list', 'source': lst_employees})
            stt = 0
            for item in employees:
                stt += 1
                worksheet.write(5 + stt, 0, stt, style_1_left)
                worksheet.write(5 + stt, 1, item['employee_code'], style_1_left)
                worksheet.write(5 + stt, 2, item['name'], style_1_left)
                worksheet.write(5 + stt, 3, '', style_1_left)
                worksheet.write(5 + stt, 4, '', style_1_left)
                worksheet.write(5 + stt, 5, '', style_1_left)

            namefile = 'Mau_import_le_tet'
            # Encode to file
            workbook.close()
            buf.seek(0)
            out = base64.encodestring(buf.getvalue())
            buf.close()
            self.write({'data': out})

            return {
                'type': 'ir.actions.act_url',
                'url': '/web/content/%s/%s/%s/%s' % (
                    self._name, self.id, 'data', namefile),
                'target': 'new',
            }
        except (IOError, ValueError) as e:
            raise ValidationError(_(u'Lỗi: \n{}').format(e))

    def action_draft(self):
        delta = self.date_to - self.date_from
        num_days = delta.days
        mang_cuoi_tuan = get_weekend_days(self.date_from, self.date_to)
        for record in self.item_ids:
            for i in range(0, num_days + 1):
                day = record.date_from + timedelta(days=i)
                if day not in mang_cuoi_tuan:
                    employee_checkin = self.env['datn.hr.checkin.checkout.line'].search(
                        [('employee_id', '=', record.employee_id.id), ('day', '=', day)]).id
                    if employee_checkin:
                        SQL = ''
                        SQL += '''DELETE FROM datn_hr_checkin_checkout_line WHERE id = %s''' % (employee_checkin)
                        self.env.cr.execute(SQL)
        self.state = 'draft'

    def action_confirmed(self):
        cr = self.env.cr
        # Thêm vào check in check out của nhân viên
        date_format = '%Y-%m-%d'
        # Tính số ngày giữa hai ngày
        delta = self.date_to - self.date_from
        num_days = delta.days
        formatted_date = datetime(self.date_from.year, self.date_to.month, 1).date()
        for record in self.item_ids:
            SQL1 = ''
            SQL1 += '''SELECT ck.id FROM datn_hr_checkin_checkout_line ckl
                                LEFT JOIN datn_hr_checkin_checkout ck ON ck.id = ckl.checkin_checkout_id
                                WHERE ckl.employee_id = %s AND to_char(ck.date_from, 'mmYYYY') = to_char('%s'::date, 'mmYYYY')
                                LIMIT 1
                    ''' % (record.employee_id.id, record.date_from)
            self.env.cr.execute(SQL1)
            results = self.env.cr.dictfetchone()
            if not results:
                SQL = ''
                SQL += '''SELECT datn_hr_checkin_checkout.id FROM datn_hr_checkin_checkout
                                    LEFT JOIN hr_department ON hr_department.id = datn_hr_checkin_checkout.department_id
                                    WHERE date_from = '%s' AND department_id in (select unnest(get_list_parent_department(%s)))
                                    ORDER BY hr_department.department_level
                                    LIMIT 1
                        ''' % (formatted_date, record.department_id.id)
                self.env.cr.execute(SQL)
                results = self.env.cr.dictfetchone()
            # Lấy giá trị đầu tiên thoả mãn
            if results:
                first_result = results.get('id')
            else:
                SQL3 = ''
                SQL3 += '''SELECT id from hr_department WHERE department_level = 1 AND id in (select unnest(get_list_parent_department(%s)))'''%(record.department_id.id)
                self.env.cr.execute(SQL3)
                results = self.env.cr.dictfetchone()
                first_result = results.get('id')
                # Lấy ngày đầu tiên của tháng
                first_day = record.date_from.replace(day=1)
                # Lấy ngày cuối cùng của tháng
                next_month = (datetime.strptime(str(record.date_from), "%Y-%m-%d") + relativedelta(months=1)).replace(day=1)
                last_day = (next_month - timedelta(days=1)).date()
                name = 'Bảng thanh check-in check-out từ ngày %s đến ngày %s'%(first_day,last_day)
                SQL4 = ''
                SQL4 += '''INSERT INTO datn_hr_checkin_checkout (department_id, date_from, date_to, name, state)
                                                   VALUES(%s,'%s','%s', '%s', 'draft')''' % (first_result, first_day, last_day,name )
                self.env.cr.execute(SQL4)

                SQL5 = ''
                SQL5 += '''SELECT id from datn_hr_checkin_checkout WHERE department_id = %s and date_from >= '%s'and date_to <= '%s' LIMIT 1''' % (first_result,first_day,last_day)
                self.env.cr.execute(SQL5)
                results = self.env.cr.dictfetchone()
                first_result = results.get('id')
            for i in range(0, num_days + 1):
                date_from = record.date_from + timedelta(days=i)
                day = date_from
                time_of_day = 8
                lydo = 'nghi_co_luong'
                employee_checkin = self.env['datn.hr.checkin.checkout.line'].search(
                    [('employee_id', '=', record.employee_id.id), ('day', '=', day)]).id
                if not employee_checkin:
                    SQL = ''
                    SQL += '''INSERT INTO datn_hr_checkin_checkout_line (day,timeofday,state,ly_do,note,checkin_checkout_id,employee_id, color)
                                    VALUES('%s',%s,'approved','%s','%s', %s, %s, %s)''' % (
                    day, time_of_day, lydo, str(self.name), first_result, record.employee_id.id, 255)
                    self.env.cr.execute(SQL)
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
            # Thực hiện unlink chỉ khi điều kiện đúng
            return super(DATNHrmLeTet, self).unlink()
class DATNHrmLeTetLine(models.Model):
    _name = 'datn.hrm.le.tet.line'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = u'Bảng chi tiết nhân sự hưởng lễ tết'
    _order = "department_id, employee_id"

    employee_id = fields.Many2one('hr.employee', string=u'Nhân viên', ondelete='cascade')
    le_tet_id = fields.Many2one('datn.hrm.le.tet', string=u'Bảng lễ tết', ondelete='cascade', required=True)
    note = fields.Text(string='Ghi chú')
    date_from = fields.Date(u'Từ ngày', widget='date', related='le_tet_id.date_from', store=True, format='%Y-%m-%d')
    date_to = fields.Date(u'Đến ngày', widget='date', related='le_tet_id.date_to', store=True, format='%Y-%m-%d')
    department_id = fields.Many2one('hr.department', ondelete='cascade', string='Đơn vị/ phòng ban', related='employee_id.department_id', store=True )

    _sql_constraints = [
        ('unique_employee_le_tet', 'unique(employee_id, le_tet_id)', u'Nhân viên chỉ được tạo 1 lần trong bản ghi này.')
    ]

    @api.constrains('date_from', 'date_to')
    def checkdate(self):
        if self.id:
            SQL = ''
            SQL += '''SELECT * FROM datn_hrm_le_tet_line WHERE id != %s and employee_id = %s AND ((date_from BETWEEN '%s' AND '%s') 
            OR (date_to BETWEEN '%s' AND '%s')) '''%(self.id, self.employee_id.id, self.date_from, self.date_to,self.date_from, self.date_to)
            self.env.cr.execute(SQL)
            employees = self.env.cr.dictfetchall()
        else:
            SQL = ''
            SQL += '''SELECT * FROM datn_hrm_le_tet_line WHERE employee_id = %s AND ((date_from BETWEEN '%s' AND '%s') 
                        OR (date_to BETWEEN '%s' AND '%s')) ''' % (
            self.employee_id.id, self.date_from, self.date_to, self.date_from, self.date_to)
            self.env.cr.execute(SQL)
            employees = self.env.cr.dictfetchall()
        if employees:
            raise ValidationError("Ngày lễ tết của bạn đang tạo có một ngày khác đã được tạo, năm trong khoảng này")




