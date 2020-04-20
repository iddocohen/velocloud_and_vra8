import requests
import json
 
def handler(context, inputs):
    #Get variables from event payload
    outputs = {}
    names = ""
    if "vmIds" not in inputs:
        raise ValueError("vmIds not provided as input")
    
    if "vcenterhost" not in inputs:
        raise ValueError("vCenter host/ip not defined")
    
    if "apiToken" not in inputs:
        raise ValueError("No authentication token for payload")
    
    ids = inputs["vmIds"]
    host = inputs["vcenterhost"]
    auth = inputs['apiToken']
     
    #Set action variables
    vmIdsInterfaces = {}
    for vm in ids:
        requestUrl = "https://{0}/rest/vcenter/vm/{1}/hardware/ethernet".format(host,vm)
        params = {} 
        
        #Execute GET request using variables
        headers = {"Content-Type": "application/json", "Accept": "application/json", "vmware-api-session-id": auth}
        response = requests.get(requestUrl, params = params, headers = headers, verify = False)
        print('Request response code is: ' + str(response.status_code))
     
        #Extract response body as JSON using inbuilt json() method
        jsonResponse = response.json().get('value')
        print(jsonResponse)
        
        #Get all interfaces of the VM
        tmpInterfaces = []
        if response.status_code == 200 and len(jsonResponse) > 0:
            for interfaces in jsonResponse:
                print("VM interface nic: " + interfaces['nic'])
                tmpInterfaces.append(interfaces['nic'])
        else:
            raise ValueError("Response code was not 200 or no matching results found for interfaces")
            
        #Execute GET request for each interfaces gathered
        relevantVmInterfaces = {}
        for interface in tmpInterfaces:
            #Get information for given interface of that given VM
            requestUrl = "https://{0}/rest/vcenter/vm/{1}/hardware/ethernet/{2}".format(host ,vm, interface)
            response = requests.get(requestUrl, params = params, headers = headers, verify = False)
            print('Request response code is: ' + str(response.status_code))
            
            #Extract response body as JSON using inbuilt json() method
            jsonResponse = response.json().get('value')
            print(jsonResponse)
            
            #Finding interfaces which are not vmxnet3 for a VM
            if jsonResponse['type'] != "VMXNET3":
                relevantVmInterfaces[interface] = jsonResponse
        
        #Associate the relevant interfaces to the right VM
        if relevantVmInterfaces:
            vmIdsInterfaces[vm] = relevantVmInterfaces   
    
    print(vmIdsInterfaces)
            
    outputs['vmIdsInterfaces'] = vmIdsInterfaces
    return outputs