from odoo import api, fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


class adb_mandate_register(models.Model):
    _name = 'adb.mandate.register'
    _description = 'Mandate Register'

    next_run = fields.Datetime()
    last_run = fields.Datetime()
    status = fields.Char(default="upcoming")  #[upcoming, failed, succeeded, unknown, expired, deleted]
    transaction_ref = fields.Char()
    order_id = fields.Many2one('adb.mandate.order')

    @api.model
    def add(self, vals):
        
        
        order = self.order_id.search([('id','=',int(vals['order_id'])),('status','=','active')])
        register = self.search([('order_id','=',int(vals['order_id']))], limit=1, order="id desc")
        if not order:
            raise ValidationError('REG01: An inactive mandate order was supplied')
        freq = order[0]['frequency']
        lastrun = register[0]['next_run']
        interval = {
            'DAILY': lastrun +relativedelta(days=+1),
            'WEEKLY': lastrun + relativedelta(weeks=+1),
            'FORTNIGHTLY':  lastrun + relativedelta(weeks=+2),
            'MONTHLY': lastrun + relativedelta(months=+1),
            'QUARTERLY': lastrun + relativedelta(months=+3),
            'YEARLY': lastrun + relativedelta(months=+12)
        }

        vals['next_run'] = interval[freq]

        return self.create(vals)



