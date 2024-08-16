from unicodedata import category, name
from odoo import api, fields, models
import logging, base64, json, requests

_logger = logging.getLogger(__name__)

class adb_merchants(models.Model):
    _name = 'adb.merchant.cfg'
    _description = 'Bills Merchants'
    # _sql_constraints = [('identifier_unique', 'unique(identifier)','Cannot have multiple configs of the same identifier')]


    #Security Tab
    # identifier = fields.Selection([('FLUTTERWAVE','Flutterwave Inc.'),('TERMII','Termii Inc.'),('SENDLITE','SendLite Inc.'),('IDENTITYPASS','Indentity Pass'),('APILAYER','API Layer Inc.'),('ABSTRACT','Abstract API'),('NIBSS-NIP','NIBSS Instant Payment'),('NIBSS-CARD','NIBSS Cards Services'),('PAYSTACK','Paystack Inc.')])
    identifier = fields.Char()
    endpoint = fields.Char() #NIBBS-NIP etc
    encryption_key = fields.Char(string="Encrpytion Key") #PGP Encrypt
    secret_key = fields.Char("Secret Key") #PGP Encrypt
    public_key = fields.Char("Public Key") #PGP Encrypt

    # instance is commented because production database should have production merchant, same with sandbox db
    # instance = fields.Char("Instance") #sandbox / production

    provider = fields.Many2one('res.partner') #domain to merchants
    services = fields.Many2many('adb.merchant.service')
    config_rank = fields.Integer()

    @api.model
    def cron_primeairtime_authenticate(self):
        cron_configs = self.search([['identifier','=','PRIMEAIRTIME']])
        if len(cron_configs):
            cron_config = cron_configs[0]
            identifier = cron_config.identifier
            endpoint = cron_config.endpoint
            credentials = base64.b64decode(cron_config.encryption_key).decode('utf-8')
            username = credentials.split(':')[0]
            password = credentials.split(':')[1]

            json_data = {"username": username, "password": password}
            headers = {"Content-Type": "application/json", "Accept": "application/json", "Cache-Control": "no-cache"}
            response = requests.post(f'{endpoint}/api/auth', data=json.dumps(json_data), headers=headers)

            _logger.info(f'Authenticating {identifier} with endpoint [{endpoint}] .......... response: {response.status_code} - {response.reason}')
            
            if response.ok:
                token = response.json().get('token')
                cron_config.write({'secret_key': token})
        return None

class adb_merchant_services(models.Model):
    _name = 'adb.merchant.service'
    _description = 'Merchant Services'
    _sql_constraints = [('service_unique', 'unique(service)','Cannot have multiple services of the same name')]

    service = fields.Char('Service Name')
    category_id = fields.Many2one('adb.merchant.service.category')
    merchant_configs = fields.Many2many('adb.merchant.cfg')

    @api.model
    def get_merchant_configs(self, service):
        # service_records = self.search([['service','=',service]]).read(['merchant_configs'])
        # return service_records[0]['merchant_configs']
        active_merchant = [{}]
        service_records = self.search([['service','=',service]])
        if len(service_records):
            service_merchants = service_records[0].merchant_configs
            if len(service_merchants):
                active_merchants = service_merchants.sorted(key=lambda r: r.config_rank)
                active_merchant = active_merchants[0].read(['secret_key','public_key','identifier','endpoint','encryption_key'])
        return active_merchant

class adb_merchant_service_categories(models.Model):
    _name = 'adb.merchant.service.category'
    _description = 'Merchant Service Categories'

    category = fields.Char('Service Category')