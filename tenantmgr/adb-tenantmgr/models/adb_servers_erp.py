from odoo import api, fields, models


class adb_servers_erp(models.Model):
    _name = 'adb.servers.erp'
    _description = 'ERP config'

    # general properties
    tenant_id = fields.Many2one('res.partner')
    name = fields.Char(string='Name')
    sandbox = fields.Boolean()
    model = fields.Selection([('ODOO15', 'ODOO15'),('SAPECC', 'SAPECC'),('SAPONE', 'SAPONE'), ('MSD365', 'MSD365'), ('ORACLE', 'ORACLE')], string='Type')

    # connection properties
    url = fields.Char(string='URL')
    username = fields.Char(string='Username')
    password = fields.Char(string='Password')
    database = fields.Char(string='Database')

    # defaults properties  
    meta = fields.Char()
