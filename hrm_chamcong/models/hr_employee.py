from odoo import models, fields, api, _

class EmployeeProfile(models.Model):
    _inherit = 'hr.employee'
    _description = 'Bảng thông tin nhân viên'

    def read(self, fields=None, load='_classic_read'):
        self.check_access_rule('read')
        return super(EmployeeProfile, self).read(fields, load=load)

    def search(self, args, offset=0, limit=None, order=None, count=False):
        domain = []
        return super(EmployeeProfile, self).search(domain + args, offset, limit, order, count=count)

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        emp_domain = self.get_domain(self.env.context or {})
        return super(EmployeeProfile, self)._name_search(name, args=args + emp_domain, operator=operator, limit=limit)

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        emp_domain = self.get_domain(self.env.context or {})
        return super(EmployeeProfile, self).search_read(domain=domain + emp_domain, fields=fields, offset=offset,
                                                        limit=limit, order=order)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        emp_domain = self.get_domain(self.env.context or {})
        return super(EmployeeProfile, self).read_group(domain + emp_domain, fields, groupby, offset=offset, limit=limit,
                                                       orderby=orderby, lazy=lazy)

    def get_domain(self, context):
        emp_domain = []
        if context.get('parent_department_id', False):
            emp_domain = [('department_id', 'child_of', context.get('parent_department_id'))]
        if context.get('parent_department_id_le', False):
            emp_domain = [('department_id', 'child_of', context.get('parent_department_id_le')[0][2])]
        if context.get('list_employee_phe_duyet', False):
            if context.get('department_phe_duyet', False):
                SQL = '''
                SELECT employee.id
                FROM hr_employee employee
                JOIN res_users user1 ON employee.user_id = user1.id
                JOIN res_groups_users_rel group_user_rel ON user1.id = group_user_rel.uid
                JOIN res_groups groups ON group_user_rel.gid = groups.id
                WHERE groups.name = '%s' AND employee.department_id IN (
                  SELECT unnest(get_list_parent_department((SELECT department_id FROM hr_employee WHERE id = %s)))
                );
                ''' % (context.get('list_employee_phe_duyet'), context.get('department_phe_duyet'))
                self.env.cr.execute(SQL)
                datas = self.env.cr.dictfetchall()
                if datas:
                    result = [item['id'] for item in datas]
                    emp_domain = [('id', 'in', result)]

        return emp_domain
