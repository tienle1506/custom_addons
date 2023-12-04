from odoo import models, fields, api, _
import re
from odoo.exceptions import ValidationError
from lxml import etree
import json
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
        context = self.env.context or {}
        emp_domain = []
        if context.get('parent_department_id', False):
            emp_domain = [('department_id', '=', context.get('parent_department_id'))]
        if context.get('parent_department_id_le', False):
            department_id = context.get('parent_department_id_le', False)[0][2]
            emp_domain = [('department_id', 'in', department_id)]
        return super(EmployeeProfile, self)._name_search(name, args=args + emp_domain, operator=operator,
                                                                  limit=limit)


    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        context = self.env.context or {}
        emp_domain = []
        if context.get('parent_department_id', False):
            emp_domain = [('department_id', '=', context.get('parent_department_id'))]
        if context.get('parent_department_id_le', False):
            emp_domain = [('department_id', 'in', context.get('parent_department_id_le'))]
        return super(EmployeeProfile, self).search_read(domain=domain + emp_domain, fields=fields,
                                                                  offset=offset, limit=limit, order=order)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        context = self.env.context or {}
        emp_domain = []
        if context.get('parent_department_id', False):
            emp_domain = [('department_id', '=', context.get('parent_department_id'))]
        if context.get('parent_department_id_le', False):
            emp_domain = [('department_id', 'in', [context.get('parent_department_id_le')])]
        return super(EmployeeProfile, self).read_group(domain + emp_domain, fields, groupby, offset=offset,
                                                                 limit=limit, orderby=orderby, lazy=lazy)
