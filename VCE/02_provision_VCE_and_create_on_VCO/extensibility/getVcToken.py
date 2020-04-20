import json
import requests
 
def handler(context, inputs):
    #Check input variables
    if "vcenterhost" not in inputs:
        raise ValueError("vCenter host/ip not defined")
    
    if "base64cred" not in inputs:
        raise ValueError("Base64 hash not defined")    
    
    
    host = inputs["vcenterhost"]
    base64hash = inputs["base64cred"]

    #Define variables with values
    requestUrl = "https://{0}/rest/com/vmware/cis/session".format(host)
    auth = "Basic {0}".format(base64hash)
    headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": auth}
 
    #Execute POST request using variables
    response = requests.post(requestUrl, headers = headers, verify = False)
    print('Request response code is: ' + str(response.status_code))
 
    #Extract response body as JSON using inbuilt json() method
    outputs = {}
    if response.status_code == 200:
        jsonResponse = response.json()
        print('VC API token is: ' + jsonResponse.get('value'))
        
        #Create output dictionary with return keys and values
        outputs['apiToken'] = jsonResponse.get('value')
    
    return outputs