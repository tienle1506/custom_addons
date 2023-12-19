from odoo import models, fields, api, _

class EmployeeProfileKySo(models.Model):
    _inherit = 'hr.employee'
    _description = 'Bảng thông tin nhân viên'

    def get_domain(self, context):
        # Thực hiện các công việc bổ sung trước khi gọi hàm cũ
        result2 = super(EmployeeProfileKySo, self).get_domain(context)
        emp_domain = result2
        # Thực hiện các công việc bổ sung sau khi gọi hàm cũ
        if context.get('list_employee_phe_duyet', False):
            if context.get('department_phe_duyet', False):
                if context.get('list_employee_phe_duyet') == 'Ký số':
                    SQL = '''    
                            SELECT DISTINCT employee.id
                            FROM hr_employee employee
                            JOIN res_users user1 ON employee.user_id = user1.id
                            JOIN res_groups_users_rel group_user_rel ON user1.id = group_user_rel.uid
                            JOIN res_groups groups ON group_user_rel.gid = groups.id
                            WHERE (groups.name = 'Ký nháy' OR groups.name = 'Đóng dấu cơ quan' OR groups.name = 'Ký tên cơ quan') AND employee.department_id IN (
                              SELECT unnest(get_list_parent_department((SELECT department_id FROM hr_employee WHERE id = %s)))
                            );
                            ''' % (context.get('department_phe_duyet'))
                    self.env.cr.execute(SQL)
                    datas = self.env.cr.dictfetchall()
                    if datas:
                        result = [item['id'] for item in datas]
                        emp_domain = [('id', 'in', result)]

        return emp_domain
