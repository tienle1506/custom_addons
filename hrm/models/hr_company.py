import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessDenied
from . import constraint


class HrCompany(models.Model):
    _name = "hr.company"
    _description = 'Company'
    _inherit = ['mail.thread']

    name = fields.Char('Tên Công ty', required=True)
    name_display = fields.Char(string="Tên hiển thị", compute='_compute_name_display', store=True)
    system_company_level = fields.Integer(string='Cấp đơn vị', readonly=True, default=1)

    child_ids = fields.One2many('hr.company', 'parent_id', string='Child Company')
    active = fields.Boolean('Active', default=True)
    type_company = fields.Selection(selection=constraint.SELECT_TYPE_COMPANY, string="Loại hình công ty",
                                    tracking=True)
    active = fields.Boolean('Active', default=True)
    phone_num = fields.Char(string='Số điện thoại', tracking=True)
    chairperson = fields.Many2one('res.users', string="Chủ tịch")
    vice_president = fields.Many2one('res.users', string='Phó chủ tịch')
    change_system_id = fields.Many2one('hr.system', string="Hệ thống", default=False)
    res_user_id = fields.Many2one('res.users')
    readonly_sys = fields.Boolean(compute='logic_in_field_readonly_sys')

    # @api.onchange('parent_id', 'system_id')
    # def _set_system_company_level(self):
    #     if self.system_id:
    #         res = self.env['hr.system'].search([('id', '=', self.system_id.id)])
    #         print(res)
    #         self.system_company_level = res.system_company_level + 1
    #     elif self.system_id and self.parent_id:
    #         self.system_company_level = self.parent_id.system_company_level + 1
    #     elif not self.parent_id and not self.system_id:
    #         self.system_company_level = 0

    @api.depends('system_id.name_display', 'type_company', 'name')
    def _compute_name_display(self):
        for rec in self:
            type_company = rec.type_company and rec.type_company[0].capitalize() or ''
            name_system = rec.system_id and rec.system_id.name or ''
            name_main = rec.name or ''
            name_parts = [part for part in [type_company, name_system, name_main] if part]  # Lọc các trường không rỗng
            rec.name_display = '.'.join(name_parts)

    def _default_systems(self):
        """Kiểm tra phòng ban mặc định của người dùng và xây dựng danh sách hệ thống con và cháu."""
        if self.env.user.system_ids_custom and not self.env.user.company_ids_custom:
            list_systems = self.env['hr.system'].search([('id', 'child_of', self.env.user.system_ids_custom.ids)])
            return [('id', 'in', list_systems.ids)]
        if self.env.user.company_ids_custom or self.env.user.block_id == 'BLOCK_OFFICE_NAME':
            # nếu có công ty thì không hiển thị hệ thống
            return [('id', '=', 0)]
        return []

    system_id = fields.Many2one('hr.system', string='System', index=True, domain=_default_systems)

    def _get_child_company(self):
        """ lấy tất cả công ty user được cấu hình trong thiết lập """
        if self.env.user.company_ids_custom:
            # nếu user đc cấu hình công ty thì lấy list id công ty con của công ty đó
            child_company = self.env['hr.company'].search([('id', 'child_of', self.env.user.company_ids_custom.ids)])
            list_child_company = [('id', 'in', child_company.ids)]
        elif not self.env.user.company_ids_custom and self.env.user.system_ids_custom:
            # nếu user chỉ đc cấu hình hệ thống
            # lấy list id công ty con của hệ thống đã chọn
            child_system_company = self.env['hr.system'].search(
                [('id', 'child_of', self.env.user.system_ids_custom.ids)])
            companies_of_system = self.env['hr.company'].search([('system_id', 'in', child_system_company.ids)])

            # companies chứa danh sách các công ty thuộc child_system_company và các công ty con

            list_child_company = [('id', 'in', companies_of_system.ids)]

        return list_child_company

    def _default_company(self):
        """ tạo bộ lọc các công ty user có thể cấu hình """
        if self.env.user.block_id != 'BLOCK_OFFICE_NAME' and not self.env.user.company_ids_custom and not self.env.user.system_ids_custom:
            # nếu user không cấu hình công ty và hệ thống, khối khác văn phòng thì hiển thị all
            return []
        company_ids = self._get_child_company()  # Assuming _get_child_company() returns a list of integers
        return company_ids

    parent_id = fields.Many2one('hr.company', string='Parent Company', index=True, domain=_default_company)

    @api.onchange('parent_id')
    def logic_in_field_readonly_sys(self):
        if self.env.user.company_ids_custom:
            self.readonly_sys = True
        elif self.env.user.block_id != 'BLOCK_OFFICE_NAME' and not self.env.user.company_ids_custom:
            self.readonly_sys = False

    @api.onchange('parent_id')
    def _onchange_parent_company(self):
        """ decorator này  chọn cty cha
            sẽ tự hiển thị hệ thống mà công ty đó thuộc vào
        """
        company_system = self.parent_id.system_id
        if company_system:
            self.system_id = company_system
        elif self.change_system_id:
            self.system_id = self.change_system_id
        else:
            self.system_id = False

    @api.onchange('system_id')
    def _onchange_system(self):
        #     """decorator này  chọn lại hệ thống sẽ clear công ty cha"""
        self.change_system_id = self.system_id
        if not self.system_id.name_display:
            self.parent_id = False
        if self.system_id != self.parent_id.system_id:
            self.parent_id = False
            child_system = self.env['hr.system'].search([('id', 'child_of', self.system_id.ids)])
            list_company_of_sys = self.env['hr.company'].search([('system_id', 'in', child_system.ids)])
            return {'domain': {'parent_id': [('id', 'in', list_company_of_sys.ids)]}}

    @api.constrains('name_display', 'type_company')
    def _check_name_block_combination(self):
        # Kiểm tra sự trùng lặp dựa trên kết hợp của work_position và block
        for record in self:
            name = self.search([('id', '!=', record.id), ('active', 'in', (True, False))])
            for n in name:
                if n['name'].lower() == record.name_display.lower() and n.type_company == self.type_company:
                    raise ValidationError(constraint.DUPLICATE_RECORD % "Công ty")


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
