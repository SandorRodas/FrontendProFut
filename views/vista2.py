from flask import Blueprint, render_template, session, abort, request
from flask import current_app

from security.tokenvalidation import token_required
from config import globalConfig, pageConfig, getSessionDefaults
from utils.restAPI import postREST
from utils.environment import getEnvironment

vista2 = Blueprint('vista2', __name__,
                        template_folder='templates', static_folder='static')


@vista2.route('/vista2', methods=['GET','POST'])
def mainView():
    customer, sidebar = getSessionDefaults(session)

    flashMessages = []
    pageConfig['title'] = "PORTAL TITLE"
    pageConfig['description'] = customer
    pageConfig['detail'] = str(getEnvironment('Server')['EnvMode'])
    faq = None

    
    return render_template('vista2.html', pageConfig=pageConfig, globalconfig=globalConfig, flashMessages=flashMessages, sidebar=sidebar, faq=faq)
