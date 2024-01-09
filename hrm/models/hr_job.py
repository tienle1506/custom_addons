import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessDenied
from . import constraint


class Position(models.Model):
    _name = 'hr.job'
    _description = 'Vị trí công việc'
    _rec_name = "name"
    _inherit = ['hr.job', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']

    def default_type_block(self):
        return 'BLOCK_OFFICE_NAME' if self.env.user.block_id == 'BLOCK_OFFICE_NAME' else 'BLOCK_COMMERCE_NAME'

    type_block = fields.Selection(constraint.TYPE_BLOCK, string='Khối', required=True, default=default_type_block)
    department_id = fields.Many2one('hr.department')

    # related = fields.Boolean(compute='_compute_related_field')
    # check_blocks = fields.Char(default=lambda self: self.env.user.block_id)
    readonly_type_block = fields.Boolean(compute='_compute_readonly_type_block')

    @api.depends('type_block')
    def _compute_readonly_type_block(self):
        for record in self:
            if record.env.user.block_id == 'full':
                record.readonly_type_block = False
            elif record.env.user.block_id == 'BLOCK_COMMERCE_NAME':
                record.type_block = 'BLOCK_COMMERCE_NAME'
                record.readonly_type_block = True
            elif record.env.user.block_id == 'BLOCK_OFFICE_NAME':
                record.type_block = 'BLOCK_OFFICE_NAME'
                record.readonly_type_block = True
        print(self.readonly_type_block)

    @api.onchange('type_block')
    def onchange_type_block(self):
        for rec in self:
            if rec.type_block == 'BLOCK_OFFICE_NAME':
                if self.env.user.department_id:
                    list_sys_com = self.env['hr.department'].search(
                        [('id', 'child_of', self.env.user.department_id.ids)])
                else:
                    list_sys_com = self.env['hr.department'].search([('type_block', '=', 'BLOCK_OFFICE_NAME')])
                return {'domain': {'department_id': [('id', 'in', list_sys_com.ids)]}}
