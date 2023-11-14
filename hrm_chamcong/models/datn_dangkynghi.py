# -*- coding:utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import Warning, ValidationError




# class DATNDangKyNghi(models.Model):
#     _name = "datn.dangkynghi"
#     _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
#     _description = u'Đăng ký nghie phép'
#     _order = "date_from DESC, date_to DESC"
#
#     nguoi_duyet = fields.Many2many('hrm.employee.profile', 'nguoiduynghi', 'employee_id', 'nghi_id', string="Người duyệt")
#     employee = fields.Many2one('hrm.employee.profile', string="Khối", ondelete='cascade')
#     date_from = fields.Date(u'Từ ngày', widget='date', format='%Y-%m-%d')
#     date_to = fields.Date(u'Đến ngày', widget='date', format='%Y-%m-%d')
#     state = fields.Selection([('draft', u'Gửi phê duyệt'), ('confirmed', u'Chờ phê duệt'), ('approved', u'Phê duyệt'), ('reject', u'Từ chối')],
#                              string=u'Trạng thái', default='draft', track_visibility='always')
#     ly_do = fields.Text(u"Lý do")
#     loai_nghi = fields.Many2one(u"hrm.loainghi.nghi", 'Loại nghỉ')
#     so_ngay_da_nghi = fields.Float(u"Số ngày phép đã nghỉ")
#     so_ngay_duoc_phan_bo = fields.Float(u"Số ngày phép được phân bổ")
#     so_ngay_con_lai = fields.Float(u"Số ngày nghỉ phép còn lại")



class HrEmplyee(models.Model):
    _inherit = "hrm.employee.profile"
    so_ngay_da_nghi = fields.Float(u"Số ngày phép đã nghỉ")
    so_ngay_duoc_phan_bo = fields.Float(u"Số ngày phép được phân bổ")
    so_ngay_con_lai = fields.Float(u"Số ngày nghỉ phép còn lại")

    



