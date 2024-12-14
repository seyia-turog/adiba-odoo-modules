# Copyright 2016 ICTSTUDIO <http://www.ictstudio.eu>
# Copyright 2021 ACSONE SA/NV <https://acsone.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import base64
import functools
import hashlib
import http
import logging
import secrets
import simplejson
import werkzeug.utils
import openerp

from openerp import SUPERUSER_ID

from openerp.modules.registry import RegistryManager

from werkzeug.urls import url_decode, url_encode

from werkzeug.exceptions import BadRequest

from odoo.addons.auth_oauth.controllers.main import OAuthLogin

from openerp.addons.web.controllers.main import set_cookie_and_redirect, login_and_redirect

_logger = logging.getLogger(__name__)


#----------------------------------------------------------
# helpers
#----------------------------------------------------------
def fragment_to_query_string(func):
    @functools.wraps(func)
    def wrapper(self, *a, **kw):
        if not kw:
            return """<html><head><script>
                var l = window.location;
                var q = l.hash.substring(1);
                var r = l.pathname + l.search;
                if(q.length !== 0) {
                    var s = l.search ? (l.search === '?' ? '' : '&') : '?';
                    r = l.pathname + l.search + s + q;
                }
                if (r == l.pathname) {
                    r = '/';
                }
                window.location = r;
            </script></head><body></body></html>"""
        return func(self, *a, **kw)
    return wrapper

class OpenIDLogin(OAuthLogin):
    def list_providers(self):
        providers = super().list_providers()
        for provider in providers:
            flow = provider.get("flow")
            if flow in ("id_token", "id_token_code"):
                params = url_decode(provider["auth_link"].split("?")[-1])
                #14/12/24: Remove illegal character from state .. causes error with WSO2IS7 - Seyi Akamo
                params["state"] = base64.urlsafe_b64encode(params["state"])
                # nonce
                params["nonce"] = secrets.token_urlsafe()
                # response_type
                if flow == "id_token":
                    # https://openid.net/specs/openid-connect-core-1_0.html
                    # #ImplicitAuthRequest
                    params["response_type"] = "id_token token"
                elif flow == "id_token_code":
                    # https://openid.net/specs/openid-connect-core-1_0.html#AuthRequest
                    params["response_type"] = "code"
                # PKCE (https://tools.ietf.org/html/rfc7636)
                code_verifier = provider["code_verifier"]
                code_challenge = base64.urlsafe_b64encode(
                    hashlib.sha256(code_verifier.encode("ascii")).digest()
                ).rstrip(b"=")
                params["code_challenge"] = code_challenge
                params["code_challenge_method"] = "S256"
                # scope
                if provider.get("scope"):
                    if "openid" not in provider["scope"].split():
                        _logger.error("openid connect scope must contain 'openid'")
                    params["scope"] = provider["scope"]
                # auth link that the user will click
                provider["auth_link"] = "{}?{}".format(
                    provider["auth_endpoint"], url_encode(params)
                )
        return providers
    
    #14/12/24: Remove illegal character from state .. causes error with WSO2IS7 - Seyi Akamo
    @http.route('/oidc/signin', type='http', auth='none')
    @fragment_to_query_string
    def signin(self, **kw):
        state_obj = base64.urlsafe_b64decode(kw['state'])
        state = simplejson.loads(state_obj)
        dbname = state['d']
        provider = state['p']
        context = state.get('c', {})
        registry = RegistryManager.get(dbname)
        with registry.cursor() as cr:
            try:
                u = registry.get('res.users')
                credentials = u.auth_oauth(cr, SUPERUSER_ID, provider, kw, context=context)
                cr.commit()
                action = state.get('a')
                menu = state.get('m')
                redirect = werkzeug.url_unquote_plus(state['r']) if state.get('r') else False
                url = '/web'
                if redirect:
                    url = redirect
                elif action:
                    url = '/web#action=%s' % action
                elif menu:
                    url = '/web#menu_id=%s' % menu
                return login_and_redirect(*credentials, redirect_url=url)
            except AttributeError:
                # auth_signup is not installed
                _logger.error("auth_signup not installed on database %s: oauth sign up cancelled." % (dbname,))
                url = "/web/login?oauth_error=1"
            except openerp.exceptions.AccessDenied:
                # oauth credentials not valid, user could be on a temporary session
                _logger.info('OAuth2: access denied, redirect to main page in case a valid session exists, without setting cookies')
                url = "/web/login?oauth_error=3"
                redirect = werkzeug.utils.redirect(url, 303)
                redirect.autocorrect_location_header = False
                return redirect
            except Exception as e:
                # signup error
                _logger.exception("OAuth2: %s" % str(e))
                url = "/web/login?oauth_error=2"

        return set_cookie_and_redirect(url)
        
