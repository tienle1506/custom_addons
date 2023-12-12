import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessDenied
from . import constraint


class Position(models.Model):
    _name = 'hr.job'
    _description = 'Vị trí công việc'
    _rec_name = "name"
    _inherit = ['hr.job', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']

    type_block = fields.Selection(selection=[
        (constraint.BLOCK_OFFICE_NAME, constraint.BLOCK_OFFICE_NAME),
        (constraint.BLOCK_COMMERCE_NAME, constraint.BLOCK_COMMERCE_NAME)], string="Khối", required=True, tracking=True)
    # team_type = fields.Selection([('marketing', 'Marketing'), ('sale', 'Sale')], string='Loại đội ngũ',
    #                              default='marketing')
    # related = fields.Boolean(compute='_compute_related_field')
    # check_blocks = fields.Char(default=lambda self: self.env.user.block_id)
