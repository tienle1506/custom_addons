# -*- coding:utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import Warning, ValidationError
from datetime import timedelta
class DATNDangKyNghi(models.Model):
    _name = "datn.dangkynghi"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = u'Đăng ký nghỉ phép'
    _order = "date_from DESC, date_to DESC"

    name = fields.Char(string='Name', required=True, default='')
    nguoi_duyet = fields.Many2many('hrm.employee.profile', 'employee_duyet_nghi_them_rel', 'nghi_id', 'employee_id', string="Người duyệt")
    employee_id = fields.Many2one('hrm.employee.profile', string="Nhân viên", ondelete='cascade', default=lambda self: self._default_employee())
    block_id = fields.Many2one('hrm.blocks', string="khối", ondelete='cascade', related='employee_id.block_id', store=True)
    date_from = fields.Date(u'Từ ngày', widget='date', format='%Y-%m-%d')
    date_to = fields.Date(u'Đến ngày', widget='date', format='%Y-%m-%d', compute='_compute_dateto', store=True)
    state = fields.Selection([('draft', u'Gửi phê duyệt'), ('confirmed', u'Chờ phê duệt'), ('approved', u'Phê duyệt'), ('refused', u'Từ chối')],
                             string=u'Trạng thái', default='draft', track_visibility='always')
    ly_do = fields.Text(u"Lý do")
    so_ngay_nghi = fields.Float(u"Số ngày nghỉ", related='loai_nghi.ngay_ap_dung', store=True)
    loai_nghi = fields.Many2one(u"datn.loai.nghi", 'Loại nghỉ')
    so_ngay_da_nghi = fields.Float(u"Số ngày phép đã nghỉ", related='employee_id.so_ngay_da_nghi', store=True)
    so_ngay_duoc_phan_bo = fields.Float(u"Số ngày phép được phân bổ", related='employee_id.so_ngay_duoc_phan_bo', store=True)
    so_ngay_con_lai = fields.Float(u"Số ngày nghỉ phép còn lại", related='employee_id.so_ngay_con_lai', store=True)
    create_date = fields.Date(u'Từ ngày', widget='date', format='%Y-%m-%d', default=fields.Date.today)

    def read(self, fields=None, load='_classic_read'):
        self.check_access_rule('read')
        return super(DATNDangKyNghi, self).read(fields, load=load)

    def search(self, args, offset=0, limit=None, order=None, count=False):
        domain = []
        return super(DATNDangKyNghi, self).search(domain + args, offset, limit, order, count=count)

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        emp_domain = self.check_employee_view()
        return super(DATNDangKyNghi, self)._name_search(name, args=args + emp_domain, operator=operator,
                                                                  limit=limit)


    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        emp_domain = self.check_employee_view()
        return super(DATNDangKyNghi, self).search_read(domain=domain + emp_domain, fields=fields,
                                                                  offset=offset, limit=limit, order=order)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        emp_domain = self.check_employee_view()
        return super(DATNDangKyNghi, self).read_group(domain + emp_domain, fields, groupby, offset=offset,
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
    @api.depends('so_ngay_nghi', 'date_from')
    def _compute_dateto(self):
        for record in self:
            if record.so_ngay_nghi and record.date_from:
                date_from = fields.Datetime.from_string(record.date_from)
                date_to = date_from + timedelta(days=record.so_ngay_nghi)
                record.date_to = fields.Date.to_string(date_to)
    @api.model
    def _default_employee(self):
        user = self.env.user
        employee = self.env['hrm.employee.profile'].search([('acc_id', '=', user.id)], limit=1)
        return employee
    @api.constrains('so_ngay_nghi')
    def _check_date_duong(self):
        if self.so_ngay_nghi < 0:
            raise ValidationError(_(u"Số ngày nghỉ phải lớn hơn 0, yêu cầu nhập lại."))

    def action_draft(self):
        self.state = 'draft'
    def action_send_approve(self):
        self.state = 'confirmed'

    def action_refuse(self):
        self.state = 'refused'

    def action_approve(self):
        self.state = 'approved'

class DATNLoaiNghi(models.Model):
    _name = 'datn.loai.nghi'
    _description = 'Cấu hình loại nghỉ'

    name = fields.Text(string="Tên loại nghỉ")
    code = fields.Text(string="Mã loại nghỉ")
    ngay_ap_dung = fields.Float(string="Ngày áp dụng", default='1')
    ngay_toi_da = fields.Float(string="Ngày nghỉ tối đa", default='0')
    trang_thai_ap_dung = fields.Boolean(string="Trạng thái áp dụng")
    loai_nghi = fields.Selection([('khongluong', u'Nghỉ không lương'), ('nghicoluong', u'Nghỉ có lương'), ('nghiphep', u'Nghỉ phép')],
                             string=u'Loại nghỉ', default='khongluong', track_visibility='always', required=True)
    note = fields.Text(string="Chú thích")

    _sql_constraints = [('code_loai_nghi_unique', 'unique(code)', 'Mã loại nghỉ đã tồn tại!')]

    @api.constrains('ngay_ap_dung')
    def _check_date_duong(self):
        if self.ngay_ap_dung < 0:
            raise ValidationError(_(u"Ngày áp dụng phải lớn hơn 0, yêu cầu nhập lại."))

    @api.constrains('ngay_toi_da')
    def _check_date_duong_td(self):
        if self.ngay_toi_da < 0:
            raise ValidationError(_(u"Ngày nghỉ tối đa phải lớn hơn 0, yêu cầu nhập lại."))


class HrEmplyee(models.Model):
    _inherit = "hrm.employee.profile"
    so_ngay_da_nghi = fields.Float(u"Số ngày phép đã nghỉ")
    so_ngay_duoc_phan_bo = fields.Float(u"Số ngày phép được phân bổ")
    so_ngay_con_lai = fields.Float(u"Số ngày nghỉ phép còn lại", compute='_compute_ngayconlai', store=True)

    @api.constrains('so_ngay_duoc_phan_bo', so_ngay_da_nghi, so_ngay_con_lai)
    def _check_date_duong_td(self):
        if self.so_ngay_da_nghi and self.so_ngay_duoc_phan_bo:
            if float(self.so_ngay_duoc_phan_bo) - float(self.so_ngay_da_nghi):
                raise ValidationError(_(u"Ngày nghỉ phép không thế vượt quá ngày nghỉ phân bổ."))

    @api.depends('so_ngay_da_nghi', 'so_ngay_duoc_phan_bo')
    def _compute_ngayconlai(self):
        self.so_ngay_con_lai = self.so_ngay_duoc_phan_bo - self.so_ngay_da_nghi





