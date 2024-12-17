import logging
import base64
import simplejson

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.home import Home
from odoo.addons.web.controllers.utils import ensure_db

import werkzeug.utils
from werkzeug.urls import url_encode, url_decode


_logger = logging.getLogger(__name__)

class CustomAuth(Home):

    @http.route('/web/login')
    def web_login(self, *args, **kw):
        ensure_db()
        if request.httprequest.method == 'POST' or 'admin' in request.params:
            _logger.info("Admin parameter value is set or request is 'POST'")
            return super().web_login(*args, **kw)
        
        try:
            provider = request.env['auth.oauth.provider'].sudo().search([('enabled', '=', True)], limit=1)
            if not provider:
                _logger.warning("No suitable OAuth providers found.")
                return super().web_login(*args, **kw) # Fallback if no provider

            state = {
                'r': kw.get('redirect') or '/',
                'csrf_token': request.csrf_token()  # Essential for security
            }


            params = dict(url_decode(provider.auth_endpoint.split("?")[-1])) # convert mapping to dict
            state_str = simplejson.dumps(state)
            params["state"] = base64.urlsafe_b64encode(state_str.encode('utf-8')).decode("utf-8")  # Encode and decode to string

            params["redirect_uri"] = request.httprequest.url_root + "oidc/signin"
            auth_url = f"{provider.auth_endpoint}?{url_encode(params)}"
            return werkzeug.utils.redirect(auth_url)

        except Exception as e:
            _logger.exception("Error in OAuth redirect: %s", e)
            return super().web_login(*args, **kw)
        

    @http.route('/web/session/logout', type='http', auth="none")
    def logout(self, redirect='/'):  
        _logger.info("Logout method called. Redirect URL: %s", redirect)
        request.session.logout(keep_db=True)
        return werkzeug.utils.redirect(redirect)