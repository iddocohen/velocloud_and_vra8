# Introduction

In a later time, I will give more detail on the extensible and walk-through on it. For now please take those as is.

Please note, the interface workflow is most likely not needed anymore from vRA 8.2 and onwards - I haven't checked it yet but keep that in mind.

# Usage

1) Download the "files" folder
2) Edit the "Flow-vVCEcreationOnVCO.abx" by providing necessary values.

```yml
...
inputs:
  VCOuser: ""               # Username which is allowed to authenticate and make changes, e.g. VCOuser: "APIuser"
  VCOpass: ""               # Associate password to that user, e.g. VCOpass: "Velocloud123"
  VCOenterproxyid: 23       # Define the MSP ID where the enteprise customer resides in. 
  VCOenterid: 507           # Define the Enterprise ID 
  VCOconfigurationid: 7737  # Define the Profile ID
...
    
```

The easiest way to get necessary IDs above is to create a test edge when logged in  VCO and see the payload the browser is using for  method "edge/edgeProvision" e.g.:

```json
{
    "jsonrpc": "2.0"
    "method": "edge/edgeProvision"
    "params": {
        "name": "test"
        "customInfo": ""
        "configurationId": "7737"                # Profile ID aka VCOconfigurationid as above
        ...
        "enterpriseId": 507                      # Enterprise ID aka VCOenterid as above 
        "enterpriseProxyId": 23                  # MSP ID aka VCOenterproxyid as above
    }
    "id": 35
}
```

There is also the option to call several RestAPI calls to discover the same but the above is the simplest.

3) Edit the "Flow-vVCEInterfaces.abx" by providing necessary values. 

```yml
...
inputs:
  base64cred: ""    # vCenter uses <username>@<domain>:<password> encoded as base64 for API calls, 
                    # e.g. for administrator@vsphere.local:Password123, the encoded string would look `YWRtaW5pc3RyYXRvckB2c3BoZXJlLmxvY2FsOlBhc3N3b3JkMTIz`. 
                    # Easiest is to use https://www.base64encode.org/ and https://www.base64decode.org/ encode and decode base64 strings.
  vcenterhost: ""   # The vCenter IP/FQDN address used. In our case 192.168.2.52.
...
```



