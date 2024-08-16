# -*- coding: utf-8 -*-

from odoo import models, fields, api

class adb_devices_keypairs(models.Model):
    _name = 'adb.device.keypair'
    _description = 'Devices encryption keys for GPG based E2E device encryption'

    gpg_key = fields.Char(string='GPG Encryption Key')
    