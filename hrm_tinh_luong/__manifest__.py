{
    'name': "HRM TINH LUONG",

    'summary': """
        Quản lý tính lương doanh nghiệp.
    """,

    'description': """
        HRM TINH LUONG
    """,

    'author': "Trong Nhat",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'HRM TINH LUONG',
    'version': '0.1',
    'application': True,
    'sequence': -100,
    # any module necessary for this one to work correctly
    'depends': ['hrm_chamcong'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/datn_quytacluong.xml',
        'views/datn_luongthang.xml',
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
