'''
This script requires "requests": http://docs.python-requests.org/
To install: pip install requests

client_id = "XXXXXXXXXXXXXX"
refresh_token = "XXXXXXXXXXXXXXXXXXC" #User Key
tenant_name = "XXXXXX"
account_logical_name = "XXXXX"
process_name = "Demo Process"
'''

import json
from flask_lambda import FlaskLambda
from flask import request
from start_process import default_start_process
import json


app = FlaskLambda(__name__)


@app.route('/test', methods=['GET'])
def test():
    return 'Test correct'


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():

    req = request.get_json(force=True)
    query_result = req.get('queryResult')
    intent_action_name = query_result.get('action')

    # Trigger UiPath process

    client_id = request.headers.get('client_id')
    refresh_token = request.headers.get('refresh_token') #User Key
    tenant_name = request.headers.get('tenant_name')
    account_logical_name = request.headers.get('account_logical_name')
    process_name = request.headers.get('process_name')

    chatbot_parameters = query_result.get('parameters')

    process_response = default_start_process(client_id, refresh_token, tenant_name,\
                        account_logical_name, process_name, chatbot_parameters, intent_action=intent_action_name)
    
    print(process_response)
    
    fulfillment_text = ''

    response = {
                "fulfillmentText": fulfillment_text,
                "source": "webhookdata"
            }
    
    return response