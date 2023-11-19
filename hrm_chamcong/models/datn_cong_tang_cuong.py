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
class DATNHrmLeTet(models.Model):
    _name = "datn.cong.tang.cuong"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = u'Quản lý công phép tăng cường'
    _order = "ngay_tao DESC"

    name = fields.Char(string=u'Tên công tăng cường', size=128, track_visibility='always', )
    year = fields.Selection(selection=[(str(year), str(year)) for year in range(1975, 2099)], string='Năm áp dụng', default=str(fields.Date.today().year))
    block_id = fields.Many2many('hrm.blocks', 'block_cong_them_rel', 'block_id', 'cong_them_id', string="Khối")
    data = fields.Binary('File', readonly=True)
    ngay_tao = fields.Date(u'Ngày tạo', widget='date', format='%Y-%m-%d', default=fields.Date.today)
    cong_them = fields.Integer(string=u'Công phép bổ sung')
    item_ids = fields.One2many('datn.cong.tang.cuong.line', string='Items', inverse_name='cong_them_id',
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
        for item in self.item_ids:
            if item['employee_id'].id:
                item['cong_them'] = self.cong_them

    def import_data(self):
        if not self.is_import:
            return
        if not self.datn_file and self.is_import:
            raise ValidationError('Bạn phải chọn file nếu sử dụng import!')
        self.check_format_file_excel(self.file_name)
        self.item_ids.unlink()
        if self.block_id:
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
                    cong_them = sheet.cell_value(row, 3)
                    if cong_them and int(cong_them):
                        cong_them = float(cong_them)
                    else:
                        cong_them = 0
                except ValueError:
                    raise ValidationError(f'Công thêm phải có dạng số nguyên')


                lines.append((0, 0, {
                    'employee_id': employee.id,
                    'cong_them': cong_them,
                    'note': sheet.cell_value(row, 4).strip()
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
            worksheet = workbook.add_worksheet('Danh sách nhân sự hưởng oông tăng cường')
            worksheet.set_row(4, 30)
            block_name = ''
            list_block=[]
            for bl in self.block_id:
                list_block.append(bl.id)
                block_name += bl.name
            worksheet.merge_range(0, 0, 0, 2, 'Khối : %s'%(block_name), style_excel['style_12_bold_left'])
            worksheet.merge_range(2, 0, 2, 6, 'Danh sách nhân sự hưởng công thêm ', style_title)

            worksheet.merge_range(4, 0, 5, 0, 'STT', style_1)
            worksheet.merge_range(4, 1, 5, 1, 'Mã Nhân Viên', style_1_require)
            worksheet.merge_range(4, 2, 5, 2, 'Tên Nhân Viên', style_1_require)
            worksheet.merge_range(4, 3, 5, 3, 'Công phát sinh', style_1)
            worksheet.merge_range(4, 4, 5, 4, 'Note', style_1)

            for i in range(1, 6):
                worksheet.set_column(i, 4, 20)

            SQL = ''

            # Lấy chức vụ của người tạo đơn đăng ký nghỉ
            SQL += '''SELECT id, employee_code_new, name  FROM hrm_employee_profile where work_start_date <= '%s'::date and block_id = ANY (ARRAY %s)''' % (datetime.now(), list_block)

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
                worksheet.write(5 + stt, 3, 0, style_1_left)
                worksheet.write(5 + stt, 4, '', style_1_left)
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
        self.env['cron.job.cong.phep'].run()
    def action_confirmed(self):
        self.state = 'confirmed'
        self.env['cron.job.cong.phep'].run()
class DATNCongTangCuongLine(models.Model):
    _name = 'datn.cong.tang.cuong.line'
    _inherit = ['mail.thread']
    _description = u'Bảng chi tiết nhân sự hưởng công tăng cường'
    _order = "block_id, employee_id"

    employee_id = fields.Many2one('hrm.employee.profile', string=u'Nhân viên', ondelete='cascade')
    cong_them_id = fields.Many2one('datn.cong.tang.cuong', string='Bảng công tăng cường', ondelete='cascade',
                                   required=True)
    note = fields.Text(string='Ghi chú')
    year = fields.Selection(string='Năm áp dụng', related='cong_them_id.year', store=True)
    cong_them = fields.Integer(u'Công tăng cuờng', default=0)
    block_id = fields.Many2one('hrm.blocks', string='Khối', related='employee_id.block_id', store=True )





