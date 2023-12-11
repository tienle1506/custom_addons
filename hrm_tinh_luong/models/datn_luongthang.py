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

class DATNHrLuongThang(models.Model):
    _name = 'datn.luongthang'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = u'Chấm công theo tháng'
    _order = "date_from DESC"

    def _default_date_from(self):
        return datetime.today().strftime('%Y-%m-01')

    def _default_date_to(self):
        return (datetime.today() + relativedelta(months=+1, day=1, days=-1)).strftime('%Y-%m-%d')


    name = fields.Char(string=u'Bảng tính lương tháng', size=128, track_visibility='always', )
    date_from = fields.Date(u'Từ ngày', required=True, default=_default_date_from,)
    date_to = fields.Date(u'Đến ngày', required=True, default=_default_date_to, track_visibility='always', )
    department_id = fields.Many2one('hr.department',ondelete='cascade', string=u'Đơn vị/ Phòng ban', required=True)
    item_ids = fields.One2many('datn.luongthang.line', string='Danh sách nhân viên', inverse_name='luongthang_id',track_visibility='always')
    nguoi_duyet = fields.Many2many('hr.employee', 'employee_duyet_luong_rel', 'luongthang_id', 'employee_id', string="Người duyệt")
    state = fields.Selection([('draft', u'Soạn thảo'), ('confirmed', u'Chờ phê duệt'), ('approved', u'Phê duyệt'),
                              ('refused', u'Từ chối')],
                             string=u'Trạng thái', default='draft', track_visibility='always')
    ngay_chi_tra = fields.Date(u'Ngày chi trả', required=True)

    def action_draft(self):
        self.state = 'draft'
    def action_send_approve(self):
        nguoi_duyet = []
        for emp in self.nguoi_duyet:
            if emp.personal_email:
                nguoi_duyet.append(emp.personal_email.strip())
        header = '''Thông báo phê duyệt đơn tăng ca của %s''' % (self.employee_id.name)
        content = u'Nhân viên %s tạo đơn tăng ca \nLý do: %s \nSố giờ tăng ca:%s\nTừ ngày: %s - đến ngày: %s \nTrang web: http://localhost:8088/web' % (
        str(self.employee_id.name), str(self.ly_do), str(self.so_gio_tang_ca),
        self.date_from.strftime('%d/%m/%Y'), self.date_to.strftime('%d/%m/%Y'))
        if nguoi_duyet and len(nguoi_duyet) > 0:
            self.env['my.mail.sender'].send_mail_to_customer(nguoi_duyet, header, content)
        self.state = 'confirmed'

    def action_refuse(self):
        self.state = 'refused'

    def action_approve(self):
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
    def action_loaddata(self):
        a=b



    @api.onchange('date_from', 'department_id')
    def onchange_name(self):
        name = 'Bảng tính lương tháng %s năm %s Đơn vị/ phòng ban %s'%(str(self.date_from.month), str(self.date_from.year), self.department_id.name)
        self.name = name

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


class DATNHrLuongThangLine(models.Model):
    _name = 'datn.luongthang.line'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = u'Danh sách nhân viên'
    _order = "date_from DESC"

    employee_id = fields.Many2one('hr.employee', string="Nhân viên", ondelete='cascade')
    department_id = fields.Many2one('hr.department', string="Đơn vị/ phòng ban", ondelete='cascade',
                                    related='employee_id.department_id', store=True)
    luongthang_id = fields.Many2one('datn.luongthang', string="Danh sách nhân sự", ondelete='cascade')
    date_from = fields.Date(u'Từ ngày', related='luongthang_id.date_from', stored=True)
    date_to = fields.Date(u'Đến ngày', related='luongthang_id.date_to', stored=True)
    tong_tien = fields.Integer(u'Tổng tiền',)
    item_ids = fields.One2many('datn.bangluong', string='Chi tiết bảng lương', inverse_name='bangluong_id',track_visibility='always')


class DATNHrBangLuong(models.Model):
    _name = 'datn.bangluong'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = u'Bảng lương'
    _order = "index DESC"

    bangluong_id = fields.Many2one('datn.luongthang.line', string="Nhân viên", ondelete='cascade')
    code = fields.Char('Mã')
    name = fields.Char('Tên')
    index = fields.Integer('Thứ tự')
    tong_tien = fields.Integer('Tổng tiền')

    _sql_constraints = [
        ('unique_code', 'unique(code)', u'Mã quy tắc đã được tạo')
    ]