from views.portal import portal_view
from views.templates.errors.notFound import not_found_view
from security.tokenlogin import token_view
from flask import Flask, render_template, redirect, url_for
from flask.logging import create_logger
from flask_pymongo import PyMongo
from logging.config import dictConfig
from base64 import b64decode
from utils.environment import loadEnvironment, getEnvironment
from config import globalConfig
from werkzeug.exceptions import InternalServerError, Unauthorized, ServiceUnavailable, NotFound, BadGateway, GatewayTimeout


#
#   Create app and load ENV
#
loadEnvironment(".env.json")
serverConfig = getEnvironment("Server")
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s: %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
app.config['SESSION_COOKIE_NAME'] = serverConfig['SessionName']
app.config['SESSION_COOKIE_SECURE'] = True
logger = create_logger(app)
app.secret_key = b64decode(serverConfig['Secret'])
rooturl = serverConfig['AppRoot']
logger.info(f"ENV_MODE: {serverConfig['EnvMode']}")

@app.after_request
def remove_header(response):
    response.headers['Server'] = "Undisclosed"
    return response

@app.errorhandler(InternalServerError)
def handle_500(e):
    original = getattr(e, "original_exception", None)

    if original is None:
        # direct 500 error, such as abort(500)
        return render_template("/errors/500.html", globalconfig=globalConfig, env=serverConfig['EnvMode']), 500

    # wrapped unhandled error
    return render_template("/errors/500_unhandled.html", e=original, globalconfig=globalConfig, env=serverConfig['EnvMode']), 500

@app.errorhandler(Unauthorized)
def handle_401(e):
    return render_template("/errors/401.html", globalconfig=globalConfig, env=serverConfig['EnvMode']), 401

@app.errorhandler(ServiceUnavailable)
def handle_503(e):
    return render_template("/errors/503.html", globalconfig=globalConfig, env=serverConfig['EnvMode']), 503

@app.errorhandler(NotFound)
def handle_404(e):
    return redirect(url_for('not_found_view.mainView'))

@app.errorhandler(BadGateway)
def handle_502(e):
    return render_template("/errors/502.html", globalconfig=globalConfig, env=serverConfig['EnvMode']), 502 

@app.errorhandler(GatewayTimeout)
def handle_504(e):
    return render_template("/errors/504.html", globalconfig=globalConfig, env=serverConfig['EnvMode']), 504 

#
# Add Standard Login entrypoint for InTaxlligence
#
app.register_blueprint(token_view, url_prefix=rooturl)

#
# Add Mockups for REST services in DEV
# You may add your own services in additional modules
# No service should be exposed in UAT / PROD
#
if serverConfig['EnvMode'] == "DEV":
    from rest_mockups.token_mockup import token_mockup
    app.register_blueprint(token_mockup)


#
# Add Mockups for API rest Golang in DEV
# You may add your own services in additional modules
# No service should be exposed in UAT / PROD
#
if serverConfig['EnvMode'] == "DEV":
    from rest_mockups.data_mockup import data_mockup
    app.register_blueprint(data_mockup)
    from rest_mockups.portal_mockup import portal_mockup
    app.register_blueprint(portal_mockup)


#
# Add Custom Views
#
app.register_blueprint(portal_view, url_prefix=rooturl)
app.register_blueprint(not_found_view, url_prefix=rooturl)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=443, ssl_context='adhoc')
    # app.run(debug=True, host='0.0.0.0')
