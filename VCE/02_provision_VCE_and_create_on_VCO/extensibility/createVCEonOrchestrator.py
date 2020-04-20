import requests
 
def handler(context, inputs):
    outputs = {}
    #Check input variables

    if "customProperties" not in inputs:
        raise ValueError("customProperties not defined in blueprint")

    if "ovf.prop:velocloud.vce.activation_code" in inputs["customProperties"]:
        _,code = inputs["customProperties"]["ovf.prop:velocloud.vce.activation_code"].split(":")
        if code.upper() != "GENERATE":
            outputs["VCEcreation"] = "Skip"
            return outputs

    if "VCOuser" not in inputs:
        raise ValueError("VCO username is not defined")

    if "VCOpass" not in inputs:
        raise ValueError("VCO password is not defined")

    if "VCOenterid" not in inputs:
        raise ValueError("VCO enterprise ID is not defined")

    if "VCOenterproxyid" not in inputs:
        raise ValueError("VCO enterprise proxy ID is not defined")

    if "VCOconfigurationid" not in inputs:
        raise ValueError("VCO configuration ID is not defined")


    _,host    = inputs["customProperties"]["ovf.prop:velocloud.vce.vco"].split(":")
    username   = inputs["VCOuser"]
    password   = inputs["VCOpass"]
    entid      = inputs["VCOenterid"]
    entproxyid = inputs["VCOenterproxyid"]
    configid   = inputs["VCOconfigurationid"]
    
    #Any name which is unique can be used. ResourceIds should be unique hence using that for now.
    name       = "ACME-{0}".format(inputs["resourceIds"][0])

    #Define variables with values
    requestUrl = "https://{0}/login/enterpriseLogin".format(host)
    headers = { "Content-Type": "application/json" }
    data = { "username": username, "password": password }

    session = requests.Session()

    #Execute POST request using variables to authenticate against VCO - one could use authtoken with 3.4 but some customers have still older version
    response = session.post(requestUrl, json=data, headers = headers, verify = False)
    print('Request response code is: ' + str(response.status_code))

    #Extract response body as JSON using inbuilt json() method
    if response.status_code == 200:
        if "velocloud.message" in session.cookies:
            if "Invalid" in session.cookies["velocloud.message"]:
                raise ValueError(session.cookies["velocloud.message"].replace("%20", " "))
        if "velocloud.session" not in session.cookies:
            raise ValueError("Cookie not received by VCO")

    #Chaning request URL
    requestUrl = "https://{0}/portal/".format(host)

    #Creating the needed payload
    params = {
        "name":"{0}".format(name),
        "customInfo":"",
        "configurationId":"{0}".format(configid),
        "serialNumber":"",
        "site":{
            "id": 0,
            "created":"",
            "name":"",
            "contactName":"automation",
            "contactPhone":"",
            "contactMobile":"",
            "contactEmail":"automation-with-vra8@github-repository.com",
            "streetAddress":"",
            "streetAddress2":"",
            "city":"",
            "state":"",
            "postalCode":"",
            "country":"",
            "lat":0,
            "lon":0,
            "timezone":"",
            "locale":"",
            "shippingSameAsLocation":1,
            "shippingContactName":"",
            "shippingAddress":"",
            "shippingAddress2":"",
            "shippingCity":"",
            "shippingState":"",
            "shippingPostalCode":"",
            "shippingCountry":"",
        },
        "modelNumber":"virtual",
        "enterpriseId":entid,
        "enterpriseProxyId":entproxyid
    }

    data = {
        "jsonrpc": "2.0",
        "id": 666,
        "method": "edge/edgeProvision",
        "params": params
    }

    response = session.post(requestUrl, json=data, headers=headers, verify = False)
    print('Request response code is: ' + str(response.status_code))

    if response.status_code == 200:
        jsonResponse = response.json()
        
        #We extract the information received by the VCO 
        if "result" in jsonResponse:
            code = jsonResponse["result"]["activationKey"]
            outputs["VCEcreation"] = "Done"
            
            #Copying all the information of input[customProperties] into output[customProperties] such that, we can alter the velocloud.vce.activation_code in for the next worfklow.
            outputs["customProperties"] = inputs["customProperties"]
            outputs["customProperties"]["ovf.prop:velocloud.vce.activation_code"] = "ovf.prop:{0}".format(code)
        else:
            #Could be used by other workflow to not execute provisioning if that has been determined
            outputs["VCEcreation"] = "Failed"
            outputs["VCEcreationError"] = jsonResponse["error"]
    else:
        outputs["VCEcreation"] = "Failed"
        outputs["VCEcreationError"] = response.content

    return outputs
