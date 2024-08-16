from odoo import api, fields, models


class adb_settlement_wallet(models.Model):
    _name = 'adb.settlement.wallet'
    _description = 'New Description'

    posting_date = fields.Char("Posting Date")
    posting_amount = fields.Char("Amount")
    posting_id = fields.Char("Posting ID")
    account_id = fields.Char("Account ID")
    posting_ref = fields.Char("Payment Reference")
    posting_rvsl_date = fields.Char("Posting Reversal Date")
    resource_rvsl_id = fields.Char("Resource Reversal ID")
    resource_rvsl_date = fields.Char("Resource Reversal Date")

    tsq_count = fields.Integer(string='Transaction Query Count', default=0)
    tsq_is_done = fields.Boolean(string="Transaction Query is Done", default=False)
    tsq_date = fields.Char("Transaction Query Date Confirmed")
    tsq_ref = fields.Char("Transaction Reference")
    
    wallet_service = fields.Char(string='Wallet Service (Channel)')
    wallet_code = fields.Char(string='Account (Phone No.)')
    partner = fields.Many2one(comodel_name='res.partner', string='Partner')

    transaction_direction = fields.Char(string="Transaction Direction")
    channel = fields.Char(string="Channel")

    @api.model
    def create(self, vals):
        partners = self.env['res.partner'].search([('external_id','=',vals['partner_ref'])])
        vals['partner'] = partners[0].id
        del vals['partner_ref']
        return super(models.Model, self).create(vals)