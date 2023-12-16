{
    'name': "Ký số",
    'version': '1.9.1',
    'category': 'Technical Settings',
    'description': """VNPT Ký số""",
    'author': 'nhatnt',
    'website': '',
    'sequence': 10000,
    "depends": ['base', 'hr', 'hrm_tinh_luong'],
    'data': [
        'data/data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/cauhinh_kyso_canhan.xml',
        'views/datn_kyso_file.xml',
        'views/templates.xml',
        'views/menu_item.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': ['static/src/xml/*.xml'],
}
# -*- encoding: utf-8 -*-
