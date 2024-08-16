# -*- coding: utf-8 -*-

from os import remove
from odoo.exceptions import ValidationError
from odoo import models, fields, api
import jwt, datetime, uuid, logging, json
from base64 import b64encode


_logger = logging.getLogger(__name__)

EXPIRES_IN = 300

class adb_refresh_tokens(models.Model):
    _name = 'adb.tokens.refresh'
    _description = 'Refresh Tokens'

    token = fields.Char()
    user_id = fields.Many2one('res.users')
    username = fields.Char()
    expires_in = fields.Char()
    sandbox = fields.Boolean()

class adb_partner(models.Model):
    _inherit = 'res.partner'
    external_id = fields.Char(string="Ref.")
    
    @api.model
    def create(self, vals):
        parent = None

        vals['external_id'] = uuid.uuid4()

        if vals.get('tenant_rank'):
            vals['tenant_ref'] = uuid.uuid4()

        if vals.get('country'):
            country = self.env['res.country'].search([('code','=',vals['country'])])
            vals['country_id'] = country[0].id
            del(vals['country'])

        if vals.get('parent'):
            parent = self.search([('external_id','=',vals['parent'])])
            vals['parent_id'] = parent[0].id
            
            del(vals['parent'])

        partner = super(models.Model, self).create(vals)

        if parent:
            self.env['mail.followers'].create({
                'res_id': parent[0].id,
                'res_model' : 'res.partner',
                'partner_id' : partner.id
            })
            str = '[:new_member] {} added to [:company] {}'.format(vals['name'], parent[0].name)
            parent.message_post(subject="New member added", body=str, message_type="comment")

        return partner

    @api.model
    def create_with_reference(self, vals):
        partner = self.search([('phone', '=', vals['phone']),('email', '=', vals['email'])])
        if not partner:
            partner = self.create(vals)
        return {
            "id": partner.id,
            "reference": partner.external_id
        }

class adb_member(models.Model):
    _inherit = 'res.users'
    email_verified = fields.Boolean(default=False)
    identity_verified = fields.Boolean(default=False)
    password_reset = fields.Boolean(default=False)

    def prepare_subscriptions(self, user):
        return [{
            "name": "BackOfficeEdgeService",
            "version": "1.0.0",
        }]
    
    def prepare_claims(self, user, nonce):
        claims = {}
        partner = user.partner_id

        claims.update({"partner": partner.external_id})
        claims.update({"email_verified": user.email_verified})
        claims.update({"identity_verified": user.identity_verified})
        claims.update({"password_reset": user.password_reset})
        claims.update({"device_verified": True})
        claims.update({"valid_license": False})

        return claims

    def prepare_payload(self, uid, sandbox, cTimestamp, nonce):
        user = self.browse(uid)
        payload = {
            'aud': "https://gw1.api.adiba.app", # important: audience of the app
            'exp': cTimestamp + EXPIRES_IN,     # configured for five minutes
            'iss': 'adiba-enterprise-odoo15',   # important: configured on the gateway
            "keytype": "PRODUCTION",            # a function of the env: Prod or Sandbox. hardcoded for now to production until we can create a sandbox environment
            'iat': cTimestamp,        
            'sub': user.login,                  # must NOT be an object, only string
            'azp': "DefaultApplication",        # consumer key
            'jti': str(uuid.uuid4()),           # important: for JWT token,
            'subscribedAPIs': self.prepare_subscriptions(user),
            'claims': self.prepare_claims(user, nonce)
        }
        #TODO: Add claims to payload
        #   reference: <partner_externalt_id>
        return payload

    def prepare_scope(self, uid):
        return "default"
    
    def prepare_private_key(self):
        priv_key = open('/opt/security/mg.key', 'rb').read()
        return priv_key

    def prepare_access_token(self, payload, private_key, tenant_ref):
        x5t= b64encode(tenant_ref.encode("UTF-8")).decode("UTF-8")
        token = jwt.encode(payload, private_key, algorithm='RS256',headers={"x5t": x5t})
        return token

    def prepare_refresh_token(self, vals, cTimestamp):
        vals['token'] = str(uuid.uuid4())
        vals['expires_in'] = cTimestamp + (EXPIRES_IN * 2)
        self.refresh_tokens.create(vals)
        return vals['token']

    @api.model
    def token(self, vals, uid=False):
        cTimestamp = int(round(datetime.datetime.now().timestamp()))
        sandbox = vals['sandbox']
        if not uid:
            _logger.info('Refresh flag has not been set, authenticating user [%s]', vals['username'])
            uid = self.authenticate(self.env.cr.dbname, vals['username'], vals['password'], {'interactive': False})
        payload = self.prepare_payload(uid, sandbox, cTimestamp, vals['nonce'])
        private_key = self.prepare_private_key()
        return {
            "access_token": self.prepare_access_token(payload, private_key, self.env.cr.dbname),
            "refresh_token": self.prepare_refresh_token({'user_id': uid, 'username':vals['username'], 'sandbox':sandbox}, cTimestamp),
            "scope": self.prepare_scope(uid),
            "token_type": "Bearer",
            "expires_in": EXPIRES_IN
        }
    
    @api.model
    def refresh(self, vals):
        refresh = vals['refresh_token']
        username = vals['username']
        currentTime = int(round(datetime.datetime.now().timestamp()))
        refresh_list = self.refresh_tokens.search_read([
            ('token','=',refresh),
            ('username','=',username),
            ('expires_in', '>', currentTime)
        ])
        if not len(refresh_list):
            raise ValidationError('IAM211: Invalid refresh token!')
        vals['sandbox'] = refresh_list[0]['sandbox']
        access_token = self.token(vals, refresh_list[0]['user_id'][0])
        self.refresh_tokens.browse([refresh_list[0]['id']]).unlink()
        return access_token

    @api.model
    def create_with_reference(self, vals):
        user = self.create(vals)
        return {
            "id": user.id,
            "login": user.login
        }