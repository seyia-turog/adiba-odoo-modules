from odoo import api, fields, models


class adb_servers_hdsk(models.Model):
    _name = 'adb.servers.hdsk'
    _description = 'Helpdesk config'

    # general properties
    tenant_id = fields.Many2one('res.partner')
    name = fields.Char(string='Name')
    sandbox = fields.Boolean()
    model = fields.Selection([('ODOO15', 'ODOO15'), ('JIRA', 'JIRA'), ('FRESHDESK', 'FRESHDESK')], string='Type')

    # connection properties
    url = fields.Char(string='URL')
    username = fields.Char(string='Username')
    password = fields.Char(string='Password')
    database = fields.Char(string='Database')

    # defaults properties
    meta = fields.Char()
