import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessDenied
from . import constraint



class HrDepartment(models.Model):
    _name = "hr.department"
    _inherit = ['hr.department', 'mail.thread']

    department_level = fields.Integer(string='Cấp đơn vị', readonly=True, default=1)
    phone_num = fields.Char(string='Số điện thoại', tracking=True)
    res_user_id = fields.Many2one('res.users')
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
        for rec in self:
            if rec.name:
                if re.search(r"[\W]+", rec.name.replace(" ", "")) or "_" in rec.name:
                    raise ValidationError(constraint.ERROR_NAME % 'phòng/ban')