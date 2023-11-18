from odoo import api, fields, models
from datetime import datetime
import os

class TestCronJob(models.Model):
    _name = 'cron.job.cong.phep'

    @api.model
    def run(self):
        cr = self.env.cr

        # Lấy ngày hiện tại
        ngay_hien_tai = datetime.now()

        # Lấy thông tin về tháng từ ngày hiện tại
        thang_hien_tai = ngay_hien_tai.month
        nam_hien_tai = ngay_hien_tai.year

        SQL = ''
        SQL += '''SELECT*FROM hrm_employee_profile Where work_start_date < '%s' ''' % (ngay_hien_tai.date())
        cr.execute(SQL)
        datas = cr.dictfetchall()
        if datas:
            datas = datas
        else:
            datas = []

        for i in range(len(datas)):
            cong_phep = 0
            ngay_vao_lam = datas[i].get('work_start_date')
            nam_vao_lam = ngay_vao_lam.year
            thang_vao_lam = ngay_vao_lam.month
            if int(nam_vao_lam) == int(nam_hien_tai):
                cong_phep = int(thang_hien_tai) - int(thang_vao_lam)
            else:
                cong_phep = int(thang_hien_tai)
            SQL2 = '''SELECT SUM(cl.cong_them) as cong_them FROM datn_cong_tang_cuong_line cl
                        LEFT JOIN datn_cong_tang_cuong c ON c.id = cl.cong_them_id
                        WHERE c.state = 'confirmed' AND cl.year = '%s'
                        AND cl.employee_id = %s'''%(nam_hien_tai, datas[i].get('id') )
            cr.execute(SQL2)
            data_cong_them = cr.dictfetchall()
            if data_cong_them:
                cong_phep += data_cong_them[0].get('cong_them') if  data_cong_them[0].get('cong_them') else 0
            SQL1 = '''UPDATE hrm_employee_profile
                            SET so_ngay_duoc_phan_bo = %s
                            WHERE id = %s;''' % (cong_phep, datas[i].get('id'))
            cr.execute(SQL1)
