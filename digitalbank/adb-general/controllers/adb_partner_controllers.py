from odoo import http
from odoo.http import request

import json

class PartnerController(http.Controller):

    @http.route('/api/partners', auth='api_key', type='http', methods=['GET'], csrf=False)
    def list_partners(self, **kwargs):
        partners = http.request.env['res.partner'].sudo().search([('client_rank','=',10)])
        db_name = request.httprequest.headers.get('x-odoo-database')
        request.session.db = db_name
        partner_list = []
        for partner in partners:
            partner_dict = {
                'reference': partner.external_id,
                'name': partner.name,
                'email': partner.email,
                'phone': partner.phone
            }
            partner_list.append(partner_dict)
        response =  http.request.make_response(json.dumps(partner_list))
        response.headers['Content-Type'] = 'application/json'
        return response
    