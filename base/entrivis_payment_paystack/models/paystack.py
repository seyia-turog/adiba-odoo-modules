# -*- coding: utf-'8' "-*-"
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2020-Today Entrivis Tech PVT. LTD. (<http://www.entrivistech.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
# coding: utf-8

import logging
from werkzeug import urls

from odoo.http import request
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import ValidationError
from odoo.addons.entrivis_payment_paystack.controllers.main import PaystackController


_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """ Override of payment to return Paystack-specific rendering values.

        Note: self.ensure_one() from `_get_processing_values`

        :param dict processing_values: The generic and specific processing values of the transaction
        :return: The dict of acquirer-specific processing values
        :rtype: dict
        """
        res = super()._get_specific_rendering_values(processing_values)
 
        if self.provider != 'paystack':
            return res

        base_url = self.acquirer_id.get_base_url()
        # adding authorization key to send them through the headers to the api call
        return_url = urls.url_join(base_url, PaystackController._return_url)
        notify_url = urls.url_join(base_url, PaystackController._return_url)
        values = {
            'Authorization': 'Bearer ' + self.acquirer_id.paystack_secret_key,
            'Content-Type': 'application/json',
            'name': self.partner_name,
            'amount': self.amount * 100,
            'description': 'Reference no :' + self.reference,
            'notify_url': notify_url,
            'cancel_return': return_url,
            'return_url': return_url,
            'item_reference': self.reference,
        }
        request.session['paystack_reference'] = self.reference
        return values

    def _process_feedback_data(self, data):
        super()._process_feedback_data(data)
        if self.provider != 'paystack':
            return

        status = data.get('status')
        error = data.get('error')
        if status and status == 'success' and not error:
            # adding the reference from paystack transaction into the payment transaction as acquire reference
            self.with_user(SUPERUSER_ID).write({'acquirer_reference': data.get('reference')})
            self.with_user(SUPERUSER_ID)._set_done()
            return True
        elif status and not error:
            # if the status is pending than also adding reference of paystack into the odoo transaction for the future reference
            self.with_user(SUPERUSER_ID).write({'acquirer_reference': data.get('reference')})
            self.with_user(SUPERUSER_ID)._set_pending()
            return True
        else:
            error = _('Paystack: feedback error')
            _logger.info(error)
            self.with_user(SUPERUSER_ID).write({'state_message': error})
            self.with_user(SUPERUSER_ID)._set_canceled()
            return False

    @api.model
    def _get_tx_from_feedback_data(self, provider, data):
        """ Override of payment to find the transaction based on Paystack data.

        :param str provider: The provider of the acquirer that handled the transaction
        :param dict data: The feedback data sent by the provider
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if the data match no transaction
        """
        tx = super()._get_tx_from_feedback_data(provider, data)
        if provider != 'paystack':
            return tx

        if not tx and data.get('transaction_id'):
            tx = data.get('transaction_id')

        reference = data.get('transactionReference')

        if not reference:
            raise ValidationError(
                "Paystack: " + _(
                    "Received data with missing reference %(r)s or txn_id %(t)s.",
                    r=reference, t=tx
                )
            )

        if not tx:
            tx = self.search([('reference', '=', reference), ('provider', '=', 'paystack')])

        if not tx:
            raise ValidationError(
                "Paystack: " + _("No transaction found matching reference %s.", reference)
            )
        return tx


class AcquirerPaystack(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('paystack', 'Paystack')], ondelete={'paystack': 'set default'})
    paystack_secret_key = fields.Char('Secret Key')

    @api.model
    def _paystack_get_api_url(self, environment):
        """ Return the API URL according to the acquirer state.
            Note: self.ensure_one()
            :return: The API URL
            :rtype: str
        """
        return {
            'paystack_form_url': 'https://api.paystack.co/page',
        }

    def _get_default_payment_method_id(self):
        self.ensure_one()
        if self.provider != 'paystack':
           return super()._get_default_payment_method_id()
        return self.env.ref('entrivis_payment_paystack.payment_method_paystack').id


class AccountPaymentMethod(models.Model):
    _inherit = 'account.payment.method'

    @api.model
    def _get_payment_method_information(self):
        res = super()._get_payment_method_information()
        res['paystack'] = {'mode': 'unique', 'domain': [('type', '=', 'bank')]}
        return res
