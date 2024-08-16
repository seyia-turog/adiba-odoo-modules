# -*- coding: utf-8 -*-

from odoo import models, fields, api

class adb_branches(models.Model):
    _name = 'adb.branch'
    _description = 'List of Bank branches'

    location_id = fields.Many2one('adb.location')   #Branch Location
    bank_id = fields.Many2one('res.bank') 
