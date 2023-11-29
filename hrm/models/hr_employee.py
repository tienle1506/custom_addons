import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessDenied
from . import constraint


class HrEmployee(models.Model):
    _name = 'hr.employee'
    _inherit = ['hr.employee', 'mail.thread', 'mail.activity.mixin']

    type_block = fields.Selection(constraint.TYPE_BLOCK, string='Khối', required=True, default='BLOCK_COMMERCE_NAME')

    employee_code = fields.Char(string='Mã nhân viên', store=True)

    email = fields.Char('Email công việc', required=True, tracking=True)
    phone_num = fields.Char('Số điện thoại di động', required=True, tracking=True)
    identifier = fields.Char('Số căn cước công dân', required=True, tracking=True)
    work_start_date = fields.Date(string='Ngày vào làm', tracking=True)
    date_receipt = fields.Date(string='Ngày được nhận chính thức', required=True)
    profile_status = fields.Selection(constraint.PROFILE_STATUS, string='Trạng thái hồ sơ')
    auto_create_acc = fields.Boolean(string='Tự động tạo tài khoản', default=True)

    # Nhân viên khối thương mại
    system_id = fields.Many2one('hr.system', string='Hệ thống', tracking=True)
    company_id2 = fields.Many2one('hr.company', string='Công ty', tracking=True)

    # Nhân viên khối văn phòng
    department_id = fields.Many2one('hr.department', string='Phòng ban', tracking=True)
    #
    # @api.depends('name')
    # def _render_code(self):
    #     for record in self:
    #         if not record.employee_code:
    #             last_employee_code = self._get_last_employee_code()
    #             record.employee_code = self._generate_employee_code(last_employee_code)
    #
    # @api.model
    # def _get_last_employee_code(self):
    #     """
    #         Hàm lấy mã nhân viên cuối cùng mà nó trùng với mã hệ thống đang chọn
    #         query dữ liệu từ dưới lên gặp mã nào trùng thì lấy và kết thúc query
    #         Kết quả cuối cùng return về mã nhân viên nếu có hoặc None nếu không thấy
    #     """
    #     domain = [('employee_code', '!=', False), ('active', 'in', (True, False))]
    #     order = 'employee_code desc'
    #     limit = 1
    #     last_employee = self.env['hr.employee'].search(domain, order=order, limit=limit)
    #     if last_employee:
    #         return last_employee.employee_code
    #     return None
    #
    # @api.model
    # def _generate_employee_code(self, last_employee_code):
    #     """
    #         Hàm nối chuỗi để lấy mã nhân viên theo logic
    #     """
    #     if last_employee_code:
    #         numbers = int(last_employee_code) + 1
    #         return f"{numbers:06d}" if numbers < 999999 else "000001"
    #     else:
    #         return "000001"

    @api.model
    def create(self, vals):
        if not vals.get('employee_code'):
            # Lấy giá trị tiếp theo từ sequence 'hr.employee.sequence'
            sequence = self.env['ir.sequence'].next_by_code('hr.employee.sequence') or '/'
            vals['employee_code'] = sequence

        return super(HrEmployee, self).create(vals)