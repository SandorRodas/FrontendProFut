from azure.data.tables import TableServiceClient
from utils.environment import getEnvironment
import uuid
from flask import current_app, session
from utils.environment import getEnvironment
from datetime import datetime

serverConfig = getEnvironment("Server")
def SaveStorage(user, ip, code, action, module, detail):
    tokendata = session['tokendata']
    if getEnvironment('Server')['EnvMode'] != "DEV":
        ym = datetime.now()
        my_entity = {
            'PartitionKey': "FILESHARING",
            'RowKey': str(uuid.uuid4()),
            "user": user,
            "ip":   ip,
            "code": code,
            "action": action,
            "module": module,
            "detail": str(detail),
            "type": "front"
        }
        table_name = f"d{ym.strftime('%Y%m')}genyus{serverConfig['EnvMode'].split('-')[0]}appLog{tokendata['customer']}c{tokendata['contract']}"
        table_service_client = TableServiceClient.from_connection_string(conn_str=getEnvironment("connStrTable"))
        table_service_client.create_table_if_not_exists(table_name = table_name)
        table_client = table_service_client.get_table_client(table_name = table_name)
        table_client.create_entity(entity=my_entity)
    elif getEnvironment('Server')['EnvMode'] == "DEV":
        logger = current_app.logger
        logger.info(f"action = {action} , module = {module} , code = {code} , detail = {detail}")