# Copyright 2016 ICTSTUDIO <http://www.ictstudio.eu>
# Copyright 2021 ACSONE SA/NV <https://acsone.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import base64
import hashlib
import logging
import secrets
import simplejson

import werkzeug.utils

from odoo import http

from werkzeug.urls import url_decode, url_encode, url_parse, url_join

from odoo.addons.auth_oauth.controllers.main import OAuthLogin


_logger = logging.getLogger(__name__)

class OpenIDLogin(OAuthLogin):
    def list_providers(self):
        providers = super().list_providers()
        for provider in providers:
            flow = provider.get("flow")
            if flow in ("id_token", "id_token_code"):
                params = url_decode(provider["auth_link"].split("?")[-1])
                #14/12/24: Remove illegal character from state .. causes error with WSO2IS7 - Seyi Akamo
                state_str = params.get("state")
                params["state"] = base64.urlsafe_b64encode(state_str.encode('utf-8'))
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
    def signin(self, **kw):
        try:
            if 'state' not in kw:
                _logger.error("OAuth2: No state parameter found.")
                url = "/web/login?oauth_error=2"  # Or handle as appropriate
                return werkzeug.utils.redirect(url)

            # URL-safe decode and handle potential padding issues:
            encoded_state = kw['state']
            try:
                state_bytes = base64.urlsafe_b64decode(encoded_state)
            except base64.binascii.Error:  # Padding error
                padding = len(encoded_state) % 4
                if padding > 0:
                    encoded_state += '=' * (4 - padding)
                state_bytes = base64.urlsafe_b64decode(encoded_state)

            state_str = state_bytes.decode('utf-8') # Decode bytes to string (UTF-8)

            original_url = http.request.httprequest.url
            parsed_url = url_parse(original_url)
            all_query_params = url_decode(parsed_url.query)
            
            if 'state' in all_query_params:
                state = simplejson.loads(state_str)  # state_str comes from your existing decoding logic
                state.update(all_query_params) # Update with existing params
                all_query_params['state'] = simplejson.dumps(state)

            query_string = url_encode(all_query_params) # Encode the complete set of query params
            final_url = url_join('/auth_oauth/signin', f"?{query_string}") # Construct the final URL

            return werkzeug.utils.redirect(final_url)

        except (ValueError, TypeError, simplejson.JSONDecodeError, KeyError) as e:  # Handle all possible exceptions
            _logger.exception("OAuth2 error: %s", str(e))  # Log the exception for debugging
            url = "/web/login?oauth_error=2"  # Handle errors gracefully
            return werkzeug.utils.redirect(url)


        except Exception as e:  
            _logger.exception("OAuth2: Unexpected error: %s", str(e))
            url = "/web/login?oauth_error=2"
            return werkzeug.utils.redirect(url)