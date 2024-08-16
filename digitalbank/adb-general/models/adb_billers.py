# -*- coding: utf-8 -*-

from cProfile import label
from itertools import product
from odoo import models, fields, api

class adb_biller_categories(models.Model):
    _name = 'adb.biller.category'
    _description = 'List of Biller Categories'

    name = fields.Char()
    icon = fields.Char()


class adb_billers(models.Model):
    _name = 'adb.biller'
    _description = 'List of Billers'

    category_id = fields.Many2one('adb.biller.category')

    name = fields.Char()
    logo = fields.Char()


class adb_biller_items(models.Model):
    _name = 'adb.biller.item'
    _description = 'List of Biller Items'

    biller_id = fields.Many2one('adb.biller')

    sku = fields.Char()
    country = fields.Char()
    operator = fields.Char()
    min_denomination = fields.Char()
    max_denomination = fields.Char()
    currency = fields.Char()
    steps = fields.Char()
    fx_rate = fields.Char()
    price = fields.Char()
    label = fields.Char()
    description = fields.Char()    
    screens = fields.Char()



class adb_biller_items_primeairtime(models.Model):
    _name = 'adb.biller.item.primeairtime'
    _descripion = 'Primeairtime billing lits'

    item_id  = fields.Many2one('adb.biller.item')
    service = fields.Char()
    product = fields.Char()
    code = fields.Char()
    price = fields.Char()
    topup_value = fields.Char()
    currency = fields.Char()
    topup_currency = fields.Char()
    isAddon = fields.Char()
    rate = fields.Char()
    min_denomination = fields.Char()
    max_denomination = fields.Char()
    step = fields.Integer()
    url_template = fields.Char()
    

class adb_biller_items_hubtel(models.Model):
    _name = 'adb.biller.item.hubtel'
    _descripion = 'Hubtel billing lits'

    item_id  = fields.Many2one('adb.biller.item')
    service = fields.Char()
    product = fields.Char()
    code = fields.Char()
    price = fields.Char()
    topup_value = fields.Char()
    currency = fields.Char()
    topup_currency = fields.Char()
    isAddon = fields.Char()
    rate = fields.Char()
    min_denomination = fields.Char()
    max_denomination = fields.Char()
    step = fields.Integer()
    url_template = fields.Char()