'''
This script requires "requests": http://docs.python-requests.org/
To install: pip install requests

client_id = "XXXXXXXXXXXXXX"
refresh_token = "XXXXXXXXXXXXXXXXXXC" #User Key
tenant_name = "XXXXXX"
account_logical_name = "XXXXX"
process_name = "Demo Process"
'''

import requests
import json


def get_accesstoken(client_id, refresh_token, tenant_name):

    data = { "grant_type": "refresh_token",
            "client_id": client_id,
            "refresh_token": refresh_token }
    headers = { "Content-Type" : "application/json",
                "X-UIPATH-TenantName" : tenant_name }

    req_accesstoken = requests.post("https://account.uipath.com/oauth/token", data, headers)

    response = json.loads(req_accesstoken.content)
    auth = "Bearer " + response["access_token"]

    return auth


def get_process_releasekey(auth, account_logical_name, tenant_name, process_name):
    
    req_process_releasekey = requests.get(f"https://platform.uipath.com/{account_logical_name}/{tenant_name}/odata/Releases?$filter=Name eq '{process_name}'",\
                                        headers={"Authorization": auth})
    response = json.loads(req_process_releasekey.content)
    if not response.get('value'):
        return ''
        
    release_key = response.get('value')[0].get('Key')

    return release_key


def start_job(tenant_name, account_logical_name, auth, release_key,\
            process_name, param_bool=False, parameters={}):

    headers2 = { "Content-Type" : "application/json",
                "X-UIPATH-TenantName" : tenant_name,
                "Authorization" : auth}


    startInfo = {}
    if not param_bool:
        ## Process without parameters (Simple)
        startInfo['ReleaseKey'] = release_key
        startInfo['Strategy'] = 'All'

    else:
        ## Process with parameters
        startInfo['ReleaseKey'] = release_key
        startInfo['Strategy'] = 'All'
        #startInfo['InputArguments'] = '{\"param1\":\"Test from Python\",\"param2\":\"Video Live 20:42\"}'
        startInfo['InputArguments'] = str(parameters)

    data2 ={}
    data2['startInfo'] = startInfo
    json_data = json.dumps(data2)

    print('sending uipath process post request')
    r2 = requests.post(f"https://platform.uipath.com/{account_logical_name}/{tenant_name}/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs",\
                    data = json_data, headers = headers2)

    print(r2.content)

    try:
        process_id = r2.json().get('value')[0].get('Id')
    except Exception as e:
        print(e)
        process_id = -1

    '''
    # wait for bot response
    while True:
        req_process_releasekey = requests.get(f"https://platform.uipath.com/{account_logical_name}/{tenant_name}/odata/Jobs?$filter=Id eq {process_id}",\
                                        headers={"Authorization": auth})        
        state = req_process_releasekey.json().get('value')[0].get('State')
        
        if state!='Running':
            print('status: \n' + str(req_process_releasekey.json()))
            break
                 
    return req_process_releasekey.json()
    '''
    return r2.json()


def default_start_process(client_id, refresh_token, tenant_name,\
                        account_logical_name, process_name, param_bool=False, parameters={}):

    auth = get_accesstoken(client_id, refresh_token, tenant_name)
    release_key = get_process_releasekey(auth, account_logical_name, tenant_name, process_name)
    
    return start_job(tenant_name, account_logical_name, auth, release_key,\
                    process_name, param_bool, parameters)