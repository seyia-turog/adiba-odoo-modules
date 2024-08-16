# -*- coding: utf-8 -*-

from odoo import models, fields, api

class adb_lookups_account(models.Model):
    _name = 'adb.lookup.account'
    _description = 'Account lookups cache'

    bank_id = fields.Many2one('res.bank')
    account_no = fields.Char('Account Number')
    beneficiary_name = fields.Char('Beneficiary Name')
    lookup_ref = fields.Char('Lookup Ref.') #Customer-ref for paystack, Other codes for other vendors
    source = fields.Char('Source') #PAYSTACK, NIBSS, ETC.
    bank_code = fields.Char('BIC') 
    bank_name = fields.Char('Bank')

    # @api.depends('bank_id')
    # def _compute_code(self):
    #     for line in self:
    #         line.bank_code = line.bank_id.bic
    #         line.bank_name = line.bank_id.name

    # @api.multi
    # def _code_search(self, operator, value):
    #     recs = self.search([]).filtered(lambda x : x.bank_code == value )
    #     return [('id', operator, [x.id for x in recs] if recs else False )]

    # @api.model
    # def create(self, vals):
    #     vals['bank_id'] = self.env['adb.banks.paystack'].search([('bank_id','=',vals['code'])]).id()
    #     return super(models.Model, self).create(vals)


# class adb_lookups_paystack(models.Model):
#     _name = 'adb.lookups.paystack'
#     _description = 'Bank Lists for Paystack'

#     name = fields.Char('Name')
#     slug = fields.Char('Slug')
#     code = fields.Char('Code')
#     longcode = fields.Char('Longcode')
#     gateway = fields.Char('Gateway')
#     country = fields.Char('Country')
#     currency = fields.Char('Currency')
#     ac_type = fields.Char('Type')
#     bank_id = fields.Many2one('res.bank')
#     paystack_id = fields.Char('paystack_id')