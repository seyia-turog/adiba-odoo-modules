from odoo import api, fields, models


class adb_servers_fnd(models.Model):
    _name = 'adb.servers.fnd'
    _description = 'Foundation Config'

    # general properties
    tenant_id = fields.Many2one('res.partner')
    name = fields.Char(string='Name')
    sandbox = fields.Boolean()
    model = fields.Selection([('ODOO15', 'ODOO15'), ('DATABASE', 'DATABASE')], string='Type')

    # connection properties
    url = fields.Char(string='URL')
    username = fields.Char(string='Username')
    password = fields.Char(string='Password')
    database = fields.Char(string='Database')

    # defaults properties
    meta = fields.Char()

