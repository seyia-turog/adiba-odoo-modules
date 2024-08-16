from odoo import api, fields, models
from datetime import datetime, timedelta


class adb_license(models.Model):
    _name = 'adb.license'

    code = fields.Char()
    expires_on = fields.Datetime(default=datetime.now() + timedelta(days=30))
    opportunity_id = fields.Many2one('crm.lead')
    