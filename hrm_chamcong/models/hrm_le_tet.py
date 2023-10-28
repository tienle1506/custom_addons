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

class DATNHrLeTet(models.Model):
    _name = 'datn.hr.le.tet'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = u'Quản lý ngày lễ tết'
    _order = "date_from DESC, date_to DESC"

    name = fields.Char(string=u'Tên ngày lễ tết', size=128, track_visibility='always', )
    block_id = fields.Many2one('hrm.blocks', string='Khối', required=True,
                    default=lambda self: self.default_block_profile(),
                    tracking=True)
    date_from = fields.Date(u'Từ ngày', widget='date', format='%Y-%m-%d')
    date_to = fields.Date(u'Đến ngày', widget='date', format='%Y-%m-%d')
    notes = fields.Text(u'Chú thích')

    @api.constrains('date_from', 'date_to')
    def constrains_date(self):
        for r in self:
            if r.date_start >= r.date_end:
                raise ValidationError(_('Từ ngày phải nhỏ hơn đến ngày!!!'))
