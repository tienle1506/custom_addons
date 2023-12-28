from odoo import models, fields


class ApprovalReasonRefusal(models.TransientModel):
    _name = "reason.reopening.account"
    _description = "Lý do mở lại"

    reason_reopening = fields.Char(string="Lý do mở lại", required=True)

    def action_reason_reopening(self):
        # lấy bản ghi đang được chọn và gọi action từ chối
        leads = self.env['hr.employee'].sudo().browse(self.env.context.get('active_ids'))
        return leads.action_reopening(self.reason_reopening)