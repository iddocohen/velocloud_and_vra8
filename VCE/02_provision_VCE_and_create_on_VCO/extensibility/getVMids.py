import requests
import json
 
def handler(context, inputs):
    #Get variables from event payload
    outputs = {}
    names = ""
    if "resourceNames" in inputs:
        names = inputs["resourceNames"]
        print("Number of resource names from event payload: " + str(len(names)))
        print(names)
        
    if "vcenterhost" not in inputs:
        raise ValueError("vCenter host/ip not defined")
    
    if "apiToken" not in inputs:
        raise ValueError("No authentication token for payload")
        
    host = inputs["vcenterhost"]
    auth = inputs['apiToken']
     
    #Set action variables
    requestUrl = "https://{0}/rest/vcenter/vm".format(host)
    params = {"filter.names": names} if names else {} 
        
    #Execute GET request using variables
    headers = {"Content-Type": "application/json", "Accept": "application/json", "vmware-api-session-id": auth}
    response = requests.get(requestUrl, params = params, headers = headers, verify = False)
    print('Request response code is: ' + str(response.status_code))
     
    #Extract response body as JSON using inbuilt json() method
    jsonResponse = response.json().get('value')
    print(jsonResponse)
     
    #Check response and if OK iterate through storing VM Identifiers into an array
    vmIds = {}
    if response.status_code == 200 and len(jsonResponse) > 0:
        for vm in jsonResponse:
            print("VM ID is: " + vm['vm'])
            vmIds[vm['vm']] = vm['name']
    else:
        print(jsonResponse)
        raise ValueError("Response code was not 200 or no matching results found")
     
    #Create output dictionary with return keys and values
    outputs['vmIds'] = vmIds
    return outputs