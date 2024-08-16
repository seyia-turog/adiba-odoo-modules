# -*- coding: utf-8 -*-
# from odoo import http


# class Adb-devices(http.Controller):
#     @http.route('/adb-devices/adb-devices', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/adb-devices/adb-devices/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('adb-devices.listing', {
#             'root': '/adb-devices/adb-devices',
#             'objects': http.request.env['adb-devices.adb-devices'].search([]),
#         })

#     @http.route('/adb-devices/adb-devices/objects/<model("adb-devices.adb-devices"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('adb-devices.object', {
#             'object': obj
#         })
