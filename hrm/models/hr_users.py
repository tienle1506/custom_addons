from odoo import models, fields, api
from . import constraint


class Users(models.Model):
    _inherit = 'res.users'

    block_id = fields.Selection(selection=[
        ('full', 'Tất cả khối'),
        ('BLOCK_COMMERCE_NAME', 'Thương mại'),
        ('BLOCK_OFFICE_NAME', 'Văn phòng')], string="Khối phân quyền", default='BLOCK_COMMERCE_NAME', required=True)
    department_id = fields.Many2many('hr.department', string='Phòng/Ban')
    system_ids_custom = fields.Many2many(
        'hr.system',
        string='Hệ thống', store=True
    )

    company_ids_custom = fields.Many2many(
        'hr.company',
        string='Công ty',
    )
    related = fields.Boolean(compute='_compute_related_')
    check_field_company = fields.Boolean(compute='_check_field_company')

    @api.depends('block_id')
    def _compute_related_(self):
        # Lấy giá trị của trường related để check điều kiện hiển thị
        for record in self:
            record.related = record.block_id == 'BLOCK_OFFICE_NAME'

    @api.onchange('block_id')
    def _onchange_block_id(self):
        self.department_id = self.system_ids_custom  = False

    @api.onchange('system_ids_custom')
    def _get_child_company(self):
        if self.system_ids_custom:
            child_system_company = self.env['hr.system'].search([('id', 'child_of', self.system_ids_custom.ids)])
            companies_of_system = self.env['hr.company'].search([('system_id', 'in', child_system_company.ids)])

            # companies chứa danh sách các công ty thuộc child_system_company và các công ty con

            company_domain = [('id', 'in', companies_of_system.ids)]
            return {'domain': {'company_ids_custom': company_domain}}
        else:
            self.company_ids_custom = [(5, 0, 0)]

    @api.onchange('company_ids_custom')
    def _check_field_company(self):
        if self.company_ids_custom:
            self.check_field_company = True
        else:
            self.check_field_company = False
