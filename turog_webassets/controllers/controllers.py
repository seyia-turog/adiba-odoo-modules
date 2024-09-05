# -*- coding: utf-8 -*-
# from odoo import http


# class TurogWebassets(http.Controller):
#     @http.route('/turog_webassets/turog_webassets', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/turog_webassets/turog_webassets/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('turog_webassets.listing', {
#             'root': '/turog_webassets/turog_webassets',
#             'objects': http.request.env['turog_webassets.turog_webassets'].search([]),
#         })

#     @http.route('/turog_webassets/turog_webassets/objects/<model("turog_webassets.turog_webassets"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('turog_webassets.object', {
#             'object': obj
#         })

