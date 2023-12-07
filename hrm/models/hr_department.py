import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessDenied
from . import constraint



class HrDepartment(models.Model):
    _name = "hr.department"
    _inherit = ['hr.department', 'mail.thread']


    type_in_block_ecom = fields.Selection([('system', 'Hệ thống'), ('company', 'Công ty')],
                                          string='Hệ thống / Công ty', default='system')
    name_display = fields.Char(string="Tên hiển thị", store=True)
    name_system = fields.Char(string='Tên hệ thống')
    name_company = fields.Char(string='Tên công ty')
    department_level = fields.Integer(string='Cấp đơn vị', readonly=True, default=1)
    type_company = fields.Selection(selection=constraint.SELECT_TYPE_COMPANY, string="Loại hình công ty",
                                    tracking=True)
    type_system = fields.Selection(constraint.TYPE_SYSTEM, string="Loại hệ thống", tracking=True)
    parent_id = fields.Many2one('hr.department', string='Parent Department', index=True)
    phone_num = fields.Char(string='Số điện thoại', tracking=True)
    chairperson = fields.Many2one('res.users', string="Chủ tịch")
    vice_president = fields.Many2one('res.users', string='Phó chủ tịch')
    approval_id = fields.Many2one('hr.approval.flow.object', tracking=True)
    relate = fields.Integer()
    res_user_id = fields.Many2one('res.users')
    has_change = fields.Boolean(default=False)
    def default_type_block(self):
        return 'BLOCK_OFFICE_NAME' if self.env.user.block_id == 'BLOCK_OFFICE_NAME' else 'BLOCK_COMMERCE_NAME'
    type_block = fields.Selection([('BLOCK_COMMERCE_NAME', 'Thương mại'),
                                   ('BLOCK_OFFICE_NAME', 'Văn phòng')], string='Loại khối',
                                  default=default_type_block)
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


    @api.onchange('parent_id')
    def _set_department_level(self):
        if not self.parent_id:
            self.department_level = 1
        res = self.env['hr.department'].search([('id', '=', self.parent_id.id)])
        if res:
            self.department_level = res.department_level + 1

    @api.constrains("name")
    def _check_valid_name(self):
        """
        kiểm tra trường name không có ký tự đặc biệt.
        \W là các ký tự ko phải là chữ, dấu cách, _
        """
        if self.type_block == 'BLOCK_OFFICE_NAME':
            for rec in self:
                if rec.name:
                    if re.search(r"[\W]+", rec.name.replace(" ", "")) or "_" in rec.name:
                        raise ValidationError(constraint.ERROR_NAME % 'phòng/ban')

    @api.onchange('type_block', 'type_in_block_ecom')
    def _onchange_relate(self):
        if self.type_block == 'BLOCK_OFFICE_NAME':
            self.relate = 1
        if self.type_block == 'BLOCK_COMMERCE_NAME':
            if self.type_in_block_ecom == 'system':
                self.relate = 3
            else:
                self.relate = 4
    @api.onchange('name_system', 'name_company')
    def _onchange_sys_com_name(self):
        if self.name_system:
            self.name = self.name_system
        elif self.name_company:
            self.name = self.name_company

    @api.constrains('name', 'type_company', 'type_system')
    def _check_name_case_insensitive(self):
        if self.type_block == 'BLOCK_OFFICE_NAME':
            for record in self:
                # Kiểm tra trùng lặp dữ liệu không phân biệt hoa thường
                name = self.search([('id', '!=', record.id), ('active', 'in', (True, False))])
                for n in name:
                    if n['name'].lower() == record.name.lower():
                        raise ValidationError(constraint.DUPLICATE_RECORD % "Phòng ban")
        elif self.type_block == 'BLOCK_COMMERCE_NAME' and self.type_in_block_ecom == 'system':
            for record in self:
                name = self.search([('id', '!=', record.id), ('active', 'in', (True, False))])
                for n in name:
                    if n['name'].lower() == record.name.lower() and n.type_system == self.type_system:
                        raise ValidationError(constraint.DUPLICATE_RECORD % "Hệ thống")
        elif self.type_block == 'BLOCK_COMMERCE_NAME' and self.type_in_block_ecom == 'company':
            for record in self:
                name = self.search([('id', '!=', record.id), ('active', 'in', (True, False))])
                for n in name:
                    if n['name'].lower() == record.name.lower() and n.type_company == self.type_company:
                        raise ValidationError(constraint.DUPLICATE_RECORD % "Công ty")


    def unlink(self, context=None):
        """ Chặn không cho xoá khối 'Văn phòng' và 'Thương mại' """
        for line in self:
            if line.has_change:
                raise ValidationError(constraint.DO_NOT_DELETE)
        return super(HrDepartment, self).unlink()


    @api.onchange('type_block', 'type_in_block_ecom')
    def _onchange_type_block(self):
        self.parent_id = False
        for rec in self:
            if rec.type_block == 'BLOCK_COMMERCE_NAME' and rec.type_in_block_ecom == 'system':
                if self.env.user.department_id:
                    list_sys_com = self.env['hr.department'].search([('id', 'child_of', self.env.user.department_id.ids), ('type_in_block_ecom', '=', 'system')])
                else:
                    list_sys_com = self.env['hr.department'].search([('type_block', '=', 'BLOCK_COMMERCE_NAME'), ('type_in_block_ecom', '=', 'system')])
                return {'domain': {'parent_id':[('id', 'in', list_sys_com.ids)]}}
            if rec.type_block == 'BLOCK_COMMERCE_NAME' and rec.type_in_block_ecom == 'company':
                if self.env.user.department_id:
                    list_sys_com = self.env['hr.department'].search([('id', 'child_of', self.env.user.department_id.ids)])
                else:
                    list_sys_com = self.env['hr.department'].search([('type_block', '=', 'BLOCK_COMMERCE_NAME')])
                return {'domain': {'parent_id':[('id', 'in', list_sys_com.ids)]}}
            if rec.type_block == 'BLOCK_OFFICE_NAME':
                if self.env.user.department_id:
                    list_sys_com = self.env['hr.department'].search([('id', 'child_of', self.env.user.department_id.ids)])
                else:
                    list_sys_com = self.env['hr.department'].search([('type_block', '=', 'BLOCK_OFFICE_NAME')])
                return {'domain': {'parent_id':[('id', 'in', list_sys_com.ids)]}}