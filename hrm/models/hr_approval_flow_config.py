from odoo import models, fields, api
from . import constraint
from odoo.exceptions import ValidationError, AccessDenied

list_department = []


class ApprovalFlowObject(models.Model):
    _name = 'hr.approval.flow.object'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']

    name = fields.Char(string='Tên luồng phê duyệt', required=True, tracking=True)

    def default_type_block(self):
        return 'BLOCK_OFFICE_NAME' if self.env.user.block_id == 'BLOCK_OFFICE_NAME' else 'BLOCK_COMMERCE_NAME'

    type_block = fields.Selection([('BLOCK_COMMERCE_NAME', 'Thương mại'),
                                   ('BLOCK_OFFICE_NAME', 'Văn phòng')], string='Loại khối',
                                  default=default_type_block)
    department_id = fields.Many2many('hr.department', string='Phòng ban', tracking=True, )
    approval_flow_link = fields.One2many('hr.approval.flow', 'approval_id', tracking=True)
    check_blocks = fields.Char(default=lambda self: self.env.user.block_id)

    # related = fields.Boolean(compute='_compute_related_')

    @api.onchange('type_block')
    def _onchange_type_block(self):
        # self.parent_id = False
        for rec in self:
            if rec.type_block == 'BLOCK_COMMERCE_NAME':
                if self.env.user.department_id:
                    list_sys_com = self.env['hr.department'].search(
                        [('id', 'child_of', self.env.user.department_id.ids)])
                else:
                    list_sys_com = self.env['hr.department'].search([('type_block', '=', 'BLOCK_COMMERCE_NAME')])
                return {'domain': {'department_id': [('id', 'in', list_sys_com.ids)]}}
            if rec.type_block == 'BLOCK_OFFICE_NAME':
                if self.env.user.department_id:
                    list_sys_com = self.env['hr.department'].search(
                        [('id', 'child_of', self.env.user.department_id.ids)])
                else:
                    list_sys_com = self.env['hr.department'].search([('type_block', '=', 'BLOCK_OFFICE_NAME')])
                return {'domain': {'department_id': [('id', 'in', list_sys_com.ids)]}}

    @api.onchange('type_block')
    def _onchange_block(self):
        self.department_id = False
        list_department.clear()
        list_record_in_block = self.env['hr.approval.flow.object'].search([('type_block', '=', self.type_block)])
        for object in list_record_in_block:
            list_department.extend(object.department_id.ids)

    @api.onchange('approval_flow_link')
    def _check_duplicate_approval(self):
        """decorator này để check trùng nhân viên tham gia luồng phê duyệt"""
        list_user_approve = [record.approve for record in self.approval_flow_link]
        seen = set()
        for item in list_user_approve:
            if item in seen:
                raise ValidationError(f'Người dùng tên {item.name} đã có trong luồng duyệt')
            else:
                seen.add(item)

    @api.constrains('approval_flow_link')
    def check_approval_flow_link(self):
        for record in self:
            if not record.approval_flow_link:
                raise ValidationError('Không thể tạo luồng phê duyệt khi không có người phê duyệt trong luồng.')
            else:
                list_check = []
                for item in record.approval_flow_link:
                    if item.obligatory:
                        list_check.append(True)
                if not any(list_check):
                    raise ValidationError('Luồng phê duyệt cần có ít nhất một người bắt buộc phê duyệt.')

    @api.onchange('department_id')
    def check_duplicate_config(self):
        department_user_picked = self.department_id.ids
        for rec in department_user_picked:
            if rec in list_department:
                raise ValidationError('Hệ thống / Công ty / Phòng ban bạn vừa chọn đã có trong luồng phê duyệt khác !')

    @api.constrains('name', 'type_block', 'department_id')
    def check_permission(self):
        if self.env.user.block_id == 'BLOCK_OFFICE_NAME':
            if self.env.user.department_id.ids:
                list_department_in_check = self.env['hr.department'].search(
                    [('id', 'child_of', self.env.user.department_id.ids)])
                for depart in self.department_id:
                    if depart.id not in list_department_in_check.ids:
                        raise AccessDenied(f"Bạn không có quyền cấu hình cho {depart.name}")
        if self.env.user.block_id == 'BLOCK_COMMERCE_NAME':
            if self.env.user.department_id.ids:
                list_sys_company = self.env['hr.department'].search(
                    [('id', 'child_of', self.env.user.department_id.ids)])
                for depart in self.department_id:
                    if depart.id not in list_sys_company.ids:
                        raise AccessDenied(f"Bạn không có quyền cấu hình cho {depart.name}")
        if self.type_block != self.env.user.block_id and self.env.user.block_id != 'full':
            if self.type_block == 'BLOCK_COMMERCE_NAME':
                raise AccessDenied(f'Bạn không có quyền cấu hình khối Thương mại!')
            else:
                raise AccessDenied(f'Bạn không có quyền cấu hình khối Văn Phòng!')

    def unlink(self):
        # Lấy danh sách tất cả các bản ghi hr.approval.flow liên quan đến các bản ghi sẽ bị xóa
        approval_flows = self.mapped('approval_flow_link')

        # Xóa tất cả các bản ghi hr.approval.flow liên quan
        approval_flows.unlink()

        # Gọi phương thức unlink mặc định của model để hoàn thành việc xóa
        return super(ApprovalFlowObject, self).unlink()


class Approve(models.Model):
    _name = 'hr.approval.flow'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']

    approval_id = fields.Many2one('hr.approval.flow.object')
    step = fields.Integer(string='Bước', default=1, order='step')
    approve = fields.Many2one('res.users', string='Người phê duyệt', required=True, tracking=True)
    obligatory = fields.Boolean(string='Bắt buộc')
    excess_level = fields.Boolean(string='Vượt cấp')


class ApproveProfile(models.Model):
    _name = 'hr.approval.flow.profile'
    _inherit = 'hr.approval.flow'

    profile_id = fields.Many2one('hr.employee')
    approve_status = fields.Selection(constraint.APPROVE_STATUS, default='pending', string="Trạng thái")
    time = fields.Datetime(string="Thời gian")
