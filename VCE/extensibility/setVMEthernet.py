import requests
import json
 
def handler(context, inputs):
    #Get variables from event payload
    if "vmIdsInterfaces" not in inputs:
        raise ValueError("vmIdsInterfaces not defined in inputs")
    
    if "vcenterhost" not in inputs:
        raise ValueError("vCenter host/ip not defined")
    
    if "apiToken" not in inputs:
        raise ValueError("No authentication token for payload")
        
    #Setting variables for easier using
    vms  = inputs['vmIdsInterfaces']
    host = inputs["vcenterhost"]
    auth = inputs['apiToken']
     

    #Static header for all requests.
    headers = {"Content-Type": "application/json", "Accept": "application/json", "vmware-api-session-id": auth}
    params = {}
    
    for vm in vms:
        
        #Stopping the VM
        requestUrl = "https://{0}/rest/vcenter/vm/{1}/power/stop".format(host,vm)
        response = requests.post(requestUrl, data={}, params = params, headers = headers, verify = False)

        #If unsuccessful for any reason then continue the loop to the next VM - there should only ever be one VM but in the case if there are many.
        if response.status_code != 200:
            continue
        
        for interface in vms[vm]:
            
            #Delete existing E1000 interface from the VM
            requestUrl = "https://{0}/rest/vcenter/vm/{1}/hardware/ethernet/{2}".format(host,vm, interface)
            response = requests.delete(requestUrl, params = params, headers = headers, verify = False)

            #Continue to the next interface if it cannot be deleted
            if response.status_code != 200:
                continue

            #Creating the needed payload
            payload = {}
            payload["spec"] = vms[vm][interface]
            payload["spec"]["type"] = "VMXNET3"
            
            #Settng mac_type to Manual as we are setting the same MAC again to avoid problems with the image
            payload["spec"]["mac_type"] = "MANUAL"
            
            #Deleting unncessary fields which will cause an error
            
            #Fixing payload for all types
            if "label" in payload["spec"]:
                del payload["spec"]["label"]
                
            #Fixing payload for all types   
            if "state" in payload["spec"]:
                del payload["spec"]["state"]
            
            #Fixing payload inside backing for different types of ports
            if "backing" in payload["spec"]:
                
                #Fixing Payload for standard based ports
                if "network_name" in payload["spec"]["backing"]:
                    del payload["spec"]["backing"]["network_name"]
                    
                #Fixing Payload for NSX based solution 
                if "connection_cookie" in payload["spec"]["backing"]:
                    del payload["spec"]["backing"]["connection_cookie"]
                    
                #Fixing Payload for NSX based solution  
                if "distributed_switch_uuid" in payload["spec"]["backing"]:
                    del payload["spec"]["backing"]["distributed_switch_uuid"]
            
            #Creating new interfaces as VMXNET3 with same information
            requestUrl = "https://{0}/rest/vcenter/vm/{1}/hardware/ethernet/".format(host,vm)
            response = requests.post(requestUrl, json=payload, headers = headers, verify = False)
            print('Request response code is: ' + str(response.status_code))
            print(response.content)
                
        #Starting back the VM
        requestUrl = "https://{0}/rest/vcenter/vm/{1}/power/start".format(host,vm)
        response = requests.post(requestUrl, data={}, params = params, headers = headers, verify = False)

