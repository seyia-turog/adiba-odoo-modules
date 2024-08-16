from odoo import api, fields, models


class adb_servers_bpm(models.Model):
    _name = 'adb.servers.bpm'
    _description = 'BPM config'

    # general properties
    tenant_id = fields.Many2one('res.partner')
    name = fields.Char(string='Name')
    sandbox = fields.Boolean()
    model = fields.Selection([('CAMUNDA', 'CAMUNDA')], string='Type')

    # connection properties
    url = fields.Char(string='URL')
    username = fields.Char(string='Username')
    password = fields.Char(string='Password')
    database = fields.Char(string='Database')

    # defaults properties
    meta = fields.Char()
    