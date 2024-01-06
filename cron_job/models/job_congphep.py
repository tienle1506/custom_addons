from odoo import api, fields, models
from datetime import datetime
import os

class TestCronJob(models.Model):
    _name = 'cron.job.cong.phep'

    @api.model
    def run(self):
        employees = self.env['hr.employee'].search([('work_start_date', '<', fields.Date.today())])
        updated_employee_ids = []
        for employee in employees:
            cong_phep = 0
            ngay_vao_lam = employee.work_start_date
            nam_vao_lam = ngay_vao_lam.year
            thang_vao_lam = ngay_vao_lam.month
            ngay_hien_tai = fields.Date.today()
            thang_hien_tai = ngay_hien_tai.month
            nam_hien_tai = ngay_hien_tai.year

            if nam_vao_lam == nam_hien_tai:
                cong_phep = thang_hien_tai - thang_vao_lam
            else:
                cong_phep = thang_hien_tai

            cong_them = self.env['datn.cong.tang.cuong.line'].search([
                ('cong_them_id.state', '=', 'confirmed'),
                ('year', '=', nam_hien_tai),
                ('employee_id', '=', employee.id)
            ])

            if cong_them:
                cong_phep += sum(cong.cong_them or 0 for cong in cong_them)

            values = {'so_ngay_duoc_phan_bo': cong_phep}
            if cong_phep == 1:
                values['so_ngay_da_nghi'] = 0

            employee.write(values)