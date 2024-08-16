from base64 import b64encode
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import jwt, datetime, uuid, logging, json, hmac, hashlib
from passlib.hash import hex_sha256 as hex_sha256


_logger = logging.getLogger(__name__)

EXPIRES_IN = 300


class adb_users(models.Model):
    _inherit = 'res.users'

    refresh_tokens = fields.One2many("adb.tokens.refresh", "user_id")

    #claims
    email_verified = fields.Boolean(default=False)
    phone_verified = fields.Boolean(default=False)
    bvn_verified = fields.Boolean(default=False)
    password_reset = fields.Boolean(default=False)

    def prepare_subscriptions(self, user):
        return [{
            "name": "OmniChannelEdgeService",
            "version": "1.0.0",
        }]
    
    def prepare_claims(self, user, checksum, secret):
        claims = {}
        partner = user.partner_id

        device_match = {'nonce':'null'}
        devices = self.env['adb.device'].search([('active','=',True),('client','=',partner.id)])
        for device in devices:
            h = hmac.new(secret.encode('UTF-8'), device.reference.encode('UTF-8'), hashlib.sha256).hexdigest()
            _logger.info('Comparing [%s] and [%s]', h, checksum)
            if (h == checksum):
                device_match['nonce'] = 'true'
            else:
                device_match['nonce'] = 'false'

        claims.update({"partner": partner.external_id})
        claims.update({"email_verified": user.email_verified})
        claims.update({"phone_verified": user.phone_verified})
        claims.update({"device_verified": device_match.get('nonce')})
        claims.update({"bvn_verified": user.bvn_verified})
        claims.update({"password_reset": user.password_reset})

        return claims

    def prepare_payload(self, uid, sandbox, cTimestamp, nonce, secret):
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
            'claims': self.prepare_claims(user, nonce, secret)
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
        payload = self.prepare_payload(uid, sandbox, cTimestamp, vals['nonce'], vals['tenant'])
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

    def check_device(self, vals):
        simple_array = [0]
        for user in self:
            partner_id = user.partner_id.id
            devices = self.env['adb.device'].search([('active','=',True),('client','=', int(partner_id))])
            if not devices:
                raise ValidationError('FDN200: No active associated devices')
            for device in devices:
                if hex_sha256.verify(device.reference, vals['checksum']):
                    simple_array.append(1)
            if not sum(simple_array):
                raise ValidationError('FDN201: Checksum failed for associated devices.')
        return True

    @api.model
    def create(self, vals):
        existing_record = self.search([('login', '=', vals.get('login'))], limit=1)
        if existing_record:
            return existing_record

        return super(adb_users, self).create(vals)

    @api.model
    def create_with_reference(self, vals):
        user = self.create(vals)
        return {
            "id": user.id,
            "login": user.login
        }

    @api.model
    def update_claim(self, vals):
        updateClaimCommand = """
        SELECT u.id from res_users u
        left join res_partner p on u.partner_id = p.id
        where p.external_id = '{partner}'
        LIMIT 1
        """.format(**vals)
        cr = self._cr
        cr.execute(updateClaimCommand)
        claim = cr.fetchone()

        if not claim:
            raise ValidationError('USRER01: Claims fetch error. User not found.')

        self.browse([claim[0]]).write({
            vals['claim']: json.loads(vals['value'])
        })
        return True