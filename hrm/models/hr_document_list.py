import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessDenied
from . import constraint



class DocumentListConfig(models.Model):
    _name = 'hrm.document.list.config'
    _description = 'Cấu hình danh sách tài liệu'

    name = fields.Char(string='Tên hiển thị', required=True)

    def default_type_block(self):
        return 'BLOCK_OFFICE_NAME' if self.env.user.block_id == 'BLOCK_OFFICE_NAME' else 'BLOCK_COMMERCE_NAME'

    type_block = fields.Selection(constraint.TYPE_BLOCK, string='Khối', required=True, default=default_type_block)
    department_id = fields.Many2one('hr.department', string='Phòng ban', tracking=True)

    document_list = fields.One2many('hrm.document.list', 'document_id', string='Danh sách tài liệu')
    related = fields.Boolean(compute='_compute_related_')

    see_record_with_config = fields.Boolean(default=True)
    update_confirm_document = fields.Selection(selection=constraint.UPDATE_CONFIRM_DOCUMENT, string="Cập nhật tài liệu")

    # các field lưu id của tài liệu tương ứng với cấu hình áp dụng cho HSNS
    new_config = fields.One2many('hrm.document.list', 'new_id')
    not_approved_and_new = fields.One2many('hrm.document.list', 'not_approved_and_new_id')
    all = fields.One2many('hrm.document.list', 'all_id')

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

    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     self.env['hrm.utils']._see_record_with_config('hrm.document.list.config')
    #     return super(DocumentListConfig, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
    #                                        submenu=submenu)

    @api.onchange('type_block')
    def onchange_type_block(self):
        for rec in self:
            if rec.type_block == 'BLOCK_OFFICE_NAME':
                if self.env.user.department_id:
                    list_sys_com = self.env['hr.department'].search([('id', 'child_of', self.env.user.department_id.ids)])
                else:
                    list_sys_com = self.env['hr.department'].search([('type_block', '=', 'BLOCK_OFFICE_NAME')])
                return {'domain': {'department_id': [('id', 'in', list_sys_com.ids)]}}
    @api.onchange('department_id', 'type_block')
    def _default_job_department(self):
        self.job_id = False
        if self.type_block == 'BLOCK_COMMERCE_NAME':
            self.department_id = False
            position = self.env['hr.job'].search([('type_block', '=', 'BLOCK_COMMERCE_NAME')])
            return {'domain': {'job_id': [('id', 'in', position.ids)]}}
        elif self.type_block == 'BLOCK_OFFICE_NAME' and self.department_id:
            position = self.env['hr.job'].search([('department_id', '=', self.department_id.id)])
            return {'domain': {'job_id': [('id', 'in', position.ids)]}}


    job_id = fields.Many2one('hr.job', string='Vị trí công việc', domain=_default_job_department)

    @api.onchange('document_list')
    def set_sequence(self):
        i = 1
        for document in self.document_list:
            document.sequence = i
            i += 1

    @api.onchange('document_list')
    def _check_duplicate_document(self):
        list_document = [record.doc for record in self.document_list]
        seen = set()
        for item in list_document:
            if item in seen:
                raise ValidationError(f'Hồ sơ {item.name} đã có trong danh sách tài liệu')
            else:
                seen.add(item)

    @api.constrains('name', 'job_id')
    def check_duplicate_document_config(self):
        """hàm này để kiểm tra trùng lặp cấu hình danh sách tài liệu cho các đối tượng được áp dụng"""
        def check_exist_object(position_id=False):
            check = self.search([('type_block', '=', self.type_block), ('id', 'not in', [self.id, False]),('job_id', '=', position_id)])
            return check.ids

        if self.job_id and check_exist_object(position_id=self.job_id.id):
            raise ValidationError(f"Đã có cấu hình danh sách tài liệu cho vị trí {self.job_id.name}")

    # def unlink(self):
    #     for record in self:
    #         document = self.env['hr.employee'].sudo().search([('document_config', '=', record.id)])
    #         if document:
    #             raise AccessDenied("Không thể xoá " + record.name)
    #     return super(DocumentListConfig, self).unlink()

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
    @api.constrains('document_list')
    def check_approval_flow_link(self):
        """Kiểm tra xem danh sách tài liệu có phần tử nào chưa, và ít nhất phải có 1 tài liệu tích bắt buộc"""
        if not self.document_list:
            raise ValidationError('Không thể tạo khi không có tài liệu nào trong danh sách tài liệu.')
        else:
            list_check = []
            for item in self.document_list:
                if item.obligatory:
                    list_check.append(True)
            if not any(list_check):
                raise ValidationError('Cần có ít nhất một tài liệu bắt buộc.')

    def action_update_document(self, object_update):
        # self.sudo().write({'update_confirm_document': object_update})
        if object_update == 'all':
            self.env['hr.employee'].sudo().search([('document_config', '=', self.id)]).write(
                {'type_update_document': 'all'}
            )
            self.all = [(6, 0, self.document_list.ids)]
        elif object_update == 'not_approved_and_new':
            self.env['hr.employee'].sudo().search([
                ('document_config', '=', self.id),
                ('state', 'in', ('draft','pending'))
            ]).write(
                {'type_update_document': 'not_approved_and_new'}
            )
            self.not_approved_and_new = [(6, 0, self.document_list.ids)]
        else:
            self.env['hr.employee'].sudo().search([
                ('document_config', '=', self.id),
                ('state', '=', 'draft')
            ]).write(
                {'type_update_document': 'new'}
            )
            self.new_config = [(6, 0, self.document_list.ids)]

class DocumentList(models.Model):
    _name = 'hrm.document.list'
    _description = 'Danh sách tài liệu'


    document_id = fields.Many2one('hrm.document.list.config')
    new_id = fields.Many2one('hrm.document.list.config')
    not_approved_and_new_id = fields.Many2one('hrm.document.list.config')
    all_id = fields.Many2one('hrm.document.list.config')
    sequence = fields.Integer(string="STT")
    doc = fields.Many2one('hr.documents', string='Tên tài liệu')
    name = fields.Char(related='doc.name')
    obligatory = fields.Boolean(string='Bắt buộc')



