# -*- coding:utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import Warning, ValidationError
from datetime import timedelta
class DATNTangCa(models.Model):
    _name = "datn.tangca"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = u'Đăng ký tăng ca'
    _order = "date_from DESC, date_to DESC"

    name = fields.Char(string='Name', required=True, default='')
    nguoi_duyet = fields.Many2many('hrm.employee.profile', 'employee_duyet_tang_ca_rel', 'tang_ca_id', 'employee_id', string="Người duyệt")
    employee_id = fields.Many2one('hrm.employee.profile', string="Nhân viên", ondelete='cascade', default=lambda self: self._default_employee())
    block_id = fields.Many2one('hrm.blocks', string="khối", ondelete='cascade', related='employee_id.block_id', store=True)
    date_from = fields.Date(u'Từ ngày', widget='date', format='%Y-%m-%d')
    date_to = fields.Date(u'Đến ngày', widget='date', format='%Y-%m-%d', compute='_compute_dateto', store=True)
    state = fields.Selection([('draft', u'Gửi phê duyệt'), ('confirmed', u'Chờ phê duệt'), ('approved', u'Phê duyệt'), ('refused', u'Từ chối')],
                             string=u'Trạng thái', default='draft', track_visibility='always')
    ly_do = fields.Text(u"Lý do")
    so_gio_tang_ca = fields.Float(string='So giờ tăng ca', default=0)
    create_date = fields.Date(u'Từ ngày', widget='date', format='%Y-%m-%d', default=fields.Date.today)

    def read(self, fields=None, load='_classic_read'):
        self.check_access_rule('read')
        return super(DATNTangCa, self).read(fields, load=load)

    def search(self, args, offset=0, limit=None, order=None, count=False):
        domain = []
        return super(DATNTangCa, self).search(domain + args, offset, limit, order, count=count)

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        emp_domain = self.check_employee_view()
        return super(DATNTangCa, self)._name_search(name, args=args + emp_domain, operator=operator,
                                                                  limit=limit)


    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        emp_domain = self.check_employee_view()
        return super(DATNTangCa, self).search_read(domain=domain + emp_domain, fields=fields,
                                                                  offset=offset, limit=limit, order=order)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        emp_domain = self.check_employee_view()
        return super(DATNTangCa, self).read_group(domain + emp_domain, fields, groupby, offset=offset,
                                                                 limit=limit, orderby=orderby, lazy=lazy)
    def check_employee_view(self):
        context = self.env.context or {}
        emp_domain = []
        user = self.env.user
        employee_id = self.env['hrm.employee.profile'].search([('acc_id', '=', user.id)], limit=1)
        if context.get('view_from_action', False):
            emp_domain = [('employee_id', '=', employee_id.id)]
        if context.get('view_from_action_phe_duyet', False):
            emp_domain = [('nguoi_duyet', '=', employee_id.id), ('state', '!=', 'darft')]
        return emp_domain

    @api.model
    def _default_employee(self):
        user = self.env.user
        employee = self.env['hrm.employee.profile'].search([('acc_id', '=', user.id)], limit=1)
        return employee

    @api.constrains('so_gio_tang_ca taw')
    def _check_date_duong(self):
        if self.so_gio_tang_ca < 0:
            raise ValidationError(_(u"Số giờ tăng ca phải lớn hơn 0, yêu cầu nhập lại."))

    def action_draft(self):
        self.state = 'draft'
    def action_send_approve(self):
        self.state = 'confirmed'

    def action_refuse(self):
        self.state = 'refused'

    def action_approve(self):
        self.state = 'approved'
