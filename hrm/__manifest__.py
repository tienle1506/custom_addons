{
    'name': "HRM",

    'summary': """
        Quản lý thông tin nhân viên.
    """,

    'description': """
        Long description of module's purpose
    """,

    'author': "",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',
    'application': True,
    'sequence': -100,
    # any module necessary for this one to work correctly
    'depends': ['base', 'utm', 'mail'],

    # always loaded
    'data': [
        'wizard/approval_reason_refusal.xml',
        'wizard/lock_account.xml',
        'wizard/reason_reopening_account.xml',
        'wizard/confirm_update_document.xml',
        'wizard/multiple_update_image.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data_department.xml',
        'views/hr_department_view.xml',
        'views/hr_teams.xml',
        'views/images_view.xml',
        'views/hr_position_view.xml',
        'views/hr_employee_inherit.xml',
        'views/approval_view.xml',
        'views/documents_view.xml',
        'views/document_list_view.xml',
        'views/document_declaration_view.xml',
        'views/hr_approval_flow_config_view.xml',
        'views/sequence_employee_code.xml',
        'views/hr_users_view.xml',
        'views/hr_employee_view.xml',
        'views/menu.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
# -*- coding: utf-8 -*-
