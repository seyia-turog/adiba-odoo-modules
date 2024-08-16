# -*- coding: utf-8 -*-
# from odoo import http


# class Adb-accounts(http.Controller):
#     @http.route('/adb-accounts/adb-accounts', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/adb-accounts/adb-accounts/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('adb-accounts.listing', {
#             'root': '/adb-accounts/adb-accounts',
#             'objects': http.request.env['adb-accounts.adb-accounts'].search([]),
#         })

#     @http.route('/adb-accounts/adb-accounts/objects/<model("adb-accounts.adb-accounts"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('adb-accounts.object', {
#             'object': obj
#         })
