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
    'depends': ['hrm', 'base', 'mail'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/datn_cong_thuc_te.xml',
        'views/datn_chamcong.xml',
        'views/datn_checkin_checkout.xml',
        'views/datn_hrm_le_tet.xml',
        'views/hr_employee.xml',
        'views/datn_cong_tang_cuong.xml',
        'views/datn_loai_nghi.xml',
        'views/datn_dang_ky_nghi_nhanvien.xml',
        'views/datn_phe_duyet.xml',
        'views/datn_create_view_pheduyet.xml',
        'views/datn_dangky_tangca_nhanvien.xml',
        'views/datn_hrm_checkin_checkout_nhanvien.xml',
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
