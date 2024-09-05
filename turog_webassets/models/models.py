# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class turog_webassets(models.Model):
#     _name = 'turog_webassets.turog_webassets'
#     _description = 'turog_webassets.turog_webassets'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

