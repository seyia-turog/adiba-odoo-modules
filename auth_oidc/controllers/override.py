import logging
import base64
import simplejson

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.home import Home
from odoo.addons.web.controllers.utils import ensure_db
from . import main

import werkzeug.utils
from werkzeug.urls import url_encode, url_decode, url_quote


_logger = logging.getLogger(__name__)

class CustomAuth(Home):

    @http.route('/web/login')
    def web_login(self, *args, **kw):
        ensure_db()
        if request.httprequest.method == 'POST' or 'admin' in request.params:
            _logger.info("Admin parameter value is set or request is 'POST'")
            return super().web_login(*args, **kw)
        
        try:

            oidc_login = main.OpenIDLogin()
            providers = oidc_login.list_providers()

            if not providers or not isinstance(providers, list) or not providers[0].get('auth_link'): # basic validation check
                _logger.error("Could not retrieve valid providers or auth_link from OpenIDLogin.")
                return super().web_login(*args, **kw)

            auth_url = providers[0].get('auth_link')  # Get the first provider's auth_link

            return werkzeug.utils.redirect(auth_url)
        
        except Exception as e:
            _logger.exception("Error in web_login: %s", e)
            return super().web_login(*args, **kw)

    @http.route('/web/session/logout', type='http', auth="none")
    def logout(self, redirect='/'):  
        _logger.info("Logout method called. Redirect URL: %s", redirect)
        request.session.logout(keep_db=True)
        return werkzeug.utils.redirect(redirect)