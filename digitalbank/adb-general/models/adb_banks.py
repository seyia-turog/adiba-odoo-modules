# -*- coding: utf-8 -*-

from odoo import models, fields, api

class adb_banks(models.Model):
    _inherit = 'res.bank'
    # _name = 'res.bank'
    # _description = 'List of Banks'
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    # _sql_constraints = [('client_id','UNIQUE (client_id)', 'Client with this ID already exists')]

    location_id = fields.Many2one('adb.location')   #HQ Bank Location
    # name = fields.Char(string='Bank Name')
    code = fields.Char(string='National Code')
    bank_logo = fields.Text(string='Bank Logo')
    category = fields.Integer(string='Category')
    description = fields.Char(string='Description')
    swift_code = fields.Char(string='Swift Code')
    branch_count = fields.Integer(string='Branch Count')
    incorporation_date = fields.Char(string='Incorporation Date')
    rc_number = fields.Char(string='RC Number')
    website = fields.Text(string='Website')
    internal = fields.Char(default="false")
    