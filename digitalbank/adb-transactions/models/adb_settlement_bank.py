from odoo import api, fields, models
from odoo.exceptions import ValidationError


class adb_settlement_bank(models.Model):
    _name = 'adb.settlement.bank'
    _description = 'Bank Settlements'

    bank = fields.Many2one('res.bank')
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

    beneficiary_account_num = fields.Char(string='Beneficiary Account Number')
    beneficiary_inst_code = fields.Char(string='Beneficiary Institution Code')
    # merchant = fields.Many2one(comodel_name='res.partner', string='Merchant')
    partner = fields.Many2one(comodel_name='res.partner', string='Partner')

    transaction_direction = fields.Char(string="Transaction Direction")
    channel = fields.Char(string="Channel")
    
    @api.model
    def create(self, vals):
        banks = self.env['res.bank'].search([('bic','=',vals['beneficiary_inst_code'])])
        partners = self.env['res.partner'].search([('external_id','=',vals['partner_ref'])])
        if len(banks) < 1:
            raise ValidationError('Bank Settlement: Beneficiary Bank is not a valid institution code.')
        if len(partners) < 1:
            raise ValidationError('Bank Settlement: Invalid partner reference supplied.')
        vals['bank'] = banks[0].id
        vals['partner'] = partners[0].id
        del vals['partner_ref']
        return super(models.Model, self).create(vals)