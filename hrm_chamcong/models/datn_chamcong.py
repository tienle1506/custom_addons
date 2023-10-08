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
    date_from = fields.Date(u'Từ ngày', required=True, default=_default_date_from,
                            states={'confirmed': [('readonly', True)]})
    date_to = fields.Date(u'Đến ngày', required=True, default=_default_date_to, track_visibility='always', )
    department_id = fields.Many2one('hrm.departments', string=u'Đơn vị/Phòng ban', required=True,
                                    states={'confirmed': [('readonly', True)]})
    item_ids = fields.One2many('datn.hr.chamcong.line', 'chamcong_id', states={'confirmed': [('readonly', True)]}, track_visibility='always',)
    state = fields.Selection([('draft', u'Soạn thảo'), ('confirmed', u'Xác nhận')],
                             string=u'Trạng thái', default='draft', track_visibility='always')
    day_of_month = fields.Integer(string="Số ngày trong tháng")
    # Lưu dữ liệu các bản ghi chấm công khi onchange phục vụ chức năng export
    backup = fields.Text(string="")

    month_year_chuky = fields.Integer(string="Chu kỳ chấm công", required=True, index=True,
                                      default=datetime.now().year * 100 + datetime.now().month, )

    # Import
    datn_file = fields.Binary(u'Đường dẫn tập tin', filters="*.xls,*.xlsx")
    file_name = fields.Char(u'Tên tệp tin')
    is_import = fields.Boolean(u'Import dữ liệu')

    is_show_ngay29 = fields.Boolean(string=u"Có ngày 29", compute='_compute_date')
    is_show_ngay30 = fields.Boolean(string=u"Có ngày 30", compute='_compute_date')
    is_show_ngay31 = fields.Boolean(string=u"Có ngày 31", compute='_compute_date')

    day_reload = fields.Selection([(str(num), num) for num in range(1, 32)], string=u'Ngày', required=False)

    # Khai báo cho báo cáo
    TYPE_CONGCHUAN = 'CONGCHUAN'
    TYPE_NGAYCONG = 'NGAYCONG'
    MA_DON_VI_KTM = '0000001'
    CONST_KHCC_CTT = 'CTT'
    CONST_KHCC_CP = 'CP'
    CONST_KHCC_NCC = 'NCC'
    CONST_KHCC_CCD = 'CCD'
    CONST_KHCC_CH = 'CH'
    CONST_KHCC_CBHXH = 'CBHXH'
    CONST_KHCC_CAC = 'CAC'
    CONST_KHCC_CNL = 'CNL'
    CONST_KHCC_CNN = 'CNN'
    CONST_KHCC_CNB = 'CNB'
    CONST_KHCC_NKL = 'NKL'
    CONST_KHCC_NVKL = 'NVKL'
    CONST_KHCC_CCDe = 'CCDe'
    CONST_TG_L_N = 'TG_L_N'
    CONST_TG_L_D = 'TG_L_D'
    CONST_TG_N_N = 'TG_N_N'
    CONST_TG_N_D = 'TG_N_D'
    CONST_KHCC_NC = 'NC'

    time_lock_before = fields.Datetime('Time Lock before', compute='_compute_time_lock')
    time_lock_after = fields.Datetime('Time Lock After  ', compute='_compute_time_lock')
    is_active_ngay1 = fields.Boolean(string=u'Sửa ngày 1', compute='_compute_time_lock')
    is_active_ngay2 = fields.Boolean(string=u'Sửa ngày 2', compute='_compute_time_lock')
    is_active_ngay3 = fields.Boolean(string=u'Sửa ngày 3', compute='_compute_time_lock')
    is_active_ngay4 = fields.Boolean(string=u'Sửa ngày 4', compute='_compute_time_lock')
    is_active_ngay5 = fields.Boolean(string=u'Sửa ngày 5', compute='_compute_time_lock')
    is_active_ngay6 = fields.Boolean(string=u'Sửa ngày 6', compute='_compute_time_lock')
    is_active_ngay7 = fields.Boolean(string=u'Sửa ngày 7', compute='_compute_time_lock')
    is_active_ngay8 = fields.Boolean(string=u'Sửa ngày 8', compute='_compute_time_lock')
    is_active_ngay9 = fields.Boolean(string=u'Sửa ngày 9', compute='_compute_time_lock')
    is_active_ngay10 = fields.Boolean(string=u'Sửa ngày 10', compute='_compute_time_lock')
    is_active_ngay11 = fields.Boolean(string=u'Sửa ngày 11', compute='_compute_time_lock')
    is_active_ngay12 = fields.Boolean(string=u'Sửa ngày 12', compute='_compute_time_lock')
    is_active_ngay13 = fields.Boolean(string=u'Sửa ngày 13', compute='_compute_time_lock')
    is_active_ngay14 = fields.Boolean(string=u'Sửa ngày 14', compute='_compute_time_lock')
    is_active_ngay15 = fields.Boolean(string=u'Sửa ngày 15', compute='_compute_time_lock')
    is_active_ngay16 = fields.Boolean(string=u'Sửa ngày 16', compute='_compute_time_lock')
    is_active_ngay17 = fields.Boolean(string=u'Sửa ngày 17', compute='_compute_time_lock')
    is_active_ngay18 = fields.Boolean(string=u'Sửa ngày 18', compute='_compute_time_lock')
    is_active_ngay19 = fields.Boolean(string=u'Sửa ngày 19', compute='_compute_time_lock')
    is_active_ngay20 = fields.Boolean(string=u'Sửa ngày 20', compute='_compute_time_lock')
    is_active_ngay21 = fields.Boolean(string=u'Sửa ngày 21', compute='_compute_time_lock')
    is_active_ngay22 = fields.Boolean(string=u'Sửa ngày 22', compute='_compute_time_lock')
    is_active_ngay23 = fields.Boolean(string=u'Sửa ngày 23', compute='_compute_time_lock')
    is_active_ngay24 = fields.Boolean(string=u'Sửa ngày 24', compute='_compute_time_lock')
    is_active_ngay25 = fields.Boolean(string=u'Sửa ngày 25', compute='_compute_time_lock')
    is_active_ngay26 = fields.Boolean(string=u'Sửa ngày 26', compute='_compute_time_lock')
    is_active_ngay27 = fields.Boolean(string=u'Sửa ngày 27', compute='_compute_time_lock')
    is_active_ngay28 = fields.Boolean(string=u'Sửa ngày 28', compute='_compute_time_lock')
    is_active_ngay29 = fields.Boolean(string=u'Sửa ngày 29', compute='_compute_time_lock')
    is_active_ngay30 = fields.Boolean(string=u'Sửa ngày 30', compute='_compute_time_lock')
    is_active_ngay31 = fields.Boolean(string=u'Sửa ngày 31', compute='_compute_time_lock')

    @api.constrains('file_name')
    def _check_filename(self):
        if self.vnpt_file:
            if not self.file_name:
                raise ValidationError(_(u"Không có tập tin!"))
            else:
                # Check the file's extension
                tmp = self.file_name.split('.')
                ext = tmp[len(tmp) - 1]
                if ext != 'xls' and ext != 'xlsx':
                    raise ValidationError(_(u"Tệp tin tải lên phải là định dạng file excel. Vui lòng xem lại."))



    @api.onchange('month_year_chuky')
    def _onchange_date(self):
        res = calendar.monthrange(int(self.month_year_chuky / 100), int(self.month_year_chuky % 100))[1]
        chu_ky = str(self.month_year_chuky)
        self.date_from = chu_ky[:4] + '-' + chu_ky[-2:] + '-01'
        self.date_to = chu_ky[:4] + '-' + chu_ky[-2:] + '-' + str(res)

    @api.depends('month_year_chuky')
    def _compute_date(self):
        if self.month_year_chuky == 0:
            return
        res = calendar.monthrange(int(self.month_year_chuky / 100), int(self.month_year_chuky % 100))[1]
        self.is_show_ngay29 = False
        self.is_show_ngay30 = False
        self.is_show_ngay31 = False
        if res == 29:
            self.is_show_ngay29 = True
        elif res == 30:
            self.is_show_ngay29 = True
            self.is_show_ngay30 = True
        elif res == 31:
            self.is_show_ngay29 = True
            self.is_show_ngay30 = True
            self.is_show_ngay31 = True

    @api.depends('department_id')
    def _compute_time_lock(self):
        self.is_active_ngay1 = True
        self.is_active_ngay2 = True
        self.is_active_ngay3 = True
        self.is_active_ngay4 = True
        self.is_active_ngay5 = True
        self.is_active_ngay6 = True
        self.is_active_ngay7 = True
        self.is_active_ngay8 = True
        self.is_active_ngay9 = True
        self.is_active_ngay10 = True
        self.is_active_ngay11 = True
        self.is_active_ngay12 = True
        self.is_active_ngay13 = True
        self.is_active_ngay14 = True
        self.is_active_ngay15 = True
        self.is_active_ngay16 = True
        self.is_active_ngay17 = True
        self.is_active_ngay18 = True
        self.is_active_ngay19 = True
        self.is_active_ngay20 = True
        self.is_active_ngay21 = True
        self.is_active_ngay22 = True
        self.is_active_ngay23 = True
        self.is_active_ngay24 = True
        self.is_active_ngay25 = True
        self.is_active_ngay26 = True
        self.is_active_ngay27 = True
        self.is_active_ngay28 = True
        self.is_active_ngay29 = True
        self.is_active_ngay30 = True
        self.is_active_ngay31 = True
        if not self.department_id:
            return
        config = self.env['hr.work.lock.config'].get_config_from_department_id(self.department_id.id, 'day')
        if not config:
            return
        self.time_lock_before = datetime.utcnow().replace(hour=int(config.hour_before), minute=0,
                                                          second=0) - relativedelta(days=config.day_before, hours=7)
        self.time_lock_after = datetime.utcnow().replace(hour=int(config.hour_after), minute=0,
                                                         second=0) + relativedelta(days=config.day_after, hours=-7)
        _month = self.month_year_chuky % 100
        _year = self.month_year_chuky // 100
        if self.time_lock_before.date() == datetime.utcnow().date():
            config.type_hour_before = 'lock_after'
        if config.type_hour_before == 'lock_after':
            for x in range(1, 29):
                if self.time_lock_before < datetime.utcnow().replace(day=x, month=_month, year=_year) < self.time_lock_after:
                    self['is_active_ngay' + str(x)] = True
                else:
                    self['is_active_ngay' + str(x)] = False
            for x in range(29, 32):
                if self['is_show_ngay' + str(x)] == True and datetime.utcnow().replace(day=x, month=_month, year=_year) + relativedelta(days=x) > self.time_lock_before \
                        and datetime.utcnow().replace(day=1, month=_month, year=_year) + relativedelta(days=x) < self.time_lock_after:
                    self['is_active_ngay' + str(x)] = True
                else:
                    self['is_active_ngay' + str(x)] = False
        else:
            for x in range(1, 29):
                if datetime.utcnow().replace(day=x, month=_month, year=_year) <= self.time_lock_before \
                        and datetime.utcnow().replace(day=x, month=_month, year=_year).date() == self.time_lock_before.date():
                    self['is_active_ngay' + str(x)] = True
                elif datetime.utcnow().replace(day=x, month=_month, year=_year) > self.time_lock_before \
                        and datetime.utcnow().replace(day=x, month=_month, year=_year).date() == self.time_lock_before.date():
                    self['is_active_ngay' + str(x)] = False
                elif self.time_lock_before < datetime.utcnow().replace(day=x, month=_month, year=_year) < self.time_lock_after:
                    self['is_active_ngay' + str(x)] = True
                else:
                    self['is_active_ngay' + str(x)] = False
            for x in range(29, 32):
                if self['is_show_ngay' + str(x)] == True and datetime.utcnow().replace(day=x, month=_month, year=_year) + relativedelta(days=x) <= self.time_lock_before \
                        and (datetime.utcnow().replace(day=x, month=_month, year=_year) + relativedelta(days=x)).date() == self.time_lock_before.date():
                    self['is_active_ngay' + str(x)] = True
                elif self['is_show_ngay' + str(x)] == True and datetime.utcnow().replace(day=x, month=_month, year=_year) + relativedelta(days=x) > self.time_lock_before \
                        and (datetime.utcnow().replace(day=x, month=_month, year=_year) + relativedelta(days=x)).date() == self.time_lock_before.date():
                    self['is_active_ngay' + str(x)] = False
                elif self['is_show_ngay' + str(x)] == True and self.time_lock_before < datetime.utcnow().replace(day=x, month=_month, year=_year) < self.time_lock_after:
                    self['is_active_ngay' + str(x)] = True
                else:
                    self['is_active_ngay' + str(x)] = False

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
    cong_hoc = fields.Float(string=u'Công học', digits=_get_decimal_precision("Timesheets"))
    cong_bhxh = fields.Float(string=u'Công BHXH', digits=_get_decimal_precision("Timesheets"))
    cong_an_ca = fields.Float(string=u'Công ăn ca', digits=_get_decimal_precision("Timesheets"))
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

    tg_t_n = fields.Float(string=u'Thêm giờ ngày thường, ban ngày', digits=_get_decimal_precision("Timesheets"))
    tg_t_d = fields.Float(string=u'Thêm giờ ngày thường, ban đêm', digits=_get_decimal_precision("Timesheets"))
    tg_l_n = fields.Float(string=u'Thêm giờ ngày lễ, ban ngày', digits=_get_decimal_precision("Timesheets"))
    tg_l_d = fields.Float(string=u'Thêm giờ ngày lễ, ban đêm', digits=_get_decimal_precision("Timesheets"))
    tg_n_n = fields.Float(string=u'Thêm giờ ngày nghỉ, ban ngày', digits=_get_decimal_precision("Timesheets"))
    tg_n_d = fields.Float(string=u'Thêm giờ ngày nghỉ, ban đêm', digits=_get_decimal_precision("Timesheets"))

    department_id = fields.Many2one('hrm.departments', string=u'Đơn vị/Phòng ban')

    # Ngay cong trong thang
    stt = fields.Integer(string=u"STT", readonly=True)
    ngay1 = fields.Datetime(string=u"01", range=True)
    ngay2 = fields.Datetime(string=u"02", range=True)
    ngay3 = fields.Datetime(string=u"03", range=True)
    ngay4 = fields.Datetime(string=u"04", range=True)
    ngay5 = fields.Datetime(string=u"05", range=True)
    ngay6 = fields.Datetime(string=u"06", range=True)
    ngay7 = fields.Datetime(string=u"07", range=True)
    ngay8 = fields.Datetime(string=u"08", range=True)
    ngay9 = fields.Datetime(string=u"09", range=True)
    ngay10 = fields.Datetime(string=u"10", range=True)
    ngay11 = fields.Datetime(string=u"11", range=True)
    ngay12 = fields.Datetime(string=u"12", range=True)
    ngay13 = fields.Datetime(string=u"13", range=True)
    ngay14 = fields.Datetime(string=u"14", range=True)
    ngay15 = fields.Datetime(string=u"15", range=True)
    ngay16 = fields.Datetime(string=u"16", range=True)
    ngay17 = fields.Datetime(string=u"17", range=True)
    ngay18 = fields.Datetime(string=u"18", range=True)
    ngay19 = fields.Datetime(string=u"19", range=True)
    ngay20 = fields.Datetime(string=u"20", range=True)
    ngay21 = fields.Datetime(string=u"21", range=True)
    ngay22 = fields.Datetime(string=u"22", range=True)
    ngay23 = fields.Datetime(string=u"23", range=True)
    ngay24 = fields.Datetime(string=u"24", range=True)
    ngay25 = fields.Datetime(string=u"25", range=True)
    ngay26 = fields.Datetime(string=u"26", range=True)
    ngay27 = fields.Datetime(string=u"27", range=True)
    ngay28 = fields.Datetime(string=u"28", range=True)
    ngay29 = fields.Datetime(string=u"29", range=True)
    ngay30 = fields.Datetime(string=u"30", range=True)
    ngay31 = fields.Datetime(string=u"31", range=True)
    day_of_month = fields.Integer(string=u"Số ngày trong tháng")
    error_text = fields.Char(string=u"Error", required=False)