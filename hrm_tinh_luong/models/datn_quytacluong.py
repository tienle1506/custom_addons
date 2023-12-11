# -*- coding:utf-8 -*-
from odoo import api, fields, models, _
class DATNQuyTacLuong(models.Model):
    _name = "datn.quytacluong"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = u'Quy tắc lương'
    _order = "index"

    code = fields.Char(string='Mã quy tắc', required=True, default='')
    name = fields.Char(string='Tên quy tắc', required=True, default='')
    mapython = fields.Text(string='Mã Python', required=True, default='')
    index = fields.Integer(string='Thứ tự ưu tiên', default=0)
    hieuluc = fields.Boolean(string='Hiệu lực', default=True)
    description = fields.Text(string='Mô tả')

    _sql_constraints = [
        ('unique_code', 'unique(code)', u'Mã quy tắc đã được tạo')
    ]