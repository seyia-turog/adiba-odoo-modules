# -*- coding: utf-8 -*-
# from odoo import http


# class Adb-transactions(http.Controller):
#     @http.route('/adb-transactions/adb-transactions', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/adb-transactions/adb-transactions/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('adb-transactions.listing', {
#             'root': '/adb-transactions/adb-transactions',
#             'objects': http.request.env['adb-transactions.adb-transactions'].search([]),
#         })

#     @http.route('/adb-transactions/adb-transactions/objects/<model("adb-transactions.adb-transactions"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('adb-transactions.object', {
#             'object': obj
#         })
