# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api

class adb_beneficiaries(models.Model):
    _name = 'adb.beneficiary'
    _description = 'List of client beneficaries'

    name = fields.Char(string='Beneficiary Name', required=True)
    currency = fields.Char(string='Currency', required=True)
    dest_account = fields.Char(string='Destination Account', required=True)
    dest_client = fields.Char(string='Destination Client Id')
    dest_account_id = fields.Integer(string="Internal Account ID")
    account_type = fields.Selection([("internal","INTERNAL"),("external","EXTERNAL")])

    bank_id = fields.Many2one(comodel_name='res.bank', required=True)
    client_id = fields.Many2one(comodel_name='res.partner', required=True)
    lookup_id = fields.Many2one('adb.lookup.account')

    bank_name = fields.Char(compute="_get_bank_details")
    bank_code = fields.Char(compute="_get_bank_details")

    def _get_bank_details(self):
        for beneficary in self:
            bank_model = self.env['res.bank'].browse([beneficary.bank_id.id])
            beneficary.bank_name = bank_model.name
            beneficary.bank_code = bank_model.bic

    # override create to check if condition exists and throw validation error if one matches before posting 
    # conditions: 
    # 1. duplication on multiple columns  
    # 2. can't determine if request is internal or external 
    # 3. if internal, dest_account_id is missing 
    # 4. if external, lookup_id is missing 

    @api.model
    def create(self, vals):
        if not vals['account_type']:
            raise ValidationError('BNF02: Account Type must be INTERNAL or EXTERNAL')
        if(vals['account_type'] == "internal" and (not vals['dest_account_id'])):
            raise ValidationError('BNF03: Account ID cannot be empty for INTERNAL type')
        if(vals['account_type'] == "external" and (not vals['lookup_id'])):
            raise ValidationError('BNF04: Lookup ID cannot be empty for EXERNAL type')
        record = self.search([('dest_account','=',vals['dest_account']),('account_type','=',vals['account_type']),('client_id','=',int(vals['client_id']))])
        if record:
            raise ValidationError('BNF01: Beneficiary already stored for destination account')
        return super(models.Model, self).create(vals)
