# -*- coding: utf-8 -*-
# from odoo import http


# class Adb-content(http.Controller):
#     @http.route('/adb-content/adb-content', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/adb-content/adb-content/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('adb-content.listing', {
#             'root': '/adb-content/adb-content',
#             'objects': http.request.env['adb-content.adb-content'].search([]),
#         })

#     @http.route('/adb-content/adb-content/objects/<model("adb-content.adb-content"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('adb-content.object', {
#             'object': obj
#         })
