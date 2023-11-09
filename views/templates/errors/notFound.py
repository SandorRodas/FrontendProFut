import json
import base64
import random
import string
import bcrypt
import sys
import datetime
import requests

from flask import Blueprint, render_template, session, abort, request, url_for, redirect
from flask import current_app


not_found_view = Blueprint('not_found_view', __name__,
                       template_folder='templates', static_folder='static')


@not_found_view.route('/notFound', methods=["GET", "POST"])
def mainView():
    # Debug Messages
    # flashMessages = []

    # rfc = tokenData['customer']
    
    # now = datetime.datetime.now()

    # Render info
    globalConfig = {
        'title': 'PRO FUT',
        'description': '',
        'footerLeft': '',
        'footerRight': '',
        'home': 'portal_view.mainView',
    }
    pageConfig = {
        'title': 'PRO FUT',
        'subtitle': '',
        'description': '',
        'detail': ''
    }

    return render_template("/errors/404.html", globalconfig=globalConfig, pageconfig=pageConfig)
