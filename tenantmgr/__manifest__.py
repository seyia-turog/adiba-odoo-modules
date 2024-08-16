{
    'name': "ADIBA Tenant Manager",

    'summary': """
        Tenant manager for ADIBA
        """,

    'description': """
        Tenant manager for ADIBA Bank in a Box Platform
    """,

    'author': "TUROG Technologies",
    'website': "http://www.turog.com.ng",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Administration',
    'version': '0.1',

    'depends': ['base','crm'],

    'pre_init_hook': '_pre_init_conflict_check',

    'data': [
        'views/views.xml',
        'security/ir.model.access.csv',
        'views/adb_servers_bpm/list.xml',
        'views/adb_servers_cba/list.xml',
        'views/adb_servers_erp/list.xml',
        'views/adb_servers_iam/list.xml',
        'views/adb_servers_fnd/list.xml',
        'views/adb_servers_hdsk/list.xml',
        'views/adb_opportunity/form.xml',
        'views/adb_tenant/form.xml',
        'views/adb_tenant/list.xml',
        'views/adb_tenant_admin/list.xml',
        'views/adb_tenant_contacts/list.xml',
        'views/menu.xml',
    ],
    "installable" : True,
    'application': True,
}
