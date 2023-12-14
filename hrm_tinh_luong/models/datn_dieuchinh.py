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
from ...hrm_chamcong.models import style_excel_wb
from ...hrm.models import constraint

class DATNDieuChinh(models.Model):
    _name = 'datn.dieuchinh'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = u'Phiếu điều chỉnh'
    _order = "ngay_tao DESC"

    data = fields.Binary('File', readonly=True)
    department_id = fields.Many2one('hr.department',ondelete='cascade', string='Đơn vị/Phòng ban', required=True,
                    tracking=True)
    type = fields.Selection([('luong', u'Điều chỉnh lương')],
                             string=u'Loại điều chỉnh', default='luong', track_visibility='always')
    ngay_tao = fields.Date(u'Ngày tạo', widget='date', format='%Y-%m-%d', default=fields.Date.today)
    item_ids = fields.One2many('datn.dieuchinh.line', string='Items', inverse_name='dieuchinh_id',
                               track_visibility='always')

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
                    ngay_huong = str(sheet.cell_value(row, 4)).strip() if sheet.cell_value(row, 3) else ''
                    if ngay_huong:
                        # Chuyển đổi chuỗi datetime thành đối tượng datetime
                        ngay_huong = datetime.strptime(ngay_huong, '%d-%m-%Y')
                    else:
                        raise ValidationError(f'Ngày hưởng dòng {row} đang trống')
                except ValueError:
                    raise ValidationError(f'Không đúng định dạng của DateTime %d-%m-%Ydòng {row}')

                muc_huong = sheet.cell_value(row, 3)
                if not muc_huong:
                    raise ValidationError(f'Mưc hưởng ở dong {row} đang trống')

                if employee.id:
                    lines.append((0, 0, {
                        'employee_id': employee.id,
                        'muc_huong': muc_huong,
                        'ngay_huong': ngay_huong,
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
            worksheet = workbook.add_worksheet('Danh sách điều chỉnh')
            worksheet.set_row(4, 30)

            worksheet.merge_range(0, 0, 0, 2, 'Đơn vị/ phòng ban : %s'%(self.department_id.name), style_excel['style_12_bold_left'])
            worksheet.merge_range(2, 0, 2, 6, 'Danh Sách nhân sự điều chỉnh', style_title)

            worksheet.merge_range(4, 0, 5, 0, 'STT', style_1)
            worksheet.merge_range(4, 1, 5, 1, 'Mã Nhân Viên', style_1_require)
            worksheet.merge_range(4, 2, 5, 2, 'Tên Nhân Viên', style_1_require)
            worksheet.merge_range(4, 3, 5, 3, 'Mức điều chỉnh', style_1)
            worksheet.merge_range(4, 4, 5, 4, 'Ngày hưởng (dd-mm-YYYY)', style_1)
            worksheet.merge_range(4, 5, 5, 5, 'Note', style_1)

            for i in range(1, 6):
                worksheet.set_column(i, 4, 20)

            # Danh mục đơn vị đào tạo
            SQL = ''
            # Lấy chức vụ của người tạo đơn đăng ký nghỉ
            SQL += '''SELECT id, employee_code, name  FROM hr_employee where department_id in (SELECT UNNEST(child_ids) FROM child_department WHERE parent_id in (%s))''' % (self.department_id.id)

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
                lst_employees.append("'%s"%(item['employee_code']))
                worksheet_object.write(i, 0, i, style_1)
                worksheet_object.write(i, 1, u"%s"%(item['employee_code']), style_1_left)
                worksheet_object.write(i, 2, item['name'], style_1_left)
                i = i + 1

            worksheet.data_validation('B6:B50', {'validate': 'list', 'source': lst_employees})
            namefile = 'Mau_import_dieu_chinh'
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


class DATNHrDieuChinhLine(models.Model):
    _name = 'datn.dieuchinh.line'
    _inherit = ['mail.thread']
    _description = u'Danh sách nhân sự hưởng điều chỉnh'
    _order = "ngay_huong DESC"
    _res_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string=u'Nhân viên', ondelete='cascade')
    dieuchinh_id = fields.Many2one('datn.dieuchinh', string=u'Phiếu điều chỉnh', ondelete='cascade', required=True)
    note = fields.Text(string='Ghi chú', compute='_compute_date', store=True)
    muc_huong = fields.Integer(string='Mức hưởng')
    ngay_huong = fields.Date(string='Ngày hưởng', widget='date', format='%m-%d-%Y')
    ngay_hieu_luc = fields.Date(string='Ngày hiệu lực', widget='date', format='%m-%d-%Y', compute='_compute_dieuchinh_ngayhieuluc', store=True)
    ngay_ket_thuc = fields.Date(string='Ngày kết thúc', widget='date', format='%m-%d-%Y', compute='_compute_dieuchinh_ngayhieuluc', store=True)
    type = fields.Selection([('luong', u'Điều chỉnh lương')],
                            string=u'Loại điều chỉnh', default='luong', track_visibility='always')
    def read(self, fields=None, load='_classic_read'):
        self.check_access_rule('read')
        return super(DATNHrDieuChinhLine, self).read(fields, load=load)

    def search(self, args, offset=0, limit=None, order=None, count=False):
        domain = []
        return super(DATNHrDieuChinhLine, self).search(domain + args, offset, limit, order, count=count)

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        emp_domain = self.check_employee_view()
        return super(DATNHrDieuChinhLine, self)._name_search(name, args=args + emp_domain, operator=operator,
                                                                  limit=limit)


    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        emp_domain = self.check_employee_view()
        return super(DATNHrDieuChinhLine, self).search_read(domain=domain + emp_domain, fields=fields,
                                                                  offset=offset, limit=limit, order=order)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        emp_domain = self.check_employee_view()
        return super(DATNHrDieuChinhLine, self).read_group(domain + emp_domain, fields, groupby, offset=offset,
                                                                 limit=limit, orderby=orderby, lazy=lazy)
    def check_employee_view(self):
        context = self.env.context or {}
        emp_domain = []
        user = self.env.user
        employee_id = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
        if context.get('view_from_action', False):
            emp_domain = [('employee_id', '=', employee_id.id)]
        return emp_domain

    @api.depends('ngay_huong')
    def _compute_dieuchinh_ngayhieuluc(self):
        for record in self:
            if record.ngay_huong:
                employees = self.env['datn.dieuchinh.line'].search([('employee_id', '=' , record.employee_id.id)], order="ngay_huong DESC")
                if employees and len(employees) > 1:
                    if record.ngay_huong > datetime.now().date():
                        record.ngay_hieu_luc = record.ngay_huong.replace(day=1)
                        ngay_cuoi_cung_thang_truoc = record.ngay_huong.replace(day=1) - timedelta(days=1)
                        employees[1].write({
                            'ngay_ket_thuc': ngay_cuoi_cung_thang_truoc
                        })
                    else:
                        if record.ngay_huong.day > 15:
                            thang_sau = record.ngay_huong.month + 1
                            nam_sau = record.ngay_huong.year

                            if thang_sau > 12:
                                thang_sau = 1
                                nam_sau = record.ngay_huong.year + 1

                            record.ngay_hieu_luc = datetime(nam_sau, thang_sau, 1).date()
                            ngay_cuoi_cung_thang_truoc = record.ngay_hieu_luc - timedelta(days=1)
                            employees[1].write({
                                'ngay_ket_thuc': ngay_cuoi_cung_thang_truoc
                            })
                        else:
                            record.ngay_hieu_luc = record.ngay_huong.replace(day=1)
                            ngay_cuoi_cung_thang_truoc = record.ngay_hieu_luc - timedelta(days=1)
                            employees[1].write({
                                'ngay_ket_thuc': ngay_cuoi_cung_thang_truoc
                            })
                else:
                    record.ngay_hieu_luc = record.ngay_huong.replace(day=1)


