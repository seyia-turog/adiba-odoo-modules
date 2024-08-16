# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
from odoo import models, fields, api
import random, logging
from passlib.hash import pbkdf2_sha256 as hashpass
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode

_logger = logging.getLogger(__name__)

class adb_devices(models.Model):
    _name = 'adb.device'
    _description = 'Device listing'

    name = fields.Char()            # for Cordova manufacturer should be name
    platform = fields.Selection([('ios','iOS'),('android','Android')])
    model = fields.Char()
    version = fields.Char()         
    reference = fields.Char()             # UUID or unique device code from mobile (persistent across re-installs)
    isVirtual = fields.Boolean(default=False)    # detect client side if it's an emulator doing the calls.   
    client = fields.Many2one('res.partner')
    locked = fields.Boolean(default=True)
    active = fields.Boolean(default=True)
    tcode = fields.Char()
    pin = fields.Char()     #TODO: Either change to password data type or use password encryption to store

    @api.model
    def create(self, vals):
        intPin = int(vals['pin'])
        if(intPin < 0 or intPin > 9999):
            raise ValidationError('FDN01: Invalid device pin') 
        vals['pin'] = hashpass.hash(vals['pin'].zfill(4))
        
        # Validation A: Same Device Cannot be used for multiple registrations
        active_devices = self.search_read([('reference','=',vals['reference']),('active','=',True)])
        if len(active_devices):
            raise ValidationError('FDN06: This device is already active.')
        
        # Validation B: Same Account Cannot be registered on multiple active devices
        active_clients = self.search_read([('client','=',vals['client']),('active','=',True)])
        if(active_clients):
            raise ValidationError('FDN07: This user already has an active device')
        
        return super(models.Model, self).create(vals)


    def transfer(self, vals):
        for device in self:
            rand_tcode = random.randint(100000,999999)
            hashed = hashpass.hash(str(rand_tcode))
            device_partner_id = device.client.id
            if device_partner_id == int(vals['client']):
                device.write({'tcode': hashed, 'locked': False})
                return rand_tcode
            else:
                raise ValidationError('FDN02: User does not match one or more devices')
    
    @api.model
    def confirm(self, vals):
        devices = self.search_read([('client','=',int(vals['client'])),('locked','=',False),('active','=',True)])
        if not len(devices):
            raise ValidationError('FDN03: Could not locate eligible device for transfer. Contact helpdesk team.')
        for device in devices:
            hashed_tcode = device['tcode']
            hashed_pin = device['pin']
            if not hashpass.verify(vals['tcode'], hashed_tcode):
                raise ValidationError('FDN04: Invalid device transfer code')
            if not hashpass.verify(vals['pin'], hashed_pin):
                raise ValidationError('FDN05: Invalid device PIN')
            active_devices = self.search_read([('reference','=',vals['reference']),('active','=',True)])
            if len(active_devices):
                raise ValidationError('FDN06: This device is already active.')
            self.browse([device.pop('id')]).write({'tcode': None, 'locked': True, 'active': False})
            vals.pop('tcode',None)
            self.create(vals)
        return True

    def check_pin(self, vals):
        intPin = int(vals['pin'])
        if(intPin < 0 or intPin > 9999):
            raise ValidationError('Invalid device pin') 
        return hashpass.verify(vals['pin'], self.pin)
   
    def set_pin(self, vals):
        intPin = int(vals['pin'])
        if(intPin < 0 or intPin > 9999):
            raise ValidationError('Invalid device pin') 
        hashed_pin = hashpass.hash(vals['pin'].zfill(4))

        for device in self:
            device.write({'pin': hashed_pin})
        return True
    
    def checksum(self, hashed, unhashed):
        encrypted = hashpass.hash(unhashed)
        if encrypted != hashed:
            return 0
        return 1
    
    def encrypt(self, plain):
        device_ref = self.reference
        key = device_ref.translate({ord('-'): None})
        cipher = AES.new(bytes(key, 'utf-8'), AES.MODE_ECB)
        ct_bytes = cipher.encrypt(pad(bytes(plain, 'utf-8'), AES.block_size))

        b64Encrypted = b64encode(ct_bytes).decode('utf-8')
        return b64Encrypted
    
    def open_dialog_box(self, message):

        #TODO: Let this action email the code rather than display

        action = {
            'name': 'Dialog Box',
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': message,
                'type': 'success',
                'sticky': False
            }
        }
        return action
    
    def action_setpin(self):
        intPin = str(random.randint(0,9999))
        self.set_pin({"pin":intPin})
        return self.open_dialog_box("Pin successfully set to {0}.".format(intPin))



    def action_reset(self):
        partner = self.client
        tcode = self.transfer({"client":partner})
        return self.open_dialog_box("Tcode successfully set to {0}.".format(tcode))