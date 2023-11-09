from utils.environment import getEnvironment
from json import loads, dumps
import http.client
from flask import current_app, session


def callREST(headers, data, method, url, server=None):
    logger = current_app.logger
    if server is None:
        server = getEnvironment("RestServer")
    logger.info(f"Method={method}, URL={url}, SERVER={server}")

    try:
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context
        # 1. Call REST
        connection = http.client.HTTPSConnection(server)
        connection.request(method, url, body=data, headers=headers)
        response = connection.getresponse()

        # 2. Confirm valid response
        logger.info(f"Response Status: {response.status}")
        if response.status >= 200 and response.status < 300:
            data = response.read()
            # logger.info(f"Response Data: '{data}'")

            # 3. Process response
            json_data = loads(data)
            # logger.info(f"JSON Data: '{json_data}'")
            respuesta = json_data

        else:
            respuesta = loads(
                '{"status": "Error", "detail":"HTTP CODE: '+str(response.status)+'", "data":[]}')

    except Exception as e:
        logger.error(f"Exception: {e}")
        respuesta = loads(
            '{"status": "Error", "detail":"'+str(e)+'", "data":[]}')

    finally:
        connection.close()

    return respuesta


def postREST(payload, url, server=None):

    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
    }
    method = "POST"
    postURL = url 
    try:
        data = dumps(payload)
        response = callREST(headers, data, method, postURL, server)
    except Exception as e:
        response = loads(
            '{"status": "Error", "detail":"POSTREST: '+str(e)+'", "data":[]}')
    return response

def postRESTHeader(payload,  url, server=None):
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'token' : session["token"],
    }
    method = "POST"
    post_url = url
    try:
        data = dumps(payload)
        response = callREST(headers, data, method, post_url, server)
    except Exception as e:
        response = loads(
            '{"status": "Error", "detail":"POSTREST: '+str(e)+'", "data":[]}')
    return response