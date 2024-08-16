from odoo import api, fields, models


class adb_refresh_tokens(models.Model):
    _name = 'adb.tokens.refresh'
    _description = 'Refresh Tokens'

    token = fields.Char()
    user_id = fields.Many2one('res.users')
    username = fields.Char()
    expires_in = fields.Char()
    sandbox = fields.Boolean()

