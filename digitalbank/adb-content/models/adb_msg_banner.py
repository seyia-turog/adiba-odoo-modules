# -*- coding: utf-8 -*-

from odoo import models, fields, api

class adb_msg_banner(models.Model):
    _name = 'adb.msg.banner'
    _description = 'Dynamic banners and in-app ads'

    name = fields.Char()  
    type = fields.Selection([('image','Image'),('html','Rich Text'),('text','Plain Text')])
    group = fields.Char() #TODO: Implement slides using this banner
    content = fields.Text()
    target_url = fields.Char()
