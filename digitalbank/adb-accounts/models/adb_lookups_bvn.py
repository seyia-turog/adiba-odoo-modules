# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api
import hmac, base64, struct, hashlib, time, logging
# import base64, pyotp, logging

_logger = logging.getLogger(__name__)


class adb_lookups_bvn(models.Model):
    _name = 'adb.lookup.bvn'
    _description = 'BVN lookups cache'
    _sql_constraints = [
        ('unique_bvn', 'unique(bvn)', 'BVN values must be unique in caches')
    ]

    bvn = fields.Char(string="BVN")
    first_name = fields.Char()
    middle_name = fields.Char()
    last_name = fields.Char()
    date_of_birth = fields.Char()
    phone_number=fields.Char()
    registration_date=fields.Char()
    enrollment_bank=fields.Char()
    address=fields.Char()
    gender=fields.Char()
    email=fields.Char()
    nationality=fields.Char()
    marital_status=fields.Char()
    state_of_residence=fields.Char()
    lga_of_residence=fields.Char()
    nin = fields.Char()

    source = fields.Char() # IDENTITYPASS, NIBSS, FLUTTERWAVE


    @api.model
    def generate_totp(self, vals):
        if not vals['reference']:
            raise ValidationError('CODE01: Validation Error exists: Invalid reference')
        totp = self.get_totp_token(vals['reference'])
        return totp

    @api.model
    def validate_totp(self, vals):
        if not vals['reference']:
            raise ValidationError('CODE01: Validation Error exists: Invalid reference')
        totp = self.get_totp_token(vals['reference'])
        return (totp['code'] == vals['token'])

    
    def get_hotp_token(self, secret, intervals_no):
        key = base64.b32decode(secret, True)
        #decoding our key
        msg = struct.pack(">Q", intervals_no)
        #conversions between Python values and C structs represente
        h = hmac.new(key, msg, hashlib.sha1).digest()
        o = o = h[19] & 15
        #Generate a hash using both of these. Hashing algorithm is HMAC
        h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
        #unpacking
        return h

    def get_totp_token(self, secret):
        #ensuring to give the same otp for 600 seconds
        timing = int(time.time())//525
        expires = time.localtime((525 * timing) + 525)
        x =str(self.get_hotp_token(secret,intervals_no=timing))
        #adding 0 in the beginning till OTP has 6 digits
        while len(x)!=6:
            x+='0'
        return {'code':x,'expires': time.strftime("%d %b %Y, %H:%M:%S",expires)}
        