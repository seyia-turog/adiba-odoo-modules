from odoo import api, fields, models


class adb_settlement_loan(models.Model):
    _name = 'adb.settlement.loan'
    _description = 'New Description'

    name = fields.Char(string='Name')
    resource_id = fields.Char('Resource ID')
    source_ref = fields.Char("Reference")
    account_num = fields.Many2one('adb.lookup.account')
    account_id = fields.Char('Account ID')
    amount = fields.Float("Amount")
    transaction_ref = fields.Char("Transaction Reference")
    posting_date = fields.Char("Posting Date")
    posting_rvsl_date = fields.Char("Posting Reversal Date")
    paycode_trans_id = fields.Char(string='Paycode Transaction ID')
    nip_tsq_count = fields.Integer(string='NIP Transaction Query Count', compute='tsq_count')
    nip_tsq_is_done = fields.Boolean("NIP Transaction Query is Done")
    nip_tsq_date = fields.Char("NIP Transaction Query Date Confirmed")
    beneficiary_inst_code = fields.Char(string='Beneficiary Institution Code')
    transaction_direction = fields.Char(string="Transaction Direction")
    channel = fields.Char(string="Channel")
    modified = fields.Datetime(string='Modified')
    
    # @api.model
    def tsq_count(numbers):
        for i in numbers:
            pass
        pass