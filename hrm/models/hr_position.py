import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessDenied
from . import constraint


class Position(models.Model):
    _name = 'hr.position'
    _description = 'Vị trí'
    _rec_name = "name"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']

    name = fields.Char(string='Tên Vị Trí', required=True, tracking=True)
    type_block = fields.Selection(selection=[
        (constraint.BLOCK_OFFICE_NAME, constraint.BLOCK_OFFICE_NAME),
        (constraint.BLOCK_COMMERCE_NAME, constraint.BLOCK_COMMERCE_NAME)], string="Khối", required=True, tracking=True
        , default=lambda self: self.env.user.block_id)
    # team_type = fields.Selection([('marketing', 'Marketing'), ('sale', 'Sale')], string='Loại đội ngũ',
    #                              default='marketing')
    active = fields.Boolean(string='Hoạt Động', default=True)
    # related = fields.Boolean(compute='_compute_related_field')
    # check_blocks = fields.Char(default=lambda self: self.env.user.block_id)

