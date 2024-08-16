# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging, time

_logger = logging.getLogger(__name__)


class adb_msg_inapp(models.Model):
    _name = 'adb.msg.inapp'
    _description = 'In-App Messages'

    name = fields.Char()
    client_id = fields.Many2one('res.partner')
    recipient = fields.Char()
    broadcast_rank = fields.Integer()
    type = fields.Selection([('html','Rich Text'),('text','Plain Text')])
    title = fields.Char()
    body = fields.Char()
    image = fields.Char()
    actions = fields.Char()
    partner_ref = fields.Char() 


    @api.model
    def create(self, vals):
        email = vals.get('recipient')
        partner = self.env['res.partner'].search([('email', '=', email)], limit=1)
        if partner:
            vals['client_id'] = partner.id
            vals['partner_ref'] = partner.external_id

        return super(adb_msg_inapp, self).create(vals)
    

    @api.model
    def cron_recipients_process(self, vals):
        updateRecipientsCommand = """
                UPDATE adb_msg_inapp AS a
                SET a.client_id = p.id
                SET a.partner_ref = p.external_id
                FROM partner AS p
                WHERE a.partner_ref isnull and
                a.recipient = p.email;
            """.format(**vals) 
        
        start_time = time.time()
        self._cr.execute(updateRecipientsCommand)
        end_time = time.time()

        execution_time = end_time - start_time
        _logger.info("Updating recipients data. Execution time:", execution_time, "seconds")

        return None
