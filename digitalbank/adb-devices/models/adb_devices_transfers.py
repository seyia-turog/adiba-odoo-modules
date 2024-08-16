# -*- coding: utf-8 -*-

from odoo import models, fields, api

class adb_devices_transfers(models.Model):
    _name = 'adb.device.transfer'
    _description = 'Devices transfers'

    old_device_id = fields.Char()
    new_device_id = fields.Char()