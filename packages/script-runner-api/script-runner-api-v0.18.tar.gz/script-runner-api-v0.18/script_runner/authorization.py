"""Utilities for API authorization."""

import json

from functools import wraps
from six.moves.urllib.request import urlopen
from jose import jwt

from flask import request
from flask_cors import cross_origin

from script_runner.server import app, api


# Auth Errors -----------------------------------------------------------------

class AuthError(Exception):
    """Represents a failure during authentication"""
    def __init__(self, error, status_code=401):
        super(AuthError, self).__init__(error)
        self.error = error
        self.status_code = status_code

@cross_origin()
@api.errorhandler(AuthError)
def handle_auth_error(ex):
    """Flask error handler"""
    return ex.error, ex.status_code


# Auth Helpers ----------------------------------------------------------------

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header"""
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({
            "code": "authorization_header_missing",
            "description": "Authorization header is expected"
        }, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must start with Bearer"
        }, 401)
    if len(parts) == 1:
        raise AuthError({
            "code": "invalid_header",
            "description": "Token not found"
        }, 401)
    if len(parts) > 2:
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must be Bearer token"
        }, 401)

    token = parts[1]
    return token

def decode_jwt():
    token = get_token_auth_header()
    jsonurl = urlopen("https://"+app.config['AUTH0_DOMAIN']+"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            return jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=app.config['AUTH0_API_AUDIENCE'],
                issuer="https://"+app.config['AUTH0_DOMAIN']+"/"
            )
        except jwt.ExpiredSignatureError:
            raise AuthError({
                "code": "token_expired",
                "description": "token is expired"
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                "code": "invalid_claims",
                "description": "incorrect claims, please check the audience and issuer"
            }, 401)
        except Exception:
            raise AuthError({
                "code": "invalid_header",
                "description": "Unable to parse authentication token."
            }, 401)


# Decorators ------------------------------------------------------------------

def requires_auth(f):
    """Determines if the Access Token is valid"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if app.config['AUTH_PROVIDER'] == 'none':
            request.current_user = {'sub': '42'}
            return f(*args, **kwargs)
        elif app.config['AUTH_PROVIDER'] == 'auth0':
            payload = decode_jwt()
            if payload:
                request.current_user = payload
                return f(*args, **kwargs)
            raise AuthError({
                "code": "invalid_header",
                "description": "Unable to find appropriate key"
            }, 401)
        return f(*args, **kwargs)
    return decorated
