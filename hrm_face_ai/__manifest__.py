{
    'name': "HRM FACE AI",

    'summary': """
        Máy chấm công FaceAi.
    """,

    'description': """
        HRM FACE AI
    """,

    'author': "Trong Nhat",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'HRM FACE AI',
    'version': '0.1',
    'application': True,
    'sequence': -100,
    # any module necessary for this one to work correctly
    'depends': ['hrm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee.xml',
            ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'css': [
        'static/src/css/style.css',
    ],
}
# -*- coding: utf-8 -*-
