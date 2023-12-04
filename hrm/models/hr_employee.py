import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessDenied
from . import constraint
from odoo.exceptions import UserError
from odoo.addons.auth_signup.models.res_users import SignupError


class HrEmployee(models.Model):
    _name = 'hr.employee'
    _inherit = ['hr.employee', 'mail.thread', 'mail.activity.mixin']

    type_block = fields.Selection(constraint.TYPE_BLOCK, string='Khối', required=True, default='BLOCK_COMMERCE_NAME')

    employee_code = fields.Char(string='Mã nhân viên', store=True)

    personal_email = fields.Char('Email cá nhân', tracking=True)
    work_email = fields.Char('Work Email', compute='_compute_work_email', store=True)
    identifier = fields.Char('Số căn cước công dân', required=True, tracking=True)
    work_start_date = fields.Date(string='Ngày vào làm', tracking=True)
    date_receipt = fields.Date(string='Ngày được nhận chính thức', required=True)
    profile_status = fields.Selection(constraint.PROFILE_STATUS, string='Trạng thái hồ sơ')
    auto_create_acc = fields.Boolean(string='Tự động tạo tài khoản', default=True)
    acc_id = fields.Many2one('res.users', string='Tài khoản đăng nhập')

    # Nhân viên khối văn phòng
    department_id = fields.Many2one('hr.department', string='Phòng ban', tracking=True)

    @api.model
    def create(self, vals):
        if not vals.get('employee_code'):
            # Lấy giá trị tiếp theo từ sequence 'hr.employee.sequence'
            sequence = self.env['ir.sequence'].next_by_code('hr.employee.sequence') or '/'
            vals['employee_code'] = sequence
        if  vals['employee_code']:
            block_prefix = 'COM' if vals['type_block'] == 'BLOCK_COMMERCE_NAME' else 'OFF'
            vals['work_email'] = f"{block_prefix}{vals['employee_code']}@huce.com"
            # self.work_email = vals['work_email']
        record = super(HrEmployee, self).create(vals)
        if record:
        # Assuming you want to call the auto_create_account_employee function
            record.auto_create_account_employee()
        return record

    @api.onchange('type_block')
    def _onchange_type_block(self):
        self.parent_id = False
        for rec in self:
            if rec.type_block == 'BLOCK_COMMERCE_NAME':
                if self.env.user.department_id:
                    list_sys_com = self.env['hr.department'].search(
                        [('id', 'child_of', self.env.user.department_id.ids), ('type_in_block_ecom', '=', 'company')])
                else:
                    list_sys_com = self.env['hr.department'].search(
                        [('type_block', '=', 'BLOCK_COMMERCE_NAME'), ('type_in_block_ecom', '=', 'company')])
                return {'domain': {'department_id': [('id', 'in', list_sys_com.ids)]}}
            if rec.type_block == 'BLOCK_OFFICE_NAME':
                if self.env.user.department_id:
                    list_sys_com = self.env['hr.department'].search(
                        [('id', 'child_of', self.env.user.department_id.ids)])
                else:
                    list_sys_com = self.env['hr.department'].search([('type_block', '=', 'BLOCK_OFFICE_NAME')])
                return {'domain': {'department_id': [('id', 'in', list_sys_com.ids)]}}

    @api.depends('employee_code')
    def _compute_work_email(self):
        for record in self:
            if record.employee_code:
               record.work_email
            else:
                record.work_email = False


    def auto_create_account_employee(self):
        # hàm tự tạo tài khoản và gán id tài khoản cho acc_id
        self.ensure_one()
        user_group = self.env.ref('hr.group_hr_user')

        values = {
            'name': self.name,
            'login': self.work_email,
            'password': '1',
            'groups_id': [(6, 0, [user_group.id])],
        }
        new_user = self.env['res.users'].sudo().create(values)
        self.user_id = new_user.id
        return {
            'name': "User Created",
            'type': 'ir.actions.act_window',
            'res_model': 'res.users',
            'res_id': new_user.id,
            'view_mode': 'form',
        }

