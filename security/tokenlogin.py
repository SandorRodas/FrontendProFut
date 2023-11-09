from flask import Blueprint, abort, redirect, url_for, session
from flask import current_app
from utils.environment import getEnvironment
from utils.restAPI import postREST
from config import globalConfig
from .tokenvalidation import token_valid

token_view = Blueprint('token_view', __name__, template_folder='templates')

@token_view.route('/bootUp/<boot_key>', methods=['GET'])
def bootup(boot_key):
    logger = current_app.logger
    token = ''
    payload = {
            "bootKey":boot_key,
            "app": getEnvironment('Server')['AppRoot'].replace("/", "")
            }
    getboot_key = postREST(payload, f"{getEnvironment('ApiSecurity')}/getToken", getEnvironment('RestServerSec'))
    if getboot_key['status'] == "Success":
        token = getboot_key['data']
        if getEnvironment('Server')['EnvMode'] == "DEV":
            logger.info(f"Token={token}")
    token_valid(current_app, session, abort, token)
    return redirect(url_for(globalConfig['home']))
