import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessDenied
from . import constraint
from odoo.exceptions import UserError
from odoo.addons.auth_signup.models.res_users import SignupError


class HrEmployee(models.Model):
    _name = 'hr.employee'
    _inherit = ['hr.employee', 'mail.thread', 'mail.activity.mixin']

    def default_type_block(self):
        return 'BLOCK_OFFICE_NAME' if self.env.user.block_id == 'BLOCK_OFFICE_NAME' else 'BLOCK_COMMERCE_NAME'

    type_block = fields.Selection(constraint.TYPE_BLOCK, string='Khối', required=True, default=default_type_block)
    type_in_block_ecom = fields.Selection([('system', 'Hệ thống'), ('company', 'Công ty')],
                                          string='Hệ thống / Công ty', default='system')

    employee_code = fields.Char(string='Mã nhân viên', store=True)

    personal_email = fields.Char('Email cá nhân', tracking=True)
    email_work = fields.Char('Work Email', store=True)
    identifier = fields.Char('Số căn cước công dân', required=True, tracking=True)
    work_start_date = fields.Date(string='Ngày vào làm', tracking=True)
    date_receipt = fields.Date(string='Ngày được nhận chính thức', required=True)
    profile_status = fields.Selection(constraint.PROFILE_STATUS, string='Trạng thái hồ sơ')
    auto_create_acc = fields.Boolean(string='Tự động tạo tài khoản', default=True)
    readonly_type_block = fields.Boolean(compute='_compute_readonly_type_block')
    state = fields.Selection(constraint.STATE, default='draft', string="Trạng thái phê duyệt")

    # Nhân viên khối văn phòng
    department_id = fields.Many2one('hr.department', string='Phòng ban', tracking=True)
    # Các trường trong tab luồng phê duyệt hồ sơ
    approved_link = fields.One2many('hr.approval.flow.profile', 'profile_id', tracking=True)
    approved_name = fields.Many2one('hr.approval.flow.object')

    @api.model
    def create(self, vals):
        if not vals.get('employee_code'):
            # Lấy giá trị tiếp theo từ sequence 'hr.employee.sequence'
            sequence = self.env['ir.sequence'].next_by_code('hr.employee.sequence') or '/'
            vals['employee_code'] = sequence

        if vals.get('employee_code'):
            block_prefix = 'COM' if vals.get('type_block') == 'BLOCK_COMMERCE_NAME' else 'OFF'
            vals['email_work'] = f"{block_prefix}{vals.get('employee_code')}@huce.com"

        # Set work_email value in vals before creating the record
        record = super(HrEmployee, self).create(vals)

        if record:
            # Assuming you want to call the auto_create_account_employee function
            record.auto_create_account_employee()
        return record

    @api.onchange('type_block', 'type_in_block_ecom')
    def _onchange_type_block(self):
        self.parent_id = False
        for rec in self:
            if rec.type_block == 'BLOCK_COMMERCE_NAME' and rec.type_in_block_ecom == 'system':

                if self.env.user.department_id:
                    list_sys_com = self.env['hr.department'].search(
                        [('id', 'child_of', self.env.user.department_id.ids), ('type_in_block_ecom', '=', 'system')])
                else:
                    list_sys_com = self.env['hr.department'].search(
                        [('type_block', '=', 'BLOCK_COMMERCE_NAME'), ('type_in_block_ecom', '=', 'system')])
                return {'domain': {'department_id': [('id', 'in', list_sys_com.ids)]}}
            elif rec.type_block == 'BLOCK_COMMERCE_NAME' and rec.type_in_block_ecom == 'company':

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

    # @api.depends('employee_code')
    # def _compute_work_email(self):
    #     for record in self:
    #         if record.employee_code:
    #            record.work_email
    #         else:
    #             record.work_email = False

    def auto_create_account_employee(self):
        # hàm tự tạo tài khoản và gán id tài khoản cho acc_id
        self.ensure_one()
        user_group = self.env.ref('hr.group_hr_user')

        values = {
            'name': self.name,
            'login': self.email_work,
            'password': '1',
            # 'groups_id': [(6, 0, [user_group.id])],
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

    @api.onchange('department_id')
    def onchange_depart(self):
        print(self.department_id.get_all_parents())

    def get_all_parents(self):
        all_parents_ids = set()

        def _recursive_parents(record):
            all_parents_ids.add(record.id)
            if record.parent_id:
                all_parents_ids.add(record.parent_id.id)
                _recursive_parents(record.parent_id)

        _recursive_parents(self)
        return list(all_parents_ids)
    
    def action_send(self):
        # Khi ấn button Gửi duyệt sẽ chuyển từ draft sang pending
        orders = self.filtered(lambda s: s.state == 'draft')
        records = self.env['hr.approval.flow.object'].sudo().search([('type_block', '=', self.type_block)])
        approved_id = None
        if records:
            # Nếu có ít nhất 1 cấu hình cho khối của hồ sơ đang thuộc
            if self.type_block == constraint.BLOCK_COMMERCE_NAME:
                # nếu là khối thương mại
                # Danh sách công ty cha con
                list_company = self.department_id.get_all_parents()
                approved_id = self.find_department(records, list_company)
                # Nếu không có cấu hình cho công ty
                # if not approved_id:
                #     # Danh sách hệ thống cha con
                #     list_system = self.get_all_parent('hrm_systems', 'parent_system', self.system_id.id)
                #     # Trả về bản ghi là cấu hình cho hệ thống
                #     approved_id = self.find_system(list_system, records)
            else:
                # Nếu là khối văn phòng
                # Danh sách các phòng ban cha con
                list_dept = self.department_id.get_all_parents()
                # Trả về bản ghi là cấu hình cho phòng ban
                approved_id = self.find_department(list_dept, records)
        # Nếu tìm được cấu hình
        if approved_id:
            self.approved_name = approved_id.id
            # Clear cấu hình cũ
            self.env['hr.approval.flow.profile'].sudo().search([('profile_id', '=', self.id)]).unlink()

            # Tạo danh sách chứa giá trị dữ liệu từ approval_flow_link
            approved_link_data = approved_id.approval_flow_link.mapped(lambda rec: {
                'profile_id': self.id,
                'step': rec.step,
                'approve': rec.approve.id,
                'obligatory': rec.obligatory,
                'excess_level': rec.excess_level,
                'approve_status': 'pending',
                'time': False,
            })

            # Sử dụng phương thức create để chèn danh sách dữ liệu vào tab trạng thái
            self.sudo().approved_link.create(approved_link_data)

            # đè base thay đổi lịch sử theo  mình
            message_body = "Đã gửi phê duyệt."
            self.message_post(body=message_body, subtype_id=self.env['ir.model.data'].xmlid_to_res_id('mail.mt_note'))
            orders.sudo().write({'state': 'pending'})
            return {'type': 'ir.actions.client', 'tag': 'reload'}
        else:
            raise ValidationError("Lỗi không tìm thấy luồng!")

    def find_department(self, list_dept, records):
        # list_dept là danh sách id hệ thống có quan hệ cha con
        # records là danh sách bản ghi cấu hình luồng phê duyệt
        # Duyệt qua 2 danh sách
        for dept in list_dept:
            for rec in records:
                # Phòng ban có trong cấu hình luồng phê duyệt nào thì trả về bản ghi cấu hình luồng phê duyệt đó
                if dept in rec.department_id.ids:
                    return rec

    def action_cancel(self):
        """Hàm này để hủy bỏ hồ sơ khi đang ở trạng thái chờ phê duyệt"""

        if self.state == "pending":
            self.sudo().write({'state': 'draft'})
            # self.message_post(body="Hủy bỏ phê duyệt.",
            #                   subtype_id=self.env['ir.model.data'].xmlid_to_res_id('mail.mt_note'))