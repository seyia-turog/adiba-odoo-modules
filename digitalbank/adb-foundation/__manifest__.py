# -*- coding: utf-8 -*-
{
    'name': "ADIBA Digital Bank",

    'summary': """
        Simple Bank-as-a-Service Platform
        """,

    'description': """
        Simple Bank-as-a-Service Platform
    """,

    'author': "TUROG Technologies",
    'website': "http://www.turog.com.ng",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Administration',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
        'adb-general',
        'adb-accounts',
        'adb-content',
        'adb-transactions',
        'adb-devices'
    ],

    'pre_init_hook': '_pre_init_conflict_check',


    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/menu.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    "auto_install": False
}
