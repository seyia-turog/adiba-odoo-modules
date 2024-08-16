# -*- coding: utf-8 -*-
#############################################################################
#
#
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

{
    'name': 'Deferred Revenue & Expenses',
    'category': 'Asset',
    'version' : '15.0',
    'summary': "Asset Deffered Revenue and Expense",
    'depends': [
        'account',],
    'author': 'APPSGATE FZC LLC',
    'description': """ 

           asset revenue,
           split,
          asset management,
          expense,
          revenue,
          asset expense,
          asset,
          prepayment,
          payment,
          pre-payment,
       """,
     'data': [
       # 'security/ir.model.access.csv',
        'data/account_asset_data.xml',
        'security/account_asset_security.xml',
        'security/ir.model.access.csv',
        'wizard/asset_depreciation_confirmation_wizard_views.xml',
        'wizard/asset_modify_views.xml',
        'views/account_asset_views.xml',
        'views/account_move_views.xml',
        'views/account_asset_templates.xml',
        'views/product_views.xml',
        'report/account_asset_report_views.xml',
        'views/account_deferred_revenue.xml',
        'views/account_deferred_expense.xml'
    ],
    'images': [
        'static/src/img/main-screenshot.png'
    ],

    'demo': [
    ],
    'license': 'AGPL-3',
    'application': True,
    'installable': True,
    'auto_install': False,
    'currency': 'USD',
    'price': 100.00,

 'assets': {
        'web.assets_backend': [
            'ag_prepayment/static/src/scss/account_asset.scss',
            'ag_prepayment/static/src/js/account_asset.js',
        ],
        'web.qunit_suite_tests': [
            ('after', 'web/static/tests/legacy/views/kanban_tests.js', '/ag_prepayment/static/tests/account_asset_tests.js'),
        ],
    },
}


