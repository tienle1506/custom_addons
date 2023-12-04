# -*- coding:utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import Warning, ValidationError, UserError, AccessError

dict_role = {
    'Đơn xin nghỉ': 'DXN',
}


class HrRequestType(models.Model):
    _name = 'hr.request.type'
    _description = 'Loại yêu cầu'
    _rec_name = 'name'
    _inherit = ['mail.thread']

    code = fields.Char(string="Mã", default='DXN')
    name = fields.Char(string=u"Tên", default='Đơn xin nghỉ')
    description = fields.Text(string="Mô tả", default='Đơn xin nghỉ')
    image = fields.Binary(string="Hình ảnh", attachment=True,
                          filters="*.png,*.jpeg,*.jpg,*.bmp",
                          default=lambda self: self._default_image())

    my_request = fields.Integer(string=u"Yêu cầu của tôi", compute='_get_data_for_request_type')
    need_approve = fields.Integer(string=u"Cần phê duyệt", compute='_get_data_for_request_type')
    is_active = fields.Boolean("Trạng thái", default=True)
    index = fields.Integer("Thứ tự", default=0)

    def _default_image(self):
        return self.env['ir.attachment'].search([('name', '=', 'change_shift.png')], limit=1).datas

    def _get_data_for_request_type(self):
        emp = self.env['hr.employee'].search([('acc_id', '=', self._uid)])
        for d in self:
            d.need_approve, d.my_request = d._count_data(d, emp)

    def _count_data(self, request, emp):
        need_approve = 0
        my_request = 0
        if request.code == 'DXN':
            if emp:
                self.env.cr.execute("""
                    SELECT count(*) FROM datn_dangkynghi dkn
                    LEFT JOIN employee_duyet_nghi_them_rel dnr ON dnr.nghi_id = dkn.id
                    WHERE dnr.employee_id = %s AND state = 'confirmed'
                """, (emp.id,))
                data = self.env.cr.dictfetchone()
                if data:
                    need_approve = data['count']
                # ----- lấy số lượng yêu cầu của tôi
                self.env.cr.execute("""
                    SELECT count(*) FROM datn_dangkynghi
                    WHERE employee_id = %s and state = 'confirmed'
                """, (emp.id,))
                data = self.env.cr.dictfetchone()
                if data:
                    my_request = data['count']
        elif request.code == 'PTC':
            if emp:
                self.env.cr.execute("""
                    SELECT count(*) FROM datn_tangca dkn
                    LEFT JOIN employee_duyet_tang_ca_rel dnr ON dnr.tang_ca_id = dkn.id
                    WHERE dnr.employee_id = %s AND state = 'confirmed'
                """, (emp.id,))
                data = self.env.cr.dictfetchone()
                if data:
                    need_approve = data['count']
                # ----- lấy số lượng yêu cầu của tôi
                self.env.cr.execute("""
                    SELECT count(*) FROM datn_tangca
                    WHERE employee_id = %s and state = 'confirmed'
                """, (emp.id,))
                data = self.env.cr.dictfetchone()
                if data:
                    my_request = data['count']

        elif request.code == 'PDCC':
            if emp:
                self.env.cr.execute("""
                    SELECT count(*) FROM datn_hr_checkin_checkout_line dkn
                    LEFT JOIN employee_duyet_checkin_checkout_rel dnr ON dnr.checkin_checkout_id = dkn.id
                    WHERE dnr.employee_id = %s AND state = 'confirmed'
                """, (emp.id,))
                data = self.env.cr.dictfetchone()
                if data:
                    need_approve = data['count']
                # ----- lấy số lượng yêu cầu của tôi
                self.env.cr.execute("""
                    SELECT count(*) FROM datn_hr_checkin_checkout_line
                    WHERE employee_id = %s and state = 'confirmed'
                """, (emp.id,))
                data = self.env.cr.dictfetchone()
                if data:
                    my_request = data['count']
        return need_approve, my_request

    def open_approve_request(self):
        action = self._get_action()
        if not action:
            raise ValidationError(_("Không có hành động tương ứng với yêu cầu. Vui lòng thử lại"))
        return action

    def open_my_request(self):
        action = self._get_action(my_request=True)
        if not action:
            raise ValidationError(_("Không có hành động tương ứng với yêu cầu. Vui lòng thử lại"))
        return action

    def _get_action(self, is_form=False, my_request=False):
        if my_request:
            context = {
                'view_from_action': 'datn_loai_phe_duyet'
            }
        else:
            context = {
                'view_from_action_phe_duyet': 1
            }
        if self.code == 'DXN':
            action = self.env.ref('hrm_chamcong.datn_dang_ky_nghi_nhanvien_action').sudo().read()[0]
            action['context'] = context
        elif self.code == 'PTC':
            action = self.env.ref('hrm_chamcong.datn_dang_ky_tang_ca_nhan_vien_action').sudo().read()[0]
            action['context'] = context
        elif self.code == 'PDCC':
            action = self.env.ref('hrm_chamcong.datn_hrm_checkin_checkout_calendar_cnf1').sudo().read()[0]
            action['context'] = context
        return action
