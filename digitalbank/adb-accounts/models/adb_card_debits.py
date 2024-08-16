# -*- coding: utf-8 -*-

from odoo import models, fields, api

class adb_card_debits(models.Model):
    _name = 'adb.card.debit'
    _description = 'List of cards maintained for tranasction debits'

    client_id = fields.Many2one('res.partner')
    authorization_code = fields.Char()
    bin = fields.Char()
    last4 = fields.Char()
    exp_month = fields.Char()
    exp_year = fields.Char()
    card_type = fields.Char()
    bank = fields.Char()
    country_code = fields.Char()
    brand = fields.Char()
    account_name = fields.Char()
    charge_amount = fields.Char()
    ip_address = fields.Char()
    partner_ref = fields.Char() #on create use this field to auto determine partner relationship (client_id)