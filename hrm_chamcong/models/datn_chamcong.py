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


class DATNHrChamCong(models.Model):
    _name = 'datn.hr.chamcong'
    _inherit = ['mail.thread']
    _description = u'Chấm công theo ca'
    _order = "month_year_chuky DESC"

    def _default_date_from(self):
        return datetime.today().strftime('%Y-%m-01')

    def _default_date_to(self):
        return (datetime.today() + relativedelta(months=+1, day=1, days=-1)).strftime('%Y-%m-%d')


    name = fields.Char(string=u'Bảng chấm công tháng', size=128, track_visibility='always', )
    date_from = fields.Date(u'Từ ngày', required=True, default=_default_date_from,)
    date_to = fields.Date(u'Đến ngày', required=True, default=_default_date_to, track_visibility='always', )
    block_id = fields.Many2one('hrm.blocks', string=u'Khối', required=True)
    item_ids = fields.One2many('datn.hr.chamcong.line', 'chamcong_id', track_visibility='always',)
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

    employee_id = fields.Many2one('hrm.employee.profile', string=u'Nhân sự', ondelete='cascade')
    chamcong_id = fields.Many2one('datn.hr.chamcong', string=u'Bảng chấm công', ondelete='cascade', required=True)
    # playslip_id = fields.Many2one('hr.payslip', string='Payslip', ondelete='cascade')

    ngay_cong = fields.Float(string=u'Ngày công', digits=_get_decimal_precision("Timesheets"))
    cong_phep = fields.Float(string=u'Công phép', digits=_get_decimal_precision("Timesheets"))

    cong_bhxh = fields.Float(string=u'Công BHXH', digits=_get_decimal_precision("Timesheets"))
    cong_ngay_le = fields.Float(string=u'Công ngày lễ', digits=_get_decimal_precision("Timesheets"))
    cong_ngay_nghi = fields.Float(string=u'Công ngày nghỉ', digits=_get_decimal_precision("Timesheets"))
    cong_nghi_bu = fields.Float(string=u'Công nghỉ bù', digits=_get_decimal_precision("Timesheets"))
    nghi_khong_luong = fields.Float(string=u'Nghỉ không lương', digits=_get_decimal_precision("Timesheets"))
    nghi_khong_phep = fields.Float(string=u'Nghỉ vô kỷ luật', digits=_get_decimal_precision("Timesheets"))
    cong_chuan = fields.Float(string=u'Công chuẩn', digits=_get_decimal_precision("Timesheets"))
    cong_thuc_te = fields.Float(string=u'Công thực tế', digits=_get_decimal_precision("Timesheets"))
    cong_che_do = fields.Float(string=u'Công chế độ', digits=_get_decimal_precision("Timesheets"))
    tong_cong = fields.Float(string=u'Tổng công', digits=_get_decimal_precision("Timesheets"))

    # end
    block_id = fields.Many2one('hrm.blocks', string=u'khối')

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