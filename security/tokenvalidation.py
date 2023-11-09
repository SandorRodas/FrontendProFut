import http.client
import json
from utils.environment import getEnvironment
from functools import wraps


class tokenAuthenticationError(SystemError):
    '''raise this when there's a authentication error'''

#
# Función que autentica el token por medio del servicio web
#


def authSession(token):
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    connection = http.client.HTTPSConnection(getEnvironment('RestServerSec'))
    header = {
        'token' : token
    }
    connection.request("POST", f"{getEnvironment('ApiSecurity')}/getSessionInformationV2", headers=header)
    response = connection.getresponse()
    data = response.read().decode("UTF-8")
    connection.close()
    return json.loads(data)

#
# Validate a given token.
# Must be called when the app starts.
# The standard login entrypoint calls it.
#


def token_valid(app, session, abort, token):
    try:
        app.logger.info("Authenticating...")
        data = authSession(token)
        if data["status"] == "Success":
            session['token'] = token
            session['tokendata'] = data
            session['customer'] = data.get('customer', 'NO CUSTOMER')
            app.logger.info("Authenticated")
        else:
            raise tokenAuthenticationError("Authentication Required")
    except tokenAuthenticationError as e:
        app.logger.error(f"Invalid token: {e}")
        abort(401)
    except Exception as e:
        app.logger.error(f"Validating token: {e}")
        abort(503)

#
# Decorator to confirm that a given call has a token in its session
# All the routes MUST have this decorator
#


def token_required(app, session, abort):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not 'token' in session:
                app.logger.error("Token Required")
                abort(401)
            token = session['token']
            token_valid(app, session, abort, token)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

#
# Decorator to confirm that a given call has a token with at least a given role
#


def role_required(app, session, abort, roles_list):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not 'tokendata' in session or not 'roles' in session['tokendata']:
                app.logger.error("Token Required")
                abort(401)
            else:
                for role in session['tokendata']['roles']:
                    if role in roles_list:
                        return f(*args, **kwargs)
                app.logger.error("Invalid role")
                abort(401)
        return decorated_function
    return decorator
