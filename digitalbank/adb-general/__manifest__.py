# -*- coding: utf-8 -*-
{
    'name': "adb-general",

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
        'views/adb_partners/agents/form.xml',
        'views/adb_partners/agents/list.xml',
        'views/adb_partners/clients/form.xml',
        'views/adb_partners/clients/list.xml',
        'views/adb_partners/merchants/form.xml',
        'views/adb_partners/merchants/list.xml',
        'views/adb_locations/list.xml',
    #    'views/adb_banks/list.xml',
        'views/adb_branches/list.xml',
        'views/adb_atms/list.xml',
        'views/adb_pos/list.xml',
        'views/adb_merchants/list.xml',
        'views/templates.xml',
        'data/cron.xml'
    ],
    "auto_install": False
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
