# -*- coding: utf-8 -*-

from odoo import models, fields, api

class adb_card_issuances(models.Model):
    _name = 'adb.card.issuance'
    _description = 'List of cards issied to clients'

    name = fields.Char()
    client_id = fields.Many2one('res.partner')
    account_num = fields.Char(string='Account Number')
    card_num = fields.Char(string='Card Number')
    card_name = fields.Char(string='Card Name')
    card_type = fields.Char(string='Card Type')
    card_cvv = fields.Char(string='CVV')
    provider = fields.Selection(string='Provider', selection=[('MasterCard', 'MasterCard'), ('Visa', 'Visa'),('Verve', 'Verve')])
    expiry_date = fields.Char("Expiry Date")
    created = fields.Datetime(string='Created')
