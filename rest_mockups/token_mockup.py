from flask import Blueprint
from flask import jsonify
from flask import current_app, request

token_mockup = Blueprint('token_mockup', __name__)

mockup_data = {
  '001': {'user': 'user01@portal.ey.com', 'contract': 40, 'customer': 'MAN9209143V1', 'token': '458b0771-b65a-45af-98aa-8e8c9a415a9f', 'language': 'es_MX', 'roles': ['EMP_PORTAL_USER', 'EMP_PORTAL_ADMIN'], 'status': 'Success'},
  '002': {'user': 'user02@portal.ey.com', 'contract': 40, 'customer': 'MAN9209143V1', 'token': '458b0771-b65a-45af-98aa-8e8c9a415a9f', 'language': 'es_MX', 'roles': ['EMP_PORTAL_USER', 'EMP_PORTAL_TEST'], 'status': 'Success'},
  'Error': {'status':'Error', 'message':'Invalid'}
}

mockup_bootkey = {
    '001' : {
      "data": "001",
      "detail": "",
      "status": "Success"
    }
}

@token_mockup.route('/appSecServ/getSessionInformationV2', methods=['POST'])
def sesion_info():
  inputheader = dict(request.headers)
  logger = current_app.logger
  
  logger.info(f"Received Token={inputheader['Token']}")
  response = mockup_data[inputheader['Token']]

  logger.info(f"Response={response}")
  return jsonify(response)


@token_mockup.route('/appSecServ/getToken', methods=['POST'])
def bootup():
  data = request.json
  logger = current_app.logger
  logger.info(data)
  response = mockup_bootkey[data['bootKey']]

  logger.info(f"Response={response}")
  return jsonify(response)
