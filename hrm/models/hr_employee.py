import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessDenied
from . import constraint
from lxml import etree
import json
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

    personal_email = fields.Char('Email cá nhân', tracking=True, required=False)
    email_work = fields.Char('Work Email', store=True, readonly=True)
    identifier = fields.Char('Số căn cước công dân', tracking=True)
    work_start_date = fields.Date(string='Ngày vào làm', tracking=True)
    date_receipt = fields.Date(string='Ngày được nhận chính thức', required=True)
    profile_status = fields.Selection(constraint.PROFILE_STATUS, string='Trạng thái hồ sơ')
    auto_create_acc = fields.Boolean(string='Tự động tạo tài khoản', default=True)
    readonly_type_block = fields.Boolean(compute='_compute_readonly_type_block')
    state = fields.Selection(constraint.STATE, default='draft', string="Trạng thái phê duyệt")

    def _default_team(self):
        return [('id', '=', 0)]

    team_marketing = fields.Many2one('hr.teams', string='Đội ngũ marketing', tracking=True, domain=_default_team)
    team_sales = fields.Many2one('hr.teams', string='Đội ngũ bán hàng', tracking=True, domain=_default_team)

    # require_team_marketing = fields.Boolean(default=False)
    # require_team_sale = fields.Boolean(default=False)
    # Tab tạo tài khoản tự động
    account_link = fields.Many2one('res.users', string="Tài khoản liên kết", readonly=1)
    url_reset_password = fields.Char(string="Link khôi phục mật khẩu", related='account_link.signup_url', readonly=True)
    url_reset_password_valid = fields.Boolean(string="Link khôi phục mật khẩu hợp lệ",
                                              related='account_link.signup_valid', readonly=True)
    status_account = fields.Boolean(string="Trạng thái tài khoản", related='account_link.active', readonly=True)
    # lý do từ chối
    reason_refusal = fields.Char(string='Lý do từ chối', index=True, ondelete='restrict', tracking=True)
    reason_reopening = fields.Char(string='Lý do mở lại tài khoản', index=True, tracking=True)

    # Nhân viên khối văn phòng
    department_id = fields.Many2one('hr.department', string='Phòng ban', tracking=True)
    # Các trường trong tab luồng phê duyệt hồ sơ
    approved_link = fields.One2many('hr.approval.flow.profile', 'profile_id', tracking=True)
    approved_name = fields.Many2one('hr.approval.flow.object')
    # Mở lại tài khoản
    date_close = fields.Datetime(string='Ngày đóng tài khoản', readonly=True)
    date_open = fields.Datetime(string='Ngày mở lại tài khoản', readonly=True)
    state_reopen = fields.Selection(constraint.STATE_REOPEN, default='close',
                                    string="Trạng thái mở lại tài khoản")

    can_see_approved_record = fields.Boolean()
    can_see_button_approval = fields.Boolean()
    can_see_opening_record = fields.Boolean()
    can_see_button_opening = fields.Boolean()
    cancelled_reopen_account = fields.Boolean(string='Huỷ', default=False)

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

        # if record:
        #     # Assuming you want to call the auto_create_account_employee function
        #     record.auto_create_account_employee()
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

    def action_confirm(self):
        # Khi ấn button Phê duyệt sẽ chuyển từ pending sang approved
        orders = self.sudo().filtered(lambda s: s.state in ['pending', 'wait_reopen'])
        id_access = self.env.user.id
        step = 0  # step đến lượt
        step_excess_level = 0  # step vượt cấp
        for rec in orders.approved_link:
            if rec.approve.id == id_access and rec.excess_level == False:
                step = rec.step
            elif rec.approve.id == id_access and rec.excess_level == True:
                step_excess_level = rec.step
        for rec in orders.approved_link:
            if (step and rec.step <= step and rec.approve_status == 'pending') or step_excess_level == rec.step:
                rec.approve_status = 'confirm'
                rec.time = fields.Datetime.now()
            elif step_excess_level and rec.step < step_excess_level and rec.approve_status == 'pending':
                # nếu là duyệt vượt cấp thì các trạng thái trước đó là pending chuyển qua confirm_excess_level
                rec.approve_status = 'confirm_excess_level'
                rec.time = fields.Datetime.now()

        message_body = f"Chờ Duyệt => Đã Phê Duyệt Tài Khoản - {self.name}"
        self.sudo().message_post(body=message_body,
                                 subtype_id=self.env['ir.model.data'].xmlid_to_res_id('mail.mt_note'))
        query = f"""
                SELECT MAX(step) FROM hr_approval_flow_profile
                WHERE profile_id = {orders.id} AND obligatory = true;
                """
        self._cr.execute(query)
        max_step = self._cr.fetchone()
        if self.state == 'pending' and max_step[0] <= step or max_step[0] <= step_excess_level:
            print(self.state)
            state = 'approved'
            # create new account when approved
            if self.auto_create_acc:
                self.ensure_one()
                user_group = self.env.ref('hrm.hrm_group_own_edit')
                self.env['res.users'].sudo().create({
                    'name': self.name,
                    'login': self.email_work,
                    'email': self.personal_email,
                    'block_id': self.type_block,
                    'department_id': self.department_id,
                    # 'user_code': self.employee_code_new,
                    # 'user_position_id': self.position_id.id,
                    # 'user_team_marketing': self.team_marketing.id,
                    # 'user_team_sales': self.team_sales.id,
                    # 'user_phone_num': self.phone_num,
                    'groups_id': [(6, 0, [user_group.id])],
                })
                self.user_id = self.env['res.users'].search([('login', '=', self.email_work)]).id
                self.account_link = self.env['res.users'].search([('login', '=', self.email_work)])
        elif max_step[0] <= step or max_step[0] <= step_excess_level and self.state == 'wait_reopen':
            self.user_id.active = True
            self.user_id.action_reset_password()
            state = 'approved'
        orders.write({'state': state})
        return {'type': 'ir.actions.client', 'tag': 'reload'}

    def action_refuse(self, reason_refusal=None):
        # Khi ấn button Từ chối sẽ chuyển từ pending sang draft
        if reason_refusal:
            # nếu có lý do từ chối thì gán lý do từ chối vào trường reason_refusal
            self.reason_refusal = reason_refusal
        orders = self.sudo().filtered(lambda s: s.state in ['pending'])
        # Lấy id người đăng nhập
        id_access = self.env.user.id
        # Duyệt qua bản ghi trong luồng (là những người được duyệt)
        for rec in orders.approved_link:
            # Tìm người trong luồng có id = người đang đăng nhập
            # Thay trạng thái của người đó trong bản ghi thành refuse
            if rec.approve.id == id_access:
                rec.approve_status = 'refuse'
                rec.time = fields.Datetime.now()
        orders.write({'state': 'draft'})
        return {'type': 'ir.actions.client', 'tag': 'reload'}

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

    # @api.onchange('department_id')
    # def onchange_depart(self):
    #     """decorator này tạo hồ sơ nhân viên, chọn cty cho hồ sơ đó
    #                  sẽ tự hiển thị đội ngũ mkt và sale nó thuộc vào
    #             """
    #     self.team_marketing = self.team_sales = False
    #     if self.type_block == 'BLOCK_COMMERCE_NAME' and self.type_in_block_ecom == 'company':
    #         if self.department_id:
    #             list_team_marketing = self.env['hr.teams'].search(
    #                 [('department_id', '=', self.department_id.id), ('type_team', '=', 'marketing')])
    #             list_team_sale = self.env['hr.teams'].search(
    #                 [('department_id', '=', self.department_id.id), ('type_team', 'in', ('sale', 'resale'))])
    #         else:
    #             return {}
    #         return {
    #             'domain': {
    #                 'team_marketing': [('id', 'in', list_team_marketing.ids)],
    #                 'team_sales': [('id', 'in', list_team_sale.ids)]
    #             }
    #         }

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

    def see_own_approved_record(self):
        """Nhìn thấy những hồ sơ user được cấu hình"""
        profile = self.env['hr.employee'].sudo().search([('state', '!=', 'draft')])
        for p in profile:
            if self.env.user.id in p.approved_link.approve.ids:
                p.can_see_approved_record = True
            else:
                p.can_see_approved_record = False

    def logic_button(self):
        """Nhìn thấy button khi đến lượt phê duyệt"""
        profile = self.env['hr.employee'].sudo().search([('state', '=', 'pending')])
        for p in profile:
            # list_id lưu id người đang đến lượt
            query = f"""
                    SELECT approve
                    FROM hr_approval_flow_profile where profile_id = {p.id}
                    AND (
                      (step = (
                        SELECT MIN(step)
                        FROM hr_approval_flow_profile
                        WHERE approve_status = 'pending' AND obligatory = true
                        AND profile_id = {p.id}
                      ))
                      OR
                      (excess_level = true AND step = (
                        SELECT MIN(step)
                        FROM hr_approval_flow_profile
                        WHERE approve_status = 'pending' AND profile_id = {p.id}
                        AND excess_level = true
                      ))
                    );
                """
            self._cr.execute(query)
            list_id = self._cr.fetchall()
            list_id_last = [i[0] for i in list_id]
            if self.env.user.id in list_id_last:
                p.can_see_button_approval = True
            else:
                p.can_see_button_approval = False

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(HrEmployee, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                      submenu=submenu)
        # self.env['hrm.utils']._see_record_with_config('hrm.employee.profile')
        self.see_own_approved_record()
        self.logic_button()
        self.see_own_opening_record()
        self.logic_button_opening()
        # self.compute_see_button_reset_and_lock()

        # Kiểm tra xem view_type có phải là 'form' và user_id có tồn tại
        if view_id:
            view = self.env['ir.ui.view'].browse(view_id)
            view_name = view.name
        if view_type == 'form' and not self.id and view_name == 'view.hr.employee.form.inherit':
            user_id = self.env.user.id
            # Kiểm tra trạng thái của bản ghi
            record_id = self.env.context.get('params', {}).get('id')
            if record_id:
                record = self.browse(record_id)
                if record.state != 'draft':
                    res['arch'] = res['arch'].replace(
                        '<form string="Tạo mới hồ sơ" create="false" edit="true" modifiers="{}">',
                        '<form string="Tạo mới hồ sơ" create="false" edit="false" modifiers="{}">')

            # Tạo một biểu thức domain mới để xác định xem nút có nên hiển thị hay không
            # Thuộc tính của trường phụ thuộc vào modifiers
            res['arch'] = res['arch'].replace(
                '<button name="action_send" string="Gửi duyệt" type="object" class="btn-primary"/>',
                f'<button name="action_send" string="Gửi duyệt" type="object" class="btn-primary" modifiers=\'{{"invisible":["|",["state","in",["pending","approved"]],["create_uid", "!=", {user_id}]]}}\'/>'
            )
            res['arch'] = res['arch'].replace(
                '<button name="action_cancel" string="Hủy" type="object"/>',
                f'<button name="action_cancel" string="Hủy" type="object" style="background-color: #FD5050; border-radius: 5px;color:#fff;" modifiers=\'{{"invisible":["|",["state","!=","pending"],["create_uid", "!=", {user_id}]]}}\'/>'
            )

            res['arch'] = res['arch'].replace(
                '<button name="reset_password" string="Đặt lại mật khẩu" type="object" class="btn-info"/>',
                f'<button name="reset_password" string="Đặt lại mật khẩu" type="object" class="btn-info" modifiers=\'{{"invisible":[["can_see_button_reset_lock", "=", false]]}}\'/>'
            )
            id_action = self.env['ir.actions.act_window'].sudo().search(
                [('name', '=', 'Xác nhận khóa tài khoản nhân sự')], limit=1)
            res['arch'] = res['arch'].replace(
                f'<button name="{id_action.id}" type="action" string="Khóa TK nhân sự" class="btn-red"/>',
                f'<button name="{id_action.id}" type="action" string="Khóa TK nhân sự" class="btn-red" modifiers=\'{{"invisible":[["can_see_button_reset_lock", "=", false]]}}\'/>'
            )

            doc = etree.XML(res['arch'])

            """Đoạn code dưới để readonly các trường nếu acc_id bản ghi đó != user.id """
            # Truy cập và sửa đổi modifier của trường 'name' trong form view
            # has_group_readonly = self.env.user.has_group("hrm.hrm_group_read_only")
            has_group_config = self.env.user.has_group("hrm.hrm_group_config_access")
            has_group_own_edit = self.env.user.has_group("hrm.hrm_group_own_edit")
            has_group_create_edit = self.env.user.has_group("hrm.hrm_group_create_edit")
            config_group = doc.xpath("//group")
            if config_group:
                cf = config_group[0]
                if has_group_create_edit or has_group_config:
                    # nếu user login có quyền cấu hình
                    for field in cf.xpath("//field[@name]"):
                        modifiers = field.attrib.get('modifiers', '')
                        modifiers = json.loads(modifiers) if modifiers else {}
                        if field.get("name") not in ['employee_code_new', 'document_config', 'document_list',
                                                     'manager_id', 'profile_status', 'account_link_secondary']:
                            modifiers.update({'readonly': ["|", ['id', '!=', False], ['create_uid', '!=', user_id],
                                                           ['state', '!=', 'draft']]})
                        if field.get("name") in ['phone_num', 'email', 'identifier']:
                            modifiers.update({'readonly': ["|", ["id", "!=", False],
                                                           ["create_uid", "!=", user_id], ['state', '=', 'pending']]})
                        if field.get("name") == 'block_id':
                            modifiers.update(
                                {'readonly': ["|", ["check_blocks", "!=", 'full'], ['state', '!=', 'draft']]})

                        field.attrib['modifiers'] = json.dumps(modifiers)
                elif has_group_own_edit:
                    # nếu user login có quyền chỉ chỉnh sửa chính mình
                    for field in cf.xpath("//field[@name]"):
                        modifiers = field.attrib.get('modifiers', '')
                        modifiers = json.loads(modifiers) if modifiers else {}
                        if field.get("name") not in ['phone_num', 'email', 'identifier']:
                            modifiers.update({'readonly': True})
                        else:
                            modifiers.update({'readonly': ["|", ['state', '!=', 'draft'], ['acc_id', '!=', user_id]]})
                        field.attrib['modifiers'] = json.dumps(modifiers)
            #     elif has_group_readonly:
            #         # nếu user login có quyền chỉ đọc thì set các field readonly
            #         for field in cf.xpath("//field[@name]"):
            #             modifiers = field.attrib.get('modifiers', '')
            #             modifiers = json.loads(modifiers) if modifiers else {}
            #             modifiers.update({'readonly': True})
            #             field.attrib['modifiers'] = json.dumps(modifiers)
            # # Gán lại 'arch' cho res với các thay đổi mới
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res


    def change_account_status(self):
        self.sudo().write({'state': 'close'})
        self.date_close = fields.Datetime.now()
        self.account_link.sudo().write({'active': False})

    def reset_password(self):
        return self.account_link.sudo().action_reset_password()

    def action_cancel_reopen_account(self):
        for profile in self:
            if profile.active in ['active', 'False']:
                profile.write({'state': 'cancelled_reopen_account', 'cancelled_reopen_account': True})

    def action_reopening(self, reason_reopening=None):
        # Khi ấn button Gửi duyệt sẽ chuyển từ draft sang pending
        orders = self.filtered(lambda s: s.state == 'close')
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
            message_body = "Đã gửi phê duyệt mở lại tài khoản."
            self.message_post(body=message_body, subtype_id=self.env['ir.model.data'].xmlid_to_res_id('mail.mt_note'))
            orders.sudo().write({'state': 'wait_reopen'})
            if reason_reopening:
                # nếu có lý do từ chối thì gán lý do từ chối vào trường reason_refusal
                self.reason_reopening = reason_reopening
            return {'type': 'ir.actions.client', 'tag': 'reload'}
        else:
            raise ValidationError("Lỗi không tìm thấy luồng!")

    def see_own_opening_record(self):
        """Nhìn thấy những hồ sơ user được cấu hình"""
        profile = self.env['hr.employee'].sudo().search([('state', '!=', 'close')])
        for p in profile:
            if self.env.user.id in p.approved_link.approve.ids:
                p.can_see_opening_record = True
            else:
                p.can_see_opening_record = False

    def logic_button_opening(self):
        """Nhìn thấy button khi đến lượt phê duyệt"""
        profile = self.env['hr.employee'].sudo().search([('state', '=', 'wait_reopen')])
        for p in profile:
            # list_id lưu id người đang đến lượt
            query = f"""
                    SELECT approve
                    FROM hr_approval_flow_profile where profile_id = {p.id}
                    AND (
                      (step = (
                        SELECT MIN(step)
                        FROM hr_approval_flow_profile
                        WHERE approve_status = 'pending' AND obligatory = true
                        AND profile_id = {p.id}
                      ))
                      OR
                      (excess_level = true AND step = (
                        SELECT MIN(step)
                        FROM hr_approval_flow_profile
                        WHERE approve_status = 'pending' AND profile_id = {p.id}
                        AND excess_level = true
                      ))
                    );
                """
            self._cr.execute(query)
            list_id = self._cr.fetchall()
            list_id_last = [i[0] for i in list_id]
            if self.env.user.id in list_id_last:
                p.can_see_button_opening = True
            else:
                p.can_see_button_opening = False