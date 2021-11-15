from flask import Flask, request
from start_process import default_start_process
import json


app = Flask(__name__)


@app.route('/test', methods=['GET'])
def test():
    return 'Test correct'


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():

    req = request.get_json(force=True)
    query_result = req.get('queryResult')

    client_id = request.headers.get('client_id')
    refresh_token = request.headers.get('refresh_token') #User Key
    tenant_name = request.headers.get('tenant_name')
    account_logical_name = request.headers.get('account_logical_name')
    process_name = request.headers.get('process_name')
    param_bool = request.headers.get('param_bool')
    param_bool = bool( str(param_bool).lower() == 'true')

    chatbot_parameters = query_result.get('parameters')

    process_response = default_start_process(client_id, refresh_token, tenant_name,\
                        account_logical_name, process_name, param_bool, chatbot_parameters)
    process_response = process_response.get('value')[0].get('OutputArguments')
    
    if process_response: process_response = json.loads(process_response).get('chatbot_response')

    print(process_response)
    
    fulfillment_text = ''
    #if query_result.get('action')=='create_event':
    #    event_name = query_result.get('parameters').get('event_name')
    #fulfillment_text = process_response

    response = {
                "fulfillmentText": fulfillment_text,
                "source": "webhookdata"
               }
    
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)