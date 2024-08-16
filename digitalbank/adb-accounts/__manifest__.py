# -*- coding: utf-8 -*-
{
    'name': "adb-accounts",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','adb-general'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/adb_beneficiaries/list.xml',
        'views/adb_card_debits/list.xml',
        'views/adb_card_issuances/list.xml',
        'views/adb_direct_debits/list.xml',
        'views/adb_lookups_accounts/list.xml',
        'views/adb_lookups_bvn/list.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "auto_install": False
}
