from odoo import api, fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError



class adb_mandate_order(models.Model):
    _name = 'adb.mandate.order'
    _description = 'Mandate Orders'
    _sql_constraints = [
        ('transaction_ref_unique', 'unique(transaction_ref)', 'Transaction reference must be unique!')
    ]

    partner = fields.Many2one('res.partner')
    partner_ref = fields.Char('Partner Ref', related='partner.external_id',store=True)
    frequency = fields.Char(string='Frequency')                                 # DAILY, WEEKLY, FORTNIGHTLY, MONTHLY, QUARTERLY, YEARLY
    batch = fields.Char(string='Batch')
    date = fields.Datetime(string='Date', default=datetime.today())
    status = fields.Char(string='Status', default="active")                     # [ active, inactive, completed, suspended]
    
    source_type = fields.Char(string='Source Type')                             #[own_transfer, intra_transfer, inter_transfer, wallet_transfer,    bills_payment,  card_funding,   loans_repayment]
    source_ref = fields.Char(string='Source Ref')                               #[client_id,    client_id,      client_id,      client_id,          client_id,      card_id,        loan_id]
    source_account = fields.Char(string='Source Account')                       #[account_id,   account_id,     account_id,     account_id,         account_id,     accountNo,      account_no]
    destination_ref = fields.Char(string='Destination Account')                 #[account_id,   client_id,      lookupId,        walletCode,        client_id,      client_id,      account_id]
    destination_account = fields.Char(string='Destination Institution Code')    #[account_no,   account_no,     accountNo,       phoneNumber,       bills_payment,  account_id,     account_no]

    transaction_ref = fields.Char(string='Transaction Ref')
    transaction = fields.Char(string='Transaction')
    biller_id = fields.Char(string='Biller ID')
    biller_item_id = fields.Char(string='Biller Item ID')
    
    amount = fields.Float(string='Amount')
    expiry = fields.Date(string="Expires On")

    register = fields.One2many('adb.mandate.register',"order_id")

    @api.model 
    def create(self, vals):
        partners = self.env['res.partner'].search([('external_id','=',vals['partner_ref'])])

        if not partners:
            raise ValidationError('MNORD01: Partner must exist for mandate')

        interval = {
            'DAILY': datetime.today()+relativedelta(days=+1),
            'WEEKLY': datetime.today() + relativedelta(weeks=+1),
            'FORTNIGHTLY':  datetime.today() + relativedelta(weeks=+2),
            'MONTHLY': datetime.today() + relativedelta(months=+1),
            'QUARTERLY': datetime.today() + relativedelta(months=+3),
            'YEARLY': datetime.today() + relativedelta(months=+12)
        }

        vals['partner'] = partners[0].id
        vals['status'] = "active"
        vals['expiry'] = datetime.strptime(vals['expiry'],"%Y-%m-%d")
        vals['batch'] = interval.get(vals['frequency']).strftime("%Y%m%d")
        vals['register'] = [(0, 0, {
            'next_run': interval.get(vals['frequency'])
        })]

        return super(models.Model, self).create(vals)
    