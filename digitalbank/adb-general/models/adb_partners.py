# -*- coding: utf-8 -*-

from os import remove
from odoo.exceptions import ValidationError
from odoo import models, fields, api
import uuid
import logging 

_logger = logging.getLogger(__name__)

class adb_partners(models.Model):
    _inherit = 'res.partner'
    # TODO-#1: All listed ranks are exclusive (e.g. you cannot be a client and a tenent etc.)
    # -- You can use SQL contraints or @api.onchange decorator (preference is for SQ constraint)

    agent_rank = fields.Integer(string="Agent Rank")           #use rank to determine agent level
    merchant_rank = fields.Integer(string="Merchant Rank")        #use rank to determine priority ranking (i.e. main, fallback, last resort)
    client_rank = fields.Integer(string="Client Rank")          #use rank to determine tier-level status
    external_id = fields.Char(string="Ref.")
    agent_location = fields.Many2one("adb.location", "Location")

    @api.model
    def create(self, vals):
        vals['external_id'] = uuid.uuid4()
        return super(models.Model, self).create(vals)

    @api.model
    def _user_create(self, vals):
        matchDeviceSqlCommand = """
            SELECT d.client, p.email, p.phone FROM adb_device d
            LEFT JOIN res_partner p on p.id = d.client
            WHERE sha256(d.reference::bytea)::varchar = concat('\\x','{device}')
            """.format(**vals)
        cr = self._cr
        cr.execute(matchDeviceSqlCommand)
        device = cr.fetchone()
        if device:
            if (device.email != vals['email'] | device.phone != vals['phone']):
                raise ValidationError('REG01: A registration has already occured using this device.')
        if(self.search_count(['|',('phone', '=', vals['phone']),('email', '=', vals['email'])]) > 0):
            raise ValidationError('REG02: A registration has already occured using this phone number or email.')

        
        del vals['device']

        return self.create(vals)

    @api.model
    def create_with_reference(self, vals):
        partner = self.search([('phone', '=', vals['phone']),('email', '=', vals['email'])])
        if not partner:
            partner = self._user_create(vals)
        return {
            "id": partner.id,
            "reference": partner.external_id
        }