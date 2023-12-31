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
from ...hrm_chamcong.models import style_excel_wb
from dateutil.relativedelta import relativedelta

class DATNHrmTroCapPhuCap(models.Model):
    _name = "datn.trocap.phucap"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = u'Quản lý trợ cấp phụ cấp'
    _order = "ngay_chi_tra desc"

    name = fields.Char(string=u'Tên trợ cấp, phụ cấp', size=128, track_visibility='always', )
    department_id = fields.Many2many('hr.department', 'department_trocap_phucap_rel', 'trocap_phucap_id','department_id', string="Đơn vị/ phòng ban")
    data = fields.Binary('File', readonly=True)
    muc_huong_chung = fields.Integer('Mức hưởng chung')
    item_ids = fields.One2many('datn.trocap.phucap.line', string='Items', inverse_name='trocap_phucap_id',
                               track_visibility='always')
    ngay_chi_tra = fields.Date(u'Ngày chi trả', required=True, default=fields.Date.today)
    ngay_tao = fields.Date(u'Ngày tạo', widget='date', format='%Y-%m-%d', default=fields.Date.today)
    state = fields.Selection([('draft', u'Soạn thảo'), ('confirmed', u'Xác nhận')],
                             string=u'Trạng thái', default='draft', track_visibility='always')
    type_id = fields.Many2one('datn.config.trocap.phucap', string="Loại")

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

    def action_loaddata(self):
        self.item_ids.unlink()
        lines = []
        if self.department_id:
            for department_id in self.department_id:
                employees = self.env['hr.employee'].search([('department_id', 'child_of', department_id.id), ('work_start_date', '<=', date.today())])
                for employee in employees:
                    lines.append((0, 0, {'employee_id': employee.id, 'muc_huong': self.muc_huong_chung}))
        self.item_ids = lines

    @api.onchange('department_id')
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


                muc_huong = sheet.cell_value(row, 3)
                if not muc_huong:
                    raise ValidationError(f'Mức hưởng không thể để trống, háy thêm dữ liệu dòng {row}')

                lines.append((0, 0, {
                    'employee_id': employee.id,
                    'muc_huong': muc_huong,
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
            worksheet = workbook.add_worksheet('Danh sách nhân sự hưởng phụ cấp, trợ cấp')
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
            worksheet.merge_range(2, 0, 2, 6, 'Danh sách nhân sự hưởng phụ cấp, trợ cấp', style_title)

            worksheet.merge_range(4, 0, 5, 0, 'STT', style_1)
            worksheet.merge_range(4, 1, 5, 1, 'Mã Nhân Viên', style_1_require)
            worksheet.merge_range(4, 2, 5, 2, 'Tên Nhân Viên', style_1_require)
            worksheet.merge_range(4, 3, 5, 3, 'Mức hưởng', style_1)
            worksheet.merge_range(4, 4, 5, 4, 'Ghi chú', style_1)

            for i in range(1, 7):
                worksheet.set_column(i, 4, 20)

            SQL = ''

            # Lấy chức vụ của người tạo đơn đăng ký nghỉ
            SQL += '''SELECT id, employee_code, name  FROM hr_employee where work_start_date <= '%s'::date and department_id = ANY(ARRAY(SELECT child_ids FROM child_department WHERE parent_id = ANY (ARRAY %s))) ''' % (self.ngay_chi_tra, list_department)

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

            namefile = 'Mau_import_tro_cap_phucap'
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
        can_unlink = True
        for record in self:
            if record.state != 'draft':
                can_unlink = False
                # Xử lý khi điều kiện không đúng
                # ví dụ:
                raise ValidationError("Không thể xoá bản ghi do bản ghi đã được ghi nhận.")

        if can_unlink:
            # Thực hiện unlink chỉ khi điều kiện đúng
            return super(DATNHrmTroCapPhuCap, self).unlink()
class DATNHrmLeTetLine(models.Model):
    _name = 'datn.trocap.phucap.line'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = u'Bảng chi tiết nhân sự hưởng trợ cấp, phụ cấp'
    _order = "department_id, employee_id"

    employee_id = fields.Many2one('hr.employee', string=u'Nhân viên', ondelete='cascade')
    trocap_phucap_id = fields.Many2one('datn.trocap.phucap', string=u'Bảng trợ cấp, phụ cấp', ondelete='cascade', required=True)
    note = fields.Text(string='Ghi chú')
    muc_huong = fields.Integer('Mức hưởng')
    department_id = fields.Many2one('hr.department', ondelete='cascade', string='Đơn vị/ phòng ban', related='employee_id.department_id', store=True )

    _sql_constraints = [
        ('unique_employee_phucap_trocap', 'unique(employee_id, phucap_trocap_id)', u'Nhân viên chỉ được tạo 1 lần trong bản ghi này.')
    ]





