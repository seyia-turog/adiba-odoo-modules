# -*- coding: utf-8 -*-

from odoo import models, fields, api

class adb_locations(models.Model):
    _name = 'adb.location'
    _description = 'Base locations for ADB'

    longitude = fields.Float()
    latitude = fields.Float()
    street = fields.Char(string='Street')
    city = fields.Char(string='City')
    state = fields.Many2one('res.country.state',string='State')
    country = fields.Many2one('res.country', string='Country')