from odoo import api, fields, models
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

class adb_opportunity(models.Model):
    _inherit = 'crm.lead'

    date_deadline = fields.Datetime(default=datetime.now() + timedelta(days=7))
    partner_name = fields.Char(required=True)
    partner_email = fields.Char(string='Email',required=True)
    mobile = fields.Char(required=True)
    country_id = fields.Many2one('res.country',required=True)
    license_ids = fields.One2many('adb.license','opportunity_id')
    license_code =  fields.Char(compute="_get_license_code")


    def _get_license_code(self):
        for opportunity in self:
            active_licenses = [None]

            for license in opportunity.license_ids:
                expiry_date = license.expires_on.strftime('%Y-%m-%d')
                current_date = datetime.now().strftime('%Y-%m-%d')
                if expiry_date > current_date:
                    active_licenses.append(license.code)

            opportunity.license_code = active_licenses[-1]

        
    @api.model
    def create(self, vals):

        if vals.get('country'):
            country = self.env['res.country'].search([('code','=',vals['country'])])
            vals['country_id'] = country[0].id
            del(vals['country'])
        
        return super(models.Model, self).create(vals)