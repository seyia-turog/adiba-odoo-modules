# -*- coding: utf-8 -*-


from odoo import models, fields, api

class adb_atms(models.Model):
    _name = 'adb.atm'
    _description = 'List of Bank ATMs'

    location_id = fields.Many2one('adb.location')   #ATM Location
    bank_id = fields.Many2one('res.bank')
    # atm_services = fields.Many2one('adb.atm.services', string='ATM Services')
    merchant = fields.Char(string='Merchant')
    mini_statement = fields.Char(string='Mini Statement')
    atm_id = fields.Char(string='ATM ID')
    terminal_id = fields.Char(string='Terminal ID')
    base_currency = fields.Many2one('res.currency', string="Currency")
    minimum_cash_amount = fields.Text(string='Minimum Cash Amount')
    # balance = fields.Float(string='Balance')
    pin_change = fields.Boolean(string="Pin Change") # If the ATM allows for pin change
    active = fields.Boolean(string='Active') # Atm active or not active


    
    