# -*- coding: utf-8 -*-

from odoo import models, fields, api

class adb_msg_logs(models.Model):
    _name = 'adb.msg.log'
    _description = 'Audit logs for external messages'

    ref = fields.Char()
    meta = fields.Char()
    destination = fields.Char()
    service = fields.Char() #TODO-1: Create a relationship with a adb.msg.service model
    type = fields.Selection([('email','E-Mail'),('push','Push Notification'),('sms','Short Message Service')])
