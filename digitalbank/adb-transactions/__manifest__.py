# -*- coding: utf-8 -*-
{
    'name': "adb-transactions",

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
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/adb_mandate_order/list.xml',
        'views/adb_mandate_register/list.xml',
        'views/adb_settlement_bank/list.xml',
        'views/adb_settlement_bill/list.xml',
        'views/adb_settlement_cardless/list.xml',
        'views/adb_settlement_card/list.xml',
        'views/adb_settlement_inward/list.xml',
        'views/adb_settlement_loan/list.xml',
        'views/adb_settlement_collections/list.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "auto_install": False
}
