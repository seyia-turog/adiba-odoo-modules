# -*- coding: utf-8 -*-
# from odoo import http


# class Adb-general(http.Controller):
#     @http.route('/adb-general/adb-general', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/adb-general/adb-general/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('adb-general.listing', {
#             'root': '/adb-general/adb-general',
#             'objects': http.request.env['adb-general.adb-general'].search([]),
#         })

#     @http.route('/adb-general/adb-general/objects/<model("adb-general.adb-general"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('adb-general.object', {
#             'object': obj
#         })
