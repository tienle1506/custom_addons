{
    'name': "HRM CHAM CONG",

    'summary': """
        Quản lý chấm công doanh nghiệp.
    """,

    'description': """
        HRM CHAM CONG
    """,

    'author': "Trong Nhat",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'HRM CHAM CONG',
    'version': '0.1',
    'application': True,
    'sequence': -100,
    # any module necessary for this one to work correctly
    'depends': ['base', 'utm', 'mail', 'hrm'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu_item.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'css': [
        'static/src/css/style.css',
    ],
}
# -*- coding: utf-8 -*-
