from flask import Blueprint
from flask import jsonify
from flask import current_app

data_mockup = Blueprint('data_mockup', __name__)

mockup_data_set_information={
    "status": "Success",
    "actionList": "OK"
}
mockup_data_get_information ={
        "status": "Success",
        "actionList": [
            {
                "TestOutputID": "21",
                "TaxID": "ROGA940529",
                "FullName": "Jose123Rosales",
                "User": "18",
                "Steps": "1",
                "BatchID": "8",
                "AuditRecord": "2019-09-18T18:09:45.761775-05:00"
            },
            {
                "TestOutputID": "22",
                "TaxID": "ROGA940529",
                "FullName": "Jose123Rosales",
                "User": "18",
                "Steps": "1",
                "BatchID": "9",
                "AuditRecord": "2019-09-18T18:14:53.039613-05:00"
            },
            {
                "TestOutputID": "23",
                "TaxID": "ROGA940529",
                "FullName": "Jose123Rosales",
                "User": "18",
                "Steps": "1",
                "BatchID": "10",
                "AuditRecord": "2019-09-18T18:17:55.724225-05:00"
            },
            {
                "TestOutputID": "24",
                "TaxID": "ROGA940529",
                "FullName": "Armando00Rosales",
                "User": "18",
                "Steps": "1",
                "BatchID": "11",
                "AuditRecord": "2019-09-18T18:31:16.011507-05:00"
            },
            {
                "TestOutputID": "25",
                "TaxID": "ROGA940529",
                "FullName": "ArmandoRosales",
                "User": "18",
                "Steps": "1",
                "BatchID": "12",
                "AuditRecord": "2019-09-18T18:36:22.571332-05:00"
            }
        ]
}
@data_mockup.route('/templateApiGo/getActionMessage', methods=['POST'])
def getMessage():
    logger = current_app.logger 
    response = mockup_data_get_information
    logger.info(f"Response={response}")
    return jsonify(response)

@data_mockup.route('/templateApiGo/setActionMessage', methods=['POST'])
def setMessage():
    logger = current_app.logger 
    response = mockup_data_set_information
    logger.info(f"Response={response}")
    return jsonify(response)