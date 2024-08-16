from odoo import api, fields, models


class adb_settlement_bill(models.Model):
    _name = 'adb.settlement.bill'
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

    biller_item = fields.Integer(string='Biller Item') #relation with biller items except for artime like payments
    partner = fields.Many2one(comodel_name='res.partner', string='Partner')

    transaction_direction = fields.Char(string="Transaction Direction")
    channel = fields.Char(string="Channel")
    
    @api.model
    def create(self, vals):
        item_dict = {"airtel":2349001, "mtn": 2349002, "globacom":2349003, "9mobile": 2349004}
        partners = self.env['res.partner'].search([('external_id','=',vals['partner_ref'])])
        if len(partners) < 1:
            raise ValidationError('Bills Settlement: Invalid partner reference supplied.')
        vals['partner'] = partners[0].id
        if(vals['biller_item'] in  item_dict.keys()):
            vals['biller_item'] = item_dict.get(vals['biller_item'])
        else:
            vals['biller_item'] = int(vals['biller_item'])
        del vals['partner_ref']
        return super(models.Model, self).create(vals)