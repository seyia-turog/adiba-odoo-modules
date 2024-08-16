# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api

class adb_lookups_identity(models.Model):
    _name = 'adb.lookup.identity'
    _description = 'Identity lookups cache'
    _sql_constraints = [
        ('unique_number', 'unique(number)', 'Identity values must be unique in caches')
    ]

    number = fields.Char(string="Number")
    first_name = fields.Char()
    middle_name = fields.Char()
    last_name = fields.Char()
    nationality = fields.Char()
    gender = fields.Char()
    place_of_birth = fields.Char()
    place_of_issue = fields.Char()
    date_of_birth = fields.Char()
    date_of_issue = fields.Char()
    date_of_expiry = fields.Char()

    identifier = fields.Char()
    source = fields.Char()