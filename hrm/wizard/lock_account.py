from odoo import models, fields


class LockAccount(models.TransientModel):
    _name = "lock.account"
    _description = "Khóa TK nhân sự"

    def action_lock_personnel_account(self):
        leads = self.env['hr.employee'].sudo().browse(self.env.context.get('active_ids'))
        return leads.change_account_status()