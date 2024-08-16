# -*- coding: utf-8 -*-

from dataclasses import dataclass
from odoo import models, fields, api

class adb_msg_templates(models.Model):
    _name = 'adb.msg.template'
    _description = 'Template messages for dynamic alerts in-app'

    template = fields.Char()
    template_data = fields.Char()
    
    #usage {template: "str", data: {key: val}}