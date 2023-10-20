# -*- coding:utf-8 -*-
import calendar
from datetime import datetime, timedelta
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
    block_id = fields.Many2one('hrm.blocks', string='Khối', required=True,
                    default=lambda self: self.default_block_profile(),
                    tracking=True)
    date_from = fields.Date(u'Từ ngày', required=True, widget='date', format='%Y-%m-%d')
    date_to = fields.Date(u'Đến ngày', required=True, widget='date', format='%Y-%m-%d')
    item_ids = fields.One2many('datn.hr.checkin.checkout.line', string='Items', inverse_name='checkin_checkout_id',
                               track_visibility='always')
    state = fields.Selection([('draft', u'Soạn thảo'), ('confirmed', u'Xác nhận')],
                             string=u'Trạng thái', default='draft', track_visibility='always')

    # Import
    datn_file = fields.Binary(u'Đường dẫn tập tin', filters="*.xls,*.xlsx")
    file_name = fields.Char(u'Tên tệp tin')
    is_import = fields.Boolean(u'Import dữ liệu')

    def default_block_profile(self):
        """kiểm tra điều kiện giữa khối văn phòng và thương mại"""
        if self.env.user.block_id == constraint.BLOCK_OFFICE_NAME:
            return self.env['hrm.blocks'].search([('name', '=', constraint.BLOCK_OFFICE_NAME)])
        else:
            return self.env['hrm.blocks'].search([('name', '=', constraint.BLOCK_COMMERCE_NAME)])

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
        if self.block_id.id:
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
                employee = self.env['hrm.employee.profile'].sudo(2).search([('employee_code_new', '=', code_employee)])

                if not employee:
                    raise ValidationError(f'Không tồn tại nhân viên có mã {code_employee}')

                try:
                    checkin = sheet.cell_value(row, 3)
                    if checkin:
                        checkin = datetime.strptime(checkin, '%Y-%m-%d %H:%M:%S')
                    else:
                        checkin = None
                except ValueError:
                    raise ValidationError(f'Không đúng định dạng của DateTime %Y-%m-%d %H:%M:%S dòng {row}')

                try:
                    checkout = sheet.cell_value(row, 4)
                    if checkout:
                        checkout = datetime.strptime(checkout, '%Y-%m-%d %H:%M:%S')
                    else:
                        checkout = None
                except ValueError:
                    raise ValidationError(f'Không đúng định dạng của DateTime %Y-%m-%d %H:%M:%S dòng {row}')

                lines.append((0, 0, {
                    'employee_id': employee.id,
                    'checkin': checkin,
                    'checkout': checkout,
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

            worksheet.merge_range(0, 0, 0, 2, 'Khối : %s'%(self.block_id.name), style_excel['style_12_bold_left'])
            worksheet.merge_range(2, 0, 2, 6, 'Danh Sách checkin - checkout', style_title)

            worksheet.merge_range(4, 0, 5, 0, 'STT', style_1)
            worksheet.merge_range(4, 1, 5, 1, 'Mã Nhân Viên', style_1_require)
            worksheet.merge_range(4, 2, 5, 2, 'Tên Nhân Viên', style_1_require)
            worksheet.merge_range(4, 3, 5, 3, 'Checkin', style_1)
            worksheet.merge_range(4, 4, 5, 4, 'Checkout', style_1)
            worksheet.merge_range(4, 5, 5, 5, 'Note', style_1)

            for i in range(1, 6):
                worksheet.set_column(i, 4, 20)

            # Danh mục đơn vị đào tạo
            SQL = ''
            # Lấy chức vụ của người tạo đơn đăng ký nghỉ
            SQL += '''SELECT id, employee_code_new, name  FROM hrm_employee_profile where work_start_date <= '%s'::date and block_id = %s''' % (self.date_from, self.block_id.id)

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
                lst_employees.append(item['employee_code_new'])
                worksheet_object.write(i, 0, i, style_1)
                worksheet_object.write(i, 1, item['employee_code_new'], style_1_left)
                worksheet_object.write(i, 2, item['name'], style_1_left)
                i = i + 1

            worksheet.data_validation('B6:B50', {'validate': 'list', 'source': lst_employees})
            stt = 0
            for item in employees:
                stt += 1
                worksheet.write(5 + stt, 0, stt, style_1_left)
                worksheet.write(5 + stt, 1, item['employee_code_new'], style_1_left)
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


class DATNHrCheckInCheckOutLine(models.Model):
    _name = 'datn.hr.checkin.checkout.line'
    _inherit = ['mail.thread']
    _description = u'Bảng chi tiết checkin - checkout'
    _order = "employee_id, checkin desc, checkout desc"

    employee_id = fields.Many2one('hrm.employee.profile', string=u'Nhân viên', ondelete='cascade')
    checkin_checkout_id = fields.Many2one('datn.hr.checkin.checkout', string=u'Bảng CheckIn CheckOut', ondelete='cascade', required=True)
    note = fields.Text(string='Ghi chú')
    checkout = fields.Datetime(string='Giờ ra')
    checkin = fields.Datetime(string='Giờ vào')
    day = fields.Date(string='Ngày', compute='_compute_date', store=True)

    _sql_constraints = [
        ('unique_employee_day', 'unique(employee_id, day)', u'Nhân viên ững với mõi ngày chỉ có 1 bản ghi chấm công')
    ]

    @api.depends('checkin', 'checkout')
    def _compute_date(self):
        if not self.checkin and not self.checkout:
            return
        elif self.checkin:
            self.day = self.checkin.date()
        elif self.checkout:
            self.day = self.checkout.date()

    # def name_search(self, name='', args=None, operator='ilike', limit=100):
    #     context = self.env.context or {}
    #     emp_domain = []
    #     if context.get('parent_block_id', False):
    #         emp_domain = [('block_id', '=', context.get('parent_block_id'))]
    #     return super(DATNHrCheckInCheckOutLine, self).name_search(name, args=args + emp_domain, operator=operator,
    #                                                               limit=limit)
    #
    # def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
    #     context = self.env.context or {}
    #     emp_domain = []
    #     if context.get('parent_block_id', False):
    #         emp_domain = [('block_id', '=', context.get('parent_block_id'))]
    #     return super(DATNHrCheckInCheckOutLine, self).search_read(domain=domain + emp_domain, fields=fields,
    #                                                               offset=offset, limit=limit, order=order)
    #
    # def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
    #     context = self.env.context or {}
    #     emp_domain = []
    #     if context.get('parent_block_id', False):
    #         emp_domain = [('block_id', '=', context.get('parent_block_id'))]
    #     return super(DATNHrCheckInCheckOutLine, self).read_group(domain + emp_domain, fields, groupby, offset=offset,
    #                                                              limit=limit, orderby=orderby, lazy=lazy)

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
            if record.checkin:
                if date_from > record.checkin.date():
                    raise ValidationError(_(u'Giờ vào phải nằm trong tháng !'))

            if record.checkout:
                if date_to < record.checkout.date():
                    raise ValidationError(_(u'Giờ ra phải nằm trong tháng !'))

            if record.checkin and record.checkout:
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
            if record.checkin:
                if date_from > record.checkin.date():
                    raise ValidationError(_(u'Giờ vào phải nằm trong tháng !'))

            if record.checkout:
                if date_to < record.checkout.date():
                    raise ValidationError(_(u'Giờ ra phải nằm trong tháng !'))

            if record.checkin and record.checkout:
                if record.checkin > record.checkout:
                    raise ValidationError(_(u'Giờ vào phải nhỏ hơn giờ ra !'))

                if date_from > record.checkin.date() or date_to < record.checkout.date():
                    raise ValidationError(_(u'Giờ vào giờ ra phải nằm trong tháng !'))

                if record.checkin.date() != record.checkout.date():
                    raise ValidationError(_(u'Giờ vào giờ ra của 1 bản ghi phải nằm trong 1 ngày!'))


