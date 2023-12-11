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
    nguoi_duyet = fields.Many2many('hr.employee', 'employee_duyet_tang_ca_rel', 'tang_ca_id', 'employee_id', string="Người duyệt")
    employee_id = fields.Many2one('hr.employee', string="Nhân viên", ondelete='cascade', default=lambda self: self._default_employee())
    department_id = fields.Many2one('hr.department', string="Đơn vị/Phòng ban", ondelete='cascade', related='employee_id.department_id', store=True)
    date_from = fields.Date(u'Từ ngày', widget='date', format='%Y-%m-%d')
    date_to = fields.Date(u'Đến ngày', widget='date', format='%Y-%m-%d', compute='_compute_dateto', store=True)
    state = fields.Selection([('draft', u'Soạn thảo'), ('confirmed', u'Chờ phê duệt'), ('approved', u'Phê duyệt'), ('refused', u'Từ chối')],
                             string=u'Trạng thái', default='draft', track_visibility='always')
    ly_do = fields.Text(u"Lý do")
    so_gio_tang_ca = fields.Float(string='Số giờ tăng ca', default=0)
    create_date = fields.Date(u'Từ ngày', widget='date', format='%Y-%m-%d', default=fields.Date.today)

    @api.constrains('date_from', 'date_to')
    def check_date_from_date_to(self):
        if self.date_to.month != self.date_from.month:
            raise ValidationError("Ngày tăng ca phải nằm trong cùng một tháng")
        if self.id:
            SQL = ''
            SQL += '''SELECT * FROM datn_tangca WHERE id != %s and employee_id = %s AND ((date_from BETWEEN '%s' AND '%s') 
            OR (date_to BETWEEN '%s' AND '%s')) '''%(self.id, self.employee_id.id, self.date_from, self.date_to,self.date_from, self.date_to)
            self.env.cr.execute(SQL)
            employees = self.env.cr.dictfetchall()
        else:
            SQL = ''
            SQL += '''SELECT * FROM datn_tangca WHERE employee_id = %s AND ((date_from BETWEEN '%s' AND '%s') 
                        OR (date_to BETWEEN '%s' AND '%s')) ''' % (
            self.employee_id.id, self.date_from, self.date_to, self.date_from, self.date_to)
            self.env.cr.execute(SQL)
            employees = self.env.cr.dictfetchall()
        if employees:
            raise ValidationError("Ngày tăng ca của bạn đang tạo có một ngày khác đã được tạo, năm trong khoảng này")

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
        employee_id = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
        if context.get('view_from_action', False):
            emp_domain = [('employee_id', '=', employee_id.id)]
        if context.get('view_from_action_phe_duyet', False):
            emp_domain = [('nguoi_duyet', '=', employee_id.id), ('state', '!=', 'draft')]
        return emp_domain

    @api.model
    def _default_employee(self):
        user = self.env.user
        employee = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
        return employee

    @api.constrains('so_gio_tang_ca taw')
    def _check_date_duong(self):
        if self.so_gio_tang_ca < 0:
            raise ValidationError(_(u"Số giờ tăng ca phải lớn hơn 0, yêu cầu nhập lại."))

    def action_draft(self):
        self.state = 'draft'
    def action_send_approve(self):
        nguoi_duyet = []
        for emp in self.nguoi_duyet:
            if emp.personal_email:
                nguoi_duyet.append(emp.personal_email.strip())
        header = '''Thông báo phê duyệt đơn tăng ca của %s''' % (self.employee_id.name)
        content = u'Nhân viên %s tạo đơn tăng ca \nLý do: %s \nSố giờ tăng ca:%s\nTừ ngày: %s - đến ngày: %s \nTrang web: http://localhost:8088/web' % (
        str(self.employee_id.name), str(self.ly_do), str(self.so_gio_tang_ca),
        self.date_from.strftime('%d/%m/%Y'), self.date_to.strftime('%d/%m/%Y'))
        if nguoi_duyet and len(nguoi_duyet) > 0:
            self.env['my.mail.sender'].send_mail_to_customer(nguoi_duyet, header, content)
        self.state = 'confirmed'

    def action_refuse(self):
        self.state = 'refused'

    def action_approve(self):
        self.state = 'approved'

    def unlink(self):
        # Kiểm tra điều kiện trước khi thực hiện unlink
        if self.state == 'draft':
            # Thực hiện unlink chỉ khi điều kiện đúng
            super().unlink()  # Gọi phương thức unlink gốc
        else:
            # Xử lý khi điều kiện không đúng
            # ví dụ:
            raise ValidationError("Không thể xoá bản ghi do bản ghi đã được ghi nhận.")
