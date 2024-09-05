# -*- coding: utf-8 -*-
{
    'name': "TUROG Web Assets",

    'summary': "TUROG Odoo Website CSS & JS assets",

    'description': """
TUROG Odoo Website CSS & JS assets
    """,

    'author': "TUROG Integrated Solutions Limited",
    'website': "https://www.turog.com.ng",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
       'web._assets_primary_variables': [
           "turog_webassets/static/src/scss/primary_variable.scss",
       ],
       'web.assets_frontend':[
           "turog_webassets/static/src/fonts/Pavelt/Pavelt.ttf",
           "turog_webassets/static/src/fonts/THICCCBOI/THICCCBOI-Black.ttf",
           "turog_webassets/static/src/fonts/THICCCBOI/THICCCBOI-Bold.ttf",
           "turog_webassets/static/src/fonts/THICCCBOI/THICCCBOI-ExtraBold.ttf",
           "turog_webassets/static/src/fonts/THICCCBOI/THICCCBOI-Light.ttf",
           "turog_webassets/static/src/fonts/THICCCBOI/THICCCBOI-Medium.ttf",
           "turog_webassets/static/src/fonts/THICCCBOI/THICCCBOI-Regular.ttf",
           "turog_webassets/static/src/fonts/THICCCBOI/THICCCBOI-SemiBold.ttf",
           "turog_webassets/static/src/fonts/THICCCBOI/THICCCBOI-ThicccAF.ttf",
           "turog_webassets/static/src/fonts/THICCCBOI/THICCCBOI-Thin.ttf",
       ]
   },
}