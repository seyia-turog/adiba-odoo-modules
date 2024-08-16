# -*- coding: utf-8 -*-

from odoo import models, fields, api

class adb_card_debits(models.Model):
    _name = 'adb.direct.debit'
    _description = 'List of cards maintained for tranasction debits'

    client_id = fields.Many2one('res.partner')
    lookup_id = fields.Many2one('adb.lookup.account')
    account_num = fields.Char(string='Account Number')
    institution_code = fields.Char(string='Institution Code')
    limit = fields.Char(string='Limit')
    currency = fields.Char(string='Currency')
    created = fields.Datetime(string='Created')
