from odoo import models, api, fields
from odoo.exceptions import ValidationError, AccessDenied
from . import constraint
import re



class HrSystem(models.Model):
    _name = "hr.system"
    _description = 'System'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _rec_name = "name"

    name = fields.Char('Tên Hệ thống', required=True)
    name_display = fields.Char(string="Tên hiển thị", compute='_compute_name_display', store=True)
    system_company_level = fields.Integer(string='Cấp đơn vị', readonly=True, default=1)
    child_ids = fields.One2many('hr.system', 'parent_id', string='Child System')
    active = fields.Boolean('Active', default=True)
    type_system = fields.Selection(constraint.TYPE_SYSTEM, string="Loại hệ thống", tracking=True)
    phone_num = fields.Char(string='Số điện thoại', tracking=True)
    chairperson = fields.Many2one('res.users', string="Chủ tịch")
    vice_president = fields.Many2one('res.users', string='Phó chủ tịch')
    res_user_id = fields.Many2one('res.users')

    def _default_systems(self):
        """Kiểm tra phòng ban mặc định của người dùng và xây dựng danh sách hệ thống con và cháu."""
        if self.env.user.system_ids_custom:
            list_systems = self.env['hr.system'].search([('id', 'child_of', self.env.user.system_ids_custom.ids)])
            return [('id', 'in', list_systems.ids)]

    parent_id = fields.Many2one('hr.system', string='Parent System', tracking=True, index=True, domain=_default_systems)


    @api.onchange('parent_id')
    def _set_system_company_level(self):
        if not self.parent_id:
            self.system_company_level = 1
        res = self.env['hr.system'].search([('id', '=', self.parent_id.id)])
        if res:
            self.system_company_level = res.system_company_level + 1

    @api.depends('parent_id.name_display', 'name')
    def _compute_name_display(self):
        for rec in self:
            if rec.parent_id and rec.name:
                rec.name_display = f'{rec.parent_id.name_display}.{rec.name}'
            elif rec.name:
                rec.name_display = rec.name

    @api.constrains("phone_num")
    def _check_phone_valid(self):
        """
        hàm kiểm tra số điện thoại: không âm, không có ký tự, có số 0 ở đầu
        """
        for rec in self:
            if rec.phone_num:
                if not re.match(r'^\d+$', rec.phone_num):
                    raise ValidationError("Số điện thoại không hợp lệ")

    @api.constrains("chairperson", "vice_president")
    def _check_chairperson_and_vice_president(self):
        """ Kiểm tra xem chairperson và vice_president có trùng id không """
        for rec in self:
            chairperson_id = rec.chairperson.id if rec.chairperson else False
            vice_president_id = rec.vice_president.id if rec.vice_president else False
            if chairperson_id and vice_president_id and chairperson_id == vice_president_id:
                raise ValidationError("Chủ tịch và Phó chủ tịch không thể giống nhau.")

    @api.constrains('name_display', 'type_system')
    def _check_name_block_combination(self):
        """
            Tên vị trí giống nhau nhưng khối khác nhau vẫn có thể lưu được
            Kiểm tra sự trùng lặp dựa trên kết hợp của name và type_system
        """
        for record in self:
            name = self.search([('id', '!=', record.id), ('active', 'in', (True, False))])
            for n in name:
                if n['name'].lower() == record.name_display.lower() and n.type_system == self.type_system:
                    raise ValidationError(constraint.DUPLICATE_RECORD % "Hệ thống")
