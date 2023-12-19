# -*- coding:utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import Warning, ValidationError
class DATNLoaiNghi(models.Model):
    _name = 'datn.config.trocap.phucap'
    _description = 'Cấu hình loại trợ cấp phụ cấp'

    name = fields.Text(string="Tên loại")
    code = fields.Text(string="Mã loại")
    trang_thai_ap_dung = fields.Boolean(string="Trạng thái áp dụng")
    note = fields.Text(string="Chú thích")

    _sql_constraints = [('code_loai_trocap_phucap_unique', 'unique(code)', 'Mã loại trợ cấp, phụ cấp đã tồn tại!')]

