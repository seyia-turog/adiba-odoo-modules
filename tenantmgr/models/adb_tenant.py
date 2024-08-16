# -*- coding: utf-8 -*-

from odoo import models, fields, api
import uuid, logging

_logger = logging.getLogger(__name__)


class adb_tenant(models.Model):
    _inherit = 'res.partner'
    # TODO-#1: All listed ranks are exclusive (e.g. you cannot be a client and a tenent etc.)
    # -- You can use SQL contraints or @api.onchange decorator (preference is for SQ constraint)

    tenant_id = fields.Many2one('res.partner')                          #TODO: restrct the partner list to just tenants.
    tenant_rank = fields.Integer(string="Tenant Rank")                  #tenant rank is used to determine the subscription tiers (gold, silver, etc.)
    tenant_admin_rank = fields.Integer(string="Tenant admin Rank")      #user rank for determining the admin level
    tenant_contact_rank = fields.Integer(string="Tenant Contact Rank")
    cba_configuration = fields.One2many('adb.servers.cba','tenant_id')
    bpm_configuration = fields.One2many('adb.servers.bpm','tenant_id')
    erp_configuration = fields.One2many('adb.servers.erp','tenant_id')
    fnd_configuration = fields.One2many('adb.servers.fnd','tenant_id')
    iam_configuration = fields.One2many('adb.servers.iam','tenant_id')
    hdsk_configuration = fields.One2many('adb.servers.hdsk','tenant_id')
    tenant_ref = fields.Char(string="Tenant Reference", default="-")

    # @api.model
    # def create(self, vals):
    #     if 'tenant_rank' in vals:
    #         if int(vals['tenant_rank']) > 0:
    #             vals['tenant_ref'] = uuid.uuid4()
    #         if vals['country']:
    #             country = self.env['res.country'].search([('code','=',vals['country'])])
    #             vals['country_id'] = country[0].id
    #             del(vals['country'])
    #     return super(models.Model, self).create(vals)
    
    @api.model
    def get_all_config(self, tenant_id):
        app_list = ['bpm', 'cba', 'erp', 'fnd', 'hdsk', 'iam']

        all_config = []
        for app in app_list:
            app_config = self.get_app_config(tenant_id, app)
            all_config.append({'name': app, 'config': app_config})
            
        return all_config
        
    @api.model
    def get_app_config(self, vals):
        model_name = 'adb.servers.' + vals['app_name']
        tenant_id = self.search([('tenant_ref','=',vals['tenant_ref'])])
        tenant_list = self.env[model_name].search_read([('tenant_id','=',tenant_id.id),('sandbox', '=', vals['sandbox'])])
        return tenant_list