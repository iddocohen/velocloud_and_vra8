# Introduction

Blueprints represent the most important entity within vRealize Automation – they define how to provision and manage the lifecycle of resources in vRealize Automation (aka, infrastrucutre as a code).
In this section, we will go deeper on the different sections of the blueprint and why we configure those for the VCE.

# Useage

By going to "Cloud Assembly"->"Blueprints"->"Upload", you should be able to upload the ``template.yaml`` with the given name and towards project you defined previously. In my case, I called it "vVCE Blueprint" and upload it to project called "Tests".  

<img src="../screenshots/Blueprint_Upload.png" width="1024">  


# Overview of the Blueprint

After uploading and opening the blueprint you will see that vRA has constructed a topology based on the definition of the YAML. 

<img src="../screenshots/Blueprint_Overview.png" width="1024">

The below will describe the template and each section of the YAML..

## Inputs

The input section in the "Blueprint" provides the end-user the option to enter values, so the Blueprint can consume those. When the Blueprint gets shared in "Service Broker" under catalog, the end-user using that Blueprint gets a input form onto which he/she is asked to input the values needed for the Blueprint. 

<img src="../screesnhots/Service_Broker_Input_Form.png">

Those inputs can also be tested in the "Blueprint" itself when by performing a "Test"

<img src="../screesnhots/Blueprint_Testing.png" width="1024">

The "Blueprint" can consume those variables because vRA8 creates an object called `input` and associates the variables defined as attributes within that object. Lets consider what I have done for vVCE deployment example. 

```yml 
...
inputs:
  host:
    type: string
    encrypted: false
    description: VCO IP or Hostname
    default: vco22-fra1.velocloud.net
    title: VCO Host
  code:
    type: string
    encrypted: false
    description: Activation code on VCO
    title: Activation Code
    default: GENERATE
  password:
    type: string
    encrypted: true
    title: Password on vVCE
    description: Password for vVCE to access via ssh
    default: Velocloud123
...
```

`host, `code` and `password` are variables which I defined in this case, so they can be used later in the template via `${input.host}`, `${input.code}`, `${input.password}` respectively. That can be seen best in [Resources section](# Resources). 

## Resources

### Compute
### Network

# Resources to keep in mind:
- [vRA8 Resource Schema](https://code.vmware.com/apis/894/vrealize-automation-resource-type-schema)
- [What are some blueprint code examples](https://docs.vmware.com/en/vRealize-Automation/8.0/Using-and-Managing-Cloud-Assembly/GUID-4717026E-D11A-48FE-93A9-E409A623C723.html)
 
