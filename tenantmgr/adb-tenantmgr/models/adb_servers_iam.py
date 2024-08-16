from odoo import api, fields, models


class adb_servers_iam(models.Model):
    _name = 'adb.servers.iam'
    _description = 'IAM config'


    # general properties
    tenant_id = fields.Many2one('res.partner')
    name = fields.Char(string='Name')
    sandbox = fields.Boolean()
    model = fields.Selection([('ODOO15', 'ODOO15'), ('WSO2IS52', 'WSO2IS52')], string='Type')

    # connection properties
    url = fields.Char(string='URL')
    username = fields.Char(string='Username')
    password = fields.Char(string='Password')
    database = fields.Char(string='Database')

    # defaults properties
    meta = fields.Char()
