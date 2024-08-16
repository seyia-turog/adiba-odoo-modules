from odoo import api, fields, models


class adb_settlement_inward(models.Model):
    _name = 'adb.settlement.inward'
    _description = 'New Description'

    name = fields.Char(string='Name')
    resource_id = fields.Char('Resource ID')
    source_ref = fields.Char("Reference")
    account_num = fields.Many2one('adb.lookup.account')
    account_id = fields.Char('Account ID')
    amount = fields.Float("Amount")
    transaction_ref = fields.Char("Transaction Reference")
    response_code = fields.Text("Response Code")
    response_message = fields.Text("Response Message")
    posting_date = fields.Char("Posting Date")
    posting_rvsl_date = fields.Char("Posting Reversal Date")
    resource_rvsl_id = fields.Char("Resource Reversal ID")
    resource_rvsl_date = fields.Char("Resource Reversal Date")
    paycode_rvsl_is_set = fields.Boolean(string="Is Set For Paycode Reversal")
    paycode_trans_id = fields.Char(string='Paycode Transaction ID')
    paycode_wdrw_resrc_id = fields.Char(string='Paycode Withdrawal Resource ID')
    nip_tsq_count = fields.Integer(string='NIP Transaction Query Count', compute='tsq_count')
    nip_tsq_is_done = fields.Boolean("NIP Transaction Query is Done")
    nip_tsq_date = fields.Char("NIP Transaction Query Date Confirmed")
    beneficiary_account_num = fields.Char(string='Beneficiary Account Number')
    transaction_direction = fields.Char(string="Transaction Direction")
    channel = fields.Char(string="Channel")
    modified = fields.Datetime(string='Modified')

    # partner = fields.Char(string='??')
    
    # @api.model
    def tsq_count(numbers):
        for i in numbers:
            pass
        pass