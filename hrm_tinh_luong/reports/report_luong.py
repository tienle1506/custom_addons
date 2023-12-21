# -*- coding:utf-8 -*-
from datetime import date, datetime
import calendar
from datetime import datetime, timedelta, time
from odoo import api, fields, models, _
from odoo.exceptions import Warning, ValidationError
from dateutil.relativedelta import relativedelta
import xlrd
import tempfile
import base64
import xlsxwriter
from io import BytesIO
from ...hrm_chamcong.models import style_excel_wb


def _default_date_from(self):
    return datetime.today().strftime('%Y-%m-01')


def _default_date_to(self):
    return (datetime.today() + relativedelta(months=+1, day=1, days=-1)).strftime('%Y-%m-%d')


def _col_to_string(n):
    string = ""
    n += 1
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string

class DATNBaseReport(models.TransientModel):
    _name = 'report.luong'
    _inherit = ['mail.thread']
    _description = u'Danh sách lương'

    department_id = fields.Many2one('hr.department', string='Đơn vị phòng ban')
    date_from = fields.Date(u'Từ ngày', required=True, default=_default_date_from, )
    date_to = fields.Date(u'Đến ngày', required=True, default=_default_date_to, track_visibility='always', )
    data = fields.Binary('File', readonly=True)
    name = fields.Char('Filename', readonly=True)
    state = fields.Selection((('choose', 'choose'),  # choose date
                              ('get', 'get'),  # get the file
                              ), default='choose')
    type_ids = fields.Many2many('datn.config.trocap.phucap', 'report_trocap_phucap_rel', 'report_id','trocap_phucap_id', string="Loại")

    @api.onchange('date_from')
    def _onchange_date_from(self):
        self.date_from = self.date_from.replace(day=1)

    @api.onchange('date_to')
    def _onchange_date_to(self):
        year = self.date_to.year
        month = self.date_to.month
        last_day = datetime(year, month, 1) + relativedelta(day=31)
        self.date_to = last_day.date()


    def export_excel(self):
        donvi_name = self.department_id.name

        file_name = u'Báo cáo lương từ ngày %s đến ngày %s'%(self.date_from, self.date_to)
        title = u'BÁO CÁO LƯƠNG THƯỜNG KỲ CÔNG TY TNHH HUCE VIỆT NAM'
        # TODO: Init báo cáo
        buf = BytesIO()
        wb = xlsxwriter.Workbook(buf, {'in_memory': True})
        wssheet = wb.add_worksheet('Biểu Ủy ban nhân dân, HĐND các cấp (2)')

        # TODO: Set độ rộng cột báo cáo
        # STT
        wssheet.set_column(0, 0, 5)
        for i in range(1, 16):
            if i == 2 or i == 3:
                wssheet.set_column(i, i, 24)
            else:
                wssheet.set_column(i, i, 12)
        wssheet.set_row(3,40)
        # wssheet.set_row(5, 50)
        # Set print fit to pages
        wssheet.fit_to_pages(1, 0)
        # Set print lan
        # wssheet.set_landscape()
        wssheet.set_portrait()
        # TODO: Tiêu đề báo cáo
        style_excel = style_excel_wb.get_style(wb)
        wssheet.merge_range(0, 0, 0, 2, u'Tổng công ty THHH HUCE Việt Nam', style_excel['style_12_left'])
        wssheet.merge_range(1, 0, 1, 2, u'Đơn vị báo cáo: %s'%(donvi_name), style_excel['style_12_left'])

        wssheet.merge_range(0, 3, 0, 15, title, style_excel['style_14_bold_center'])
        wssheet.merge_range(1, 3, 1, 15, u'Tính từ ngày %s đến ngày %s'%(self.date_from, self.date_to), style_excel['style_12_center_italic'])

        _row = 3
        wssheet.write(_row, 0, u"STT", style_excel['style_11_bold_center_border'])
        wssheet.write(_row, 1, u"Mã nhân viên", style_excel['style_11_bold_center_border'])
        wssheet.write(_row, 2, u"Họ và tên", style_excel['style_11_bold_center_border'])
        wssheet.write(_row, 3, u"Đơn vị phòng ban", style_excel['style_11_bold_center_border'])
        wssheet.write(_row, 4, u"Tổng lương", style_excel['style_11_bold_center_border'])
        wssheet.write(_row, 5, u"Bảo hiểm xã hội CP", style_excel['style_11_bold_center_border'])
        wssheet.write(_row, 6, u"Bảo hiểm y tế CP", style_excel['style_11_bold_center_border'])
        wssheet.write(_row, 7, u"Bảo hiểm tai nạn lao động CP", style_excel['style_11_bold_center_border'])
        wssheet.write(_row, 8, u"Bảo hiểm thât nghiệp CP", style_excel['style_11_bold_center_border'])
        wssheet.write(_row, 9, u"Công đoàn phí", style_excel['style_11_bold_center_border'])
        wssheet.write(_row, 10, u"Khấu trừ bảo hểm", style_excel['style_11_bold_center_border'])
        wssheet.write(_row, 11, u"Khấu trừ thuế", style_excel['style_11_bold_center_border'])
        wssheet.write(_row, 12, u"ST_BHXH_BHYT_KPCD", style_excel['style_11_bold_center_border'])
        wssheet.write(_row, 13, u"Thu nhập trước thuế", style_excel['style_11_bold_center_border'])
        wssheet.write(_row, 14, u"Thu nhập sau thuế", style_excel['style_11_bold_center_border'])
        wssheet.write(_row, 15, u"Thực lĩnh", style_excel['style_11_bold_center_border'])


        _row += 1
        for j in range(0, 16):
            wssheet.write(_row, j, '(%s)'%(j + 1), style_excel['style_11_center_border'])
        _row += 1

        SQL = ''
        SQL += ''' WITH bang_luong AS (
                    SELECT ltl.employee_id, sum(bl.tong_tien) AS tong_tien, bl.code 
                    FROM datn_luongthang_line ltl 
                    INNER JOIN datn_luongthang lt ON ltl.luongthang_id = lt.id
                    INNER JOIN datn_bangluong bl ON bl.bangluong_id = ltl.id 
                    LEFT JOIN hr_employee emp ON emp.id = ltl.employee_id
                    LEFT JOIN hr_department dp ON dp.id = emp.department_id 
                    WHERE lt.state = 'approved' AND lt.date_from >= '%s' 
                    AND lt.date_to <= '%s' AND dp.id IN (SELECT UNNEST(child_ids) FROM child_department WHERE parent_id IN (%s))
                    GROUP BY ltl.employee_id, bl.code
                )
                SELECT emp.name AS hoten, dp.name AS department_name, emp.employee_code,
                    json_object_agg(bl.code, bl.tong_tien) AS list_bang_luong
                FROM datn_luongthang_line ltl 
                INNER JOIN datn_luongthang lt ON ltl.luongthang_id = lt.id 
                LEFT JOIN hr_employee emp ON emp.id = ltl.employee_id
                LEFT JOIN hr_department dp ON dp.id = emp.department_id 
                LEFT JOIN bang_luong bl ON bl.employee_id = ltl.employee_id 
                WHERE lt.state = 'approved' AND lt.date_from >= '%s' 
                AND lt.date_to <= '%s' AND dp.id IN (SELECT UNNEST(child_ids) FROM child_department WHERE parent_id IN (%s))
                GROUP BY emp.id, dp.id, emp.name, dp.name, emp.employee_code;'''%(self.date_from, self.date_to, self.department_id.id,self.date_from, self.date_to, self.department_id.id)
        self.env.cr.execute(SQL)
        result = self.env.cr.dictfetchall()
        current_row = _row
        hang_dau = current_row + 1
        stt = 0
        if result:
            for i in range(len(result)):
                stt += 1
                wssheet.write(current_row, 0, stt, style_excel['style_11_center_border'])
                wssheet.write(current_row, 1, result[i].get('employee_code'), style_excel['style_11_center_border'])
                wssheet.write(current_row, 2, result[i].get('hoten'), style_excel['style_11_left_border'])
                wssheet.write(current_row, 3, result[i].get('department_name'), style_excel['style_11_left_border'])
                if result[i].get('list_bang_luong'):
                    bangluong = result[i].get('list_bang_luong')
                    wssheet.write(current_row, 4, bangluong.get('TLTT'), style_excel['style_10_right_border_money'])
                    wssheet.write(current_row, 5, bangluong.get('BHXH_CP'), style_excel['style_10_right_border_money'])
                    wssheet.write(current_row, 6, bangluong.get('BHYT_CP'), style_excel['style_10_right_border_money'])
                    wssheet.write(current_row, 7, bangluong.get('TNLD_CP'), style_excel['style_10_right_border_money'])
                    wssheet.write(current_row, 8, bangluong.get('BHTN_CP'), style_excel['style_10_right_border_money'])
                    wssheet.write(current_row, 9, bangluong.get('CDP_CP'), style_excel['style_10_right_border_money'])
                    wssheet.write(current_row, 10, bangluong.get('ST_BH'), style_excel['style_10_right_border_money'])
                    wssheet.write(current_row, 11, bangluong.get('KTT'), style_excel['style_10_right_border_money'])
                    wssheet.write(current_row, 12, bangluong.get('ST_BHXH_BHYT_KPCD'), style_excel['style_10_right_border_money'])
                    wssheet.write(current_row, 13, bangluong.get('TNTT'), style_excel['style_10_right_border_money'])
                    wssheet.write(current_row, 14, bangluong.get('TNST'), style_excel['style_10_right_border_money'])
                    wssheet.write(current_row, 15, bangluong.get('TTNTN'), style_excel['style_10_right_border_money'])
                    current_row += 1

        wssheet.merge_range(current_row, 0, current_row, 3, 'Tổng cộng', style_excel['style_12_bold_center_border'])
        wssheet.write(current_row, 4, u"=SUM(%s%s:%s%s)"%('E', hang_dau, 'E', current_row), style_excel['style_10_right_bold_border_money'])
        wssheet.write(current_row, 5, u"=SUM(%s%s:%s%s)"%('F', hang_dau, 'F', current_row), style_excel['style_10_right_bold_border_money'])
        wssheet.write(current_row, 6, u"=SUM(%s%s:%s%s)"%('G', hang_dau, 'G', current_row), style_excel['style_10_right_bold_border_money'])
        wssheet.write(current_row, 7, u"=SUM(%s%s:%s%s)"%('H', hang_dau, 'H', current_row), style_excel['style_10_right_bold_border_money'])
        wssheet.write(current_row, 8, u"=SUM(%s%s:%s%s)"%('I', hang_dau, 'I', current_row), style_excel['style_10_right_bold_border_money'])
        wssheet.write(current_row, 9, u"=SUM(%s%s:%s%s)"%('J', hang_dau, 'J', current_row), style_excel['style_10_right_bold_border_money'])
        wssheet.write(current_row, 10, u"=SUM(%s%s:%s%s)"%('K', hang_dau, 'K', current_row), style_excel['style_10_right_bold_border_money'])
        wssheet.write(current_row, 11, u"=SUM(%s%s:%s%s)"%('L', hang_dau, 'L', current_row), style_excel['style_10_right_bold_border_money'])
        wssheet.write(current_row, 12, u"=SUM(%s%s:%s%s)"%('M', hang_dau, 'M', current_row), style_excel['style_10_right_bold_border_money'])
        wssheet.write(current_row, 13, u"=SUM(%s%s:%s%s)"%('N', hang_dau, 'N', current_row), style_excel['style_10_right_bold_border_money'])
        wssheet.write(current_row, 14, u"=SUM(%s%s:%s%s)"%('O', hang_dau, 'O', current_row), style_excel['style_10_right_bold_border_money'])
        wssheet.write(current_row, 15, u"=SUM(%s%s:%s%s)"%('P', hang_dau, 'P', current_row), style_excel['style_10_right_bold_border_money'])
        #Todo Số lượng CBCCVC thuộc Ủy ban Nhân dân
        current_row = current_row + 2
        # TODO: Xuất footer báo cáo
        wssheet.merge_range(current_row + 5, 2, current_row + 5, 5, u'Người lập biểu', style_excel['style_12_bold_center'])
        wssheet.merge_range(current_row + 6, 5, current_row + 6, 5, u'(Ký, họ tên)', style_excel['style_12_center_italic'])

        wssheet.merge_range(current_row + 6, 7, current_row + 6, 10, u'Thủ trưởng đơn vị', style_excel['style_12_bold_center'])
        wssheet.merge_range(current_row + 7, 7, current_row + 7, 10, u'(Ký, họ tên)', style_excel['style_12_center_italic'])

        # TODO: Xuất ra File báo cáo
        wb.close()
        buf.seek(0)
        out = base64.encodestring(buf.getvalue())
        buf.close()
        self.write({'state': 'get', 'data': out, 'name': file_name + '.xlsx'})
        view = self.env.ref('hrm_tinh_luong.report_luong_view')
        view_id = view and view.id or False
        return {
            'name': _('Danh sách lương'),
            'type': 'ir.actions.act_window',
            'res_model': 'report.luong',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(view_id, 'form')],
            'target': 'new',
        }

    def export_excel_report_trocap_phucap(self):
        dada = self.get_trocap_phucap()
        donvi_name = self.department_id.name

        file_name = u'Báo cáo phụ cấp, trợ cấp từ ngày %s đến ngày %s' % (self.date_from, self.date_to)
        title = u'BÁO CÁO PHỤ CẤP, TRỢ CẤP THƯỜNG KỲ CÔNG TY TNHH HUCE VIỆT NAM'
        # TODO: Init báo cáo
        buf = BytesIO()
        wb = xlsxwriter.Workbook(buf, {'in_memory': True})
        wssheet = wb.add_worksheet('Biểu phụ cấp trợ cấp thường kỳ')

        # TODO: Set độ rộng cột báo cáo
        # STT
        wssheet.set_column(0, 0, 5)
        for i in range(1, 10):
            if i == 2 or i == 3:
                wssheet.set_column(i, i, 24)
            else:
                wssheet.set_column(i, i, 12)
        wssheet.set_row(3, 40)
        wssheet.set_row(0, 60)
        # wssheet.set_row(5, 50)
        # Set print fit to pages
        wssheet.fit_to_pages(1, 0)
        # Set print lan
        # wssheet.set_landscape()
        wssheet.set_portrait()

        if self.type_ids:
            len_type = len(self.type_ids)
            type_ids_list = self.type_ids.mapped('name')
        else:
            list_all = self.env['datn.config.trocap.phucap'].search([('trang_thai_ap_dung', '=', True)])
            if list_all:
                len_type = len(list_all)
                type_ids_list = list_all.mapped('name')
            else:
                len_type = 0
                type_ids_list = []

        row_tt = 4
        strlb = 'Tổng công ty THHH HUCE Việt Nam \nĐơn vị báo cáo: {}'.format(donvi_name)
        # TODO: Tiêu đề báo cáo
        style_excel = style_excel_wb.get_style(wb)
        wssheet.merge_range(0, 0, 0, 2, strlb, style_excel['style_12_left'])
        wssheet.merge_range(0, 3, 0, row_tt + len_type + 1, title, style_excel['style_14_bold_center'])
        wssheet.merge_range(1, 3, 1, row_tt + len_type + 1, u'Tính từ ngày %s đến ngày %s' % (self.date_from, self.date_to),
                            style_excel['style_12_center_italic'])

        _row = 3

        wssheet.write(_row, 0, u"STT", style_excel['style_11_bold_center_border'])
        wssheet.write(_row, 1, u"Mã nhân viên", style_excel['style_11_bold_center_border'])
        wssheet.write(_row, 2, u"Họ và tên", style_excel['style_11_bold_center_border'])
        wssheet.write(_row, 3, u"Đơn vị phòng ban", style_excel['style_11_bold_center_border'])
        if len_type > 0:
            for i in range(0, len_type):
                wssheet.write(_row, row_tt + i, str(type_ids_list[i]), style_excel['style_11_bold_center_border'])

        wssheet.write(_row, row_tt + len_type, u"Tổng cộng", style_excel['style_11_bold_center_border'])
        wssheet.write(_row, row_tt + len_type + 1, u"Chú thích", style_excel['style_11_bold_center_border'])

        _row += 1
        for j in range(0, row_tt + len_type + 2):
            wssheet.write(_row, j, '(%s)' % (j + 1), style_excel['style_11_center_border'])
        _row += 1
        current_row = _row
        employees = self.get_trocap_phucap()
        if employees:
            for i in range(0, len(employees)):
                wssheet.write(current_row, 0, '%s' % (j + 1), style_excel['style_11_center_border'])
                wssheet.write(current_row, 1, str(employees[i].get('code')), style_excel['style_11_center_border'])
                wssheet.write(current_row, 2, str(employees[i].get('hoten')), style_excel['style_11_left_border'])
                wssheet.write(current_row, 3, str(employees[i].get('department_name')), style_excel['style_11_left_border'])
                if len_type > 0:
                    for j in range(0, len_type):
                        valttpc = 0
                        listttpc = employees[i].get('list_ttpc') if employees[i].get('list_ttpc') else {}
                        for ttpc in listttpc:
                            if ttpc['type'] == str(type_ids_list[j]):
                                valttpc = ttpc['tongtien']
                        wssheet.write(current_row, row_tt + j, valttpc, style_excel['style_10_right_border_money'])

                if not len_type or len_type == 0:
                    str_sum = ''
                else:
                    str_sum = '=SUM(%s%s:%s%s)'%(_col_to_string(row_tt), current_row + 1, _col_to_string(row_tt + len_type - 1), current_row + 1)
                wssheet.write(current_row, row_tt + len_type, str_sum, style_excel['style_10_right_border_money'])
                wssheet.write(current_row, row_tt + len_type + 1, '', style_excel['style_11_bold_center_border'])
                current_row += 1

        # Todo Số lượng CBCCVC thuộc Ủy ban Nhân dân
        current_row = current_row + 2
        # TODO: Xuất footer báo cáo
        wssheet.merge_range(current_row , 1, current_row, 2, u'Người lập biểu', style_excel['style_12_bold_center'])
        wssheet.merge_range(current_row + 1, 1, current_row + 1, 2, u'(Ký tên, ghi rõ họ tên)', style_excel['style_12_center_italic'])

        wssheet.merge_range(current_row + 1, row_tt + len_type - 1, current_row + 1, row_tt + len_type + 1, u'Thủ trưởng đơn vị', style_excel['style_12_bold_center'])
        wssheet.merge_range(current_row + 2, row_tt + len_type - 1, current_row + 2, row_tt + len_type + 1, u'(Ký tên, đóng dấu)', style_excel['style_12_center_italic'])

        # TODO: Xuất ra File báo cáo
        wb.close()
        buf.seek(0)
        out = base64.encodestring(buf.getvalue())
        buf.close()
        self.write({'state': 'get', 'data': out, 'name': file_name + '.xlsx'})
        view = self.env.ref('hrm_tinh_luong.report_trocap_phucap_view')
        view_id = view and view.id or False
        return {
            'name': _('Danh sách lương'),
            'type': 'ir.actions.act_window',
            'res_model': 'report.luong',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(view_id, 'form')],
            'target': 'new',
        }

    def get_trocap_phucap(self):
        string_type = 'WHERE'
        if not self.type_ids:
            lists = self.env['datn.config.trocap.phucap'].search([('trang_thai_ap_dung', '=', True)])
            if lists:
                for i in range(0, len(lists)):
                    if i == 0:
                        string_type += ' ctt.id = %s'%(lists[i].id)
                    else:
                        string_type += ' OR ctt.id = %s' % (lists[i].id)
            else:
                string_type += ' id = 0'

        else:
            i = 0
            for ls in self.type_ids:
                if i == 0:
                    string_type += ' ctt.id = %s' % (ls.id)
                else:
                    string_type += ' OR ctt.id = %s' % (ls.id)

                i = i+1
        SQL = ''
        SQL += '''WITH s AS (SELECT emp.employee_code AS code, emp.id as employee_id, emp.name AS hoten, dp.name AS department_name, SUM(muc_huong) AS tongtien, ctt.name AS type
                from datn_trocap_phucap_line ttl INNER JOIN datn_trocap_phucap tt ON ttl.trocap_phucap_id = tt.id
                INNER JOIN hr_employee emp ON ttl.employee_id = emp.id
                INNER JOIN hr_department dp ON dp.id = emp.department_id
                INNER JOIN datn_config_trocap_phucap ctt ON ctt.id = tt.type_id
                %s AND ngay_chi_tra <= '%s' AND ngay_chi_tra >= '%s' AND emp.department_id = ANY
                      (ARRAY(SELECT child_ids FROM child_department WHERE parent_id = %s)) AND tt.state='confirmed'
                GROUP BY emp.id, dp.id, ctt.id)

                select JSON_AGG(
                json_build_object(
                'tongtien', s.tongtien,
                'type', s.type
                )) as list_ttpc, hoten, department_name, code from s
                GROUP BY s.code, s.employee_id, s.hoten, s.department_name
                '''%(string_type, self.date_to, self.date_from, self.department_id.id)
        self.env.cr.execute(SQL)
        datas = self.env.cr.dictfetchall()
        if not datas:
            datas = []

        return  datas