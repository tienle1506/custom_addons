# -*- coding:utf-8 -*-
import calendar
from datetime import datetime, timedelta, time
from odoo import api, fields, models, _
from odoo.exceptions import Warning, ValidationError
import xlrd
import tempfile
import base64
import xlsxwriter
from io import BytesIO
from . import style_excel_wb
from ...hrm.models import constraint

class DATNHrCheckInCheckOut(models.Model):
    _name = 'datn.hr.checkin.checkout'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = u'Bảng checkin - checkout'
    _order = "date_from DESC, date_to DESC"

    data = fields.Binary('File', readonly=True)
    name = fields.Char(string=u'Tên Bảng CheckIn CheckOut', size=128, track_visibility='always', )
    department_id = fields.Many2one('hr.department',ondelete='cascade', string='Đơn vị/Phòng ban', required=True,
                    tracking=True)
    date_from = fields.Date(u'Từ ngày', required=True, widget='date', format='%m-%d-%Y')
    date_to = fields.Date(u'Đến ngày', required=True, widget='date', format='%m-%d-%Y')
    item_ids = fields.One2many('datn.hr.checkin.checkout.line', string='Items', inverse_name='checkin_checkout_id',
                               track_visibility='always')
    state = fields.Selection([('draft', u'Soạn thảo'), ('confirmed', u'Xác nhận')],
                             string=u'Trạng thái', default='draft', track_visibility='always')

    # Import
    datn_file = fields.Binary(u'Đường dẫn tập tin', filters="*.xls,*.xlsx")
    file_name = fields.Char(u'Tên tệp tin')
    is_import = fields.Boolean(u'Import dữ liệu')

    _sql_constraints = [
        ('unique_department_day', 'unique(department_id, date_from)', u'Phòng ban đã được tạo để ghi checkin checkout')
    ]

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

        self.check_format_file_excel(self.file_name)
        self.item_ids.unlink()
        if self.department_id.id:
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
                    checkin = str(sheet.cell_value(row, 3)).strip() if sheet.cell_value(row, 3) else ''
                    if checkin:
                        # Chuyển đổi chuỗi datetime thành đối tượng datetime
                        checkin_datetime = datetime.strptime(checkin, '%d-%m-%Y %H:%M:%S')

                        # Trừ đi 5 giờ bằng cách sử dụng timedelta
                        new_datetime = checkin_datetime - timedelta(hours=7)

                        # Chuyển đổi đối tượng datetime thành chuỗi datetime mới
                        checkin = new_datetime.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        checkin = None
                except ValueError:
                    raise ValidationError(f'Không đúng định dạng của DateTime %d-%m-%Y %H:%M:%S dòng {row}')

                try:
                    checkout = str(sheet.cell_value(row, 4)).strip() if sheet.cell_value(row, 4) else ''
                    if checkout:
                        # Chuyển đổi chuỗi datetime thành đối tượng datetime
                        checkout_datetime = datetime.strptime(checkout, '%d-%m-%Y %H:%M:%S')

                        # Trừ đi 5 giờ bằng cách sử dụng timedelta
                        new_datetime = checkout_datetime - timedelta(hours=7)

                        # Chuyển đổi đối tượng datetime thành chuỗi datetime mới
                        checkout = new_datetime.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        checkout = None
                except ValueError:
                    raise ValidationError(f'Không đúng định dạng của DateTime %d-%m-%Y %H:%M:%S dòng {row}')
                if employee.id:
                    if checkin and checkout:
                        state = 'approved'
                    else:
                        state = 'draft'
                    lines.append((0, 0, {
                        'employee_id': employee.id,
                        'checkin': checkin,
                        'checkout': checkout,
                        'state': state,
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
            worksheet = workbook.add_worksheet('Danh sách checkin - checkout')
            worksheet.set_row(4, 30)

            worksheet.merge_range(0, 0, 0, 2, 'Đơn vị/ phòng ban : %s'%(self.department_id.name), style_excel['style_12_bold_left'])
            worksheet.merge_range(2, 0, 2, 6, 'Danh Sách checkin - checkout', style_title)

            worksheet.merge_range(4, 0, 5, 0, 'STT', style_1)
            worksheet.merge_range(4, 1, 5, 1, 'Mã Nhân Viên', style_1_require)
            worksheet.merge_range(4, 2, 5, 2, 'Tên Nhân Viên', style_1_require)
            worksheet.merge_range(4, 3, 5, 3, 'Checkin \ndd-mm-YYYY HH:MM:SS', style_1)
            worksheet.merge_range(4, 4, 5, 4, 'Checkout \ndd-mm-YYYY HH:MM:SS', style_1)
            worksheet.merge_range(4, 5, 5, 5, 'Note', style_1)

            for i in range(1, 6):
                worksheet.set_column(i, 4, 20)

            # Danh mục đơn vị đào tạo
            SQL = ''
            # Lấy chức vụ của người tạo đơn đăng ký nghỉ
            SQL += '''SELECT id, employee_code, name  FROM hr_employee where work_start_date <= '%s'::date and department_id in (SELECT UNNEST(child_ids) FROM child_department WHERE parent_id in (%s))''' % (self.date_from, self.department_id.id)

            self.env.cr.execute(SQL)
            employees = self.env.cr.dictfetchall()
            worksheet_object = workbook.add_worksheet('Danh sách nhân sự')
            worksheet_object.set_column(0, 0, 7)
            worksheet_object.set_column(1, 1, 30)
            worksheet_object.set_column(2, 2, 50)
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
            namefile = 'Mau_import_mon_hoc'
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
        self.state = 'draft'
    def action_confirmed(self):
        self.state = 'confirmed'

    def unlink(self):
        # Kiểm tra điều kiện trước khi thực hiện unlink
        if self.state == 'draft':
            # Thực hiện unlink chỉ khi điều kiện đúng
            super().unlink()  # Gọi phương thức unlink gốc
        else:
            # Xử lý khi điều kiện không đúng
            # ví dụ:
            raise ValidationError("Không thể xoá bản ghi do bản ghi đã được ghi nhận.")

class DATNHrCheckInCheckOutLine(models.Model):
    _name = 'datn.hr.checkin.checkout.line'
    _inherit = ['mail.thread']
    _description = u'Bảng chi tiết checkin - checkout'
    _order = "employee_id, day desc"
    _res_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string=u'Nhân viên', ondelete='cascade')
    checkin_checkout_id = fields.Many2one('datn.hr.checkin.checkout', string=u'Bảng CheckIn CheckOut', ondelete='cascade', required=True)
    note = fields.Text(string='Ghi chú', compute='_compute_date', store=True)
    checkout = fields.Datetime(string='Giờ ra', widget='date', format='%m-%d-%Y')
    checkin = fields.Datetime(string='Giờ vào', widget='date', format='%m-%d-%Y')
    day = fields.Date(string='Ngày', compute='_compute_date', store=True)
    timeofday = fields.Float(string="Số giờ trong ngày", compute='_compute_date', store=True)
    ly_do = fields.Selection([('quen_checkin', u'Quên chấm công vào'), ('quen_checkout', u'Quên chấm công ra'), ('quen',u'Quên chấm công vào và chấm công ra'),
                              ('lam_sang',u'Đi làm nửa ngày sáng, nghỉ chiều'),('lam_chieu',u'Đi làm nửa ngày chiều, nghỉ sáng'),('khac', u'Khác'),
                             ('nghi_khong_luong', u'Nghỉ không lương'), ('nghi_khong_phep', u'Tự ý nghỉ không xin phép'), ('nghi_phep', u'Nghỉ có phép'),
                              ('nghi_co_luong', u'Nghỉ có lương')],
                             string=u'Lý do xác nhận chấm công', default='quen', track_visibility='always')
    state = fields.Selection([('draft', u'Gửi phê duyệt'), ('confirmed', u'Chờ phê duệt'), ('approved', u'Phê duyệt'),
                              ('refused', u'Từ chối')],
                             string=u'Trạng thái', default='draft', track_visibility='always')
    nguoi_duyet = fields.Many2many('hr.employee', 'employee_duyet_checkin_checkout_rel', 'checkin_checkout_id', 'employee_id',
                                   string="Người duyệt")
    color = fields.Integer(string='Màu', compute='_compute_date', store=True, default=16711680)

    _sql_constraints = [
        ('unique_employee_day', 'unique(employee_id, day)', u'Nhân viên ững với mõi ngày chỉ có 1 bản ghi chấm công')
    ]

    @api.depends('checkin', 'checkout')
    def _compute_date(self):
        for record in self:
            if not record.checkin and not record.checkout:
                return
            elif record.checkin:
                record.day = record.checkin.date()
            elif record.checkout:
                record.day = record.checkout.date()
            if record.checkin and record.checkout:
                record.state = 'approved'
                checkout_time_io = record.checkout.time()  # Trích xuất giá trị thời gian hiện tại
                target_time = time(hour=6, minute=30)
                if checkout_time_io >= target_time:
                    time_difference = record.checkout - record.checkin
                    record.timeofday = time_difference.total_seconds() / 3600
                record.note = ''
                record.color = 255
            else:
                record.timeofday = 0
                if record.checkin and not record.checkout:
                    record.color = 16711680
                    record.note = 'Quên chấm công ra'
                elif record.checkout and not record.checkin:
                    record.note = 'Quên chấm công vào'
                    record.color = 16711680


    @property
    def date_from(self):
        return self.env.context.get('date_from', False)

    @property
    def date_to(self):
        return self.env.context.get('date_to', False)

    @api.constrains('checkin', 'checkout')
    def _check_checkin_checkout(self):
        for record in self:
            date_from = record.checkin_checkout_id.date_from
            date_to = record.checkin_checkout_id.date_to
            if date_from and record.checkin:
                if date_from > record.checkin.date():
                    raise ValidationError(_(u'Giờ vào phải nằm trong tháng !'))

            if date_to and record.checkout:
                if date_to < record.checkout.date():
                    raise ValidationError(_(u'Giờ ra phải nằm trong tháng !'))

            if date_from and date_to and record.checkin and record.checkout:
                if record.checkin > record.checkout:
                    raise ValidationError(_(u'Giờ vào phải nhỏ hơn giờ ra !'))

                if date_from > record.checkin.date() or date_to < record.checkout.date():
                    raise ValidationError(_(u'Giờ vào giờ ra phải nằm trong tháng !'))

                if record.checkin.date() != record.checkout.date():
                    raise ValidationError(_(u'Giờ vào giờ ra của 1 bản ghi phải nằm trong 1 ngày!'))

    @api.onchange('checkin', 'checkout')
    def _ochange_checkin_checkout(self):
        for record in self:
            date_from = record.checkin_checkout_id.date_from
            date_to = record.checkin_checkout_id.date_to
            if date_from and record.checkin:
                if date_from > record.checkin.date():
                    raise ValidationError(_(u'Giờ vào phải nằm trong tháng !'))

            if date_to and record.checkout:
                if date_to < record.checkout.date():
                    raise ValidationError(_(u'Giờ ra phải nằm trong tháng !'))

            if date_to and date_from and record.checkin and record.checkout:
                if record.checkin > record.checkout:
                    raise ValidationError(_(u'Giờ vào phải nhỏ hơn giờ ra !'))

                if date_from > record.checkin.date() or date_to < record.checkout.date():
                    raise ValidationError(_(u'Giờ vào giờ ra phải nằm trong tháng !'))

                if record.checkin.date() != record.checkout.date():
                    raise ValidationError(_(u'Giờ vào giờ ra của 1 bản ghi phải nằm trong 1 ngày!'))

    def read(self, fields=None, load='_classic_read'):
        self.check_access_rule('read')
        return super(DATNHrCheckInCheckOutLine, self).read(fields, load=load)

    def search(self, args, offset=0, limit=None, order=None, count=False):
        domain = []
        return super(DATNHrCheckInCheckOutLine, self).search(domain + args, offset, limit, order, count=count)

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        emp_domain = self.check_employee_view()
        return super(DATNHrCheckInCheckOutLine, self)._name_search(name, args=args + emp_domain, operator=operator,
                                                                  limit=limit)


    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        emp_domain = self.check_employee_view()
        return super(DATNHrCheckInCheckOutLine, self).search_read(domain=domain + emp_domain, fields=fields,
                                                                  offset=offset, limit=limit, order=order)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        emp_domain = self.check_employee_view()
        return super(DATNHrCheckInCheckOutLine, self).read_group(domain + emp_domain, fields, groupby, offset=offset,
                                                                 limit=limit, orderby=orderby, lazy=lazy)
    def check_employee_view(self):
        context = self.env.context or {}
        emp_domain = []
        user = self.env.user
        employee_id = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
        if context.get('view_from_action', False):
            emp_domain = [('employee_id', '=', employee_id.id)]
        if context.get('view_from_action_phe_duyet', False):
            emp_domain = [('nguoi_duyet', '=', employee_id.id), ('state', '=', 'confirmed')]
        return emp_domain

    def action_draft(self):
        self.state = 'draft'

    def action_send_approve(self):
        nguoi_duyet = []
        for emp in self.nguoi_duyet:
            if emp.personal_email:
                nguoi_duyet.append(emp.personal_mail.strip())
        header = '''Thông báo phê duyệt chấm công %s''' % (self.employee_id.name)
        ly_do_value = self.ly_do
        ly_do_label = dict(self._fields['ly_do'].selection).get(ly_do_value)
        content = u'Nhân viên %s tạo đơn xác nhận chấm công \nLý do: %s \nNgày: %s \nGhi chú: %s \nTrang web: http://localhost:8088/web' % (
            str(self.employee_id.name), str(ly_do_label), self.day.strftime('%d/%m/%Y'), self.note)
        if nguoi_duyet and len(nguoi_duyet) > 0:
            self.env['my.mail.sender'].send_mail_to_customer(nguoi_duyet, header, content)
        self.state = 'confirmed'
    def action_refuse(self):
        self.state = 'refused'
    def action_approve(self):
        day = self.day
        if self.ly_do == 'quen_checkin':
            desired_datetime = datetime.combine(day, datetime.min.time()) + timedelta(hours=1)
            self.checkin = desired_datetime
            self.state = 'approved'
        elif self.ly_do == 'quen_checkout':
            desired_datetime = datetime.combine(day, datetime.min.time()) + timedelta(hours=10)
            self.checkout = desired_datetime
            self.state = 'approved'
        elif self.ly_do == 'quen':
            desired_datetime = datetime.combine(day, datetime.min.time()) + timedelta(hours=10)
            self.checkout = desired_datetime
            desired_datetimeci = datetime.combine(day, datetime.min.time()) + timedelta(hours=1)
            self.checkin = desired_datetimeci
            self.state = 'approved'
        elif self.ly_do == 'lam_sang':
            desired_datetime = datetime.combine(day, datetime.min.time()) + timedelta(hours=5)
            self.checkout = desired_datetime
            self.state = 'approved'
        elif self.ly_do == 'lam_chieu':
            desired_datetime = datetime.combine(day, datetime.min.time()) + timedelta(hours=10)
            self.checkin = self.checkout
            self.checkout = desired_datetime
            self.state = 'approved'
        else:
            self.state = 'approved'


