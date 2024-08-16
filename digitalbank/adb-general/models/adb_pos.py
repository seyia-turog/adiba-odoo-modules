
from odoo import models, fields, api

class adb_pos(models.Model):
    _name = 'adb.pos'
    _description = 'List of Bank POSs'

    location_id = fields.Many2one('adb.location')   #POS Location
    bank_id = fields.Many2one('res.bank')
    currency = fields.Many2one('res.currency')
    phone = fields.Char('Phone Number')
    date_deployed = fields.Char(string='Date Deployed')
    merchant_id = fields.Many2one('res.partner', string="Merchant ID")
    email = fields.Many2one("res.partner", string="Email")