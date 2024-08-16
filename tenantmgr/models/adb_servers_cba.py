from xml.etree.ElementInclude import default_loader
from odoo import api, fields, models


class adb_servers_cba(models.Model):
    _name = 'adb.servers.cba'
    _description = 'Core Banking Application'

    # general properties
    tenant_id = fields.Many2one('res.partner')
    name = fields.Char(string='Name')
    sandbox = fields.Boolean()
    model = fields.Selection([('FINACLE', 'FINACLE'), ('FINERACT', 'FINERACT'), ('FINERACT-CN', 'FINERACT-CN')], string='Type')

    # connection properties
    url = fields.Char(string='URL')
    username = fields.Char(string='Username')
    password = fields.Char(string='Password')
    database = fields.Char(string='Database')

    # defaults properties
    meta = fields.Char()
