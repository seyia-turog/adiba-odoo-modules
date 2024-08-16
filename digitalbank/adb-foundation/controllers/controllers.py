# -*- coding: utf-8 -*-
# from odoo import http


# class Adb-foundation(http.Controller):
#     @http.route('/adb-foundation/adb-foundation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/adb-foundation/adb-foundation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('adb-foundation.listing', {
#             'root': '/adb-foundation/adb-foundation',
#             'objects': http.request.env['adb-foundation.adb-foundation'].search([]),
#         })

#     @http.route('/adb-foundation/adb-foundation/objects/<model("adb-foundation.adb-foundation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('adb-foundation.object', {
#             'object': obj
#         })
