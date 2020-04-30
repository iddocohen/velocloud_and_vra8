# Introduction

Blueprints represent the most important entity within vRealize Automation – they define how to provision and manage the lifecycle of resources in vRealize Automation (aka, infrastrucutre as a code).In this section, we will go deeper on the different sections of the blueprint and why we configure those for the VCE.

In summary the main objectives of this blueprint:
- Create the VCE within vSphere and create 6 interfaces.
  - Those 6 interfaces must be configured towards the right networks (done via constraints).
  - Associate right compute resources on VCO.
- Create an input form for variables we need for provisioning the VCE itself and the automation of register the VCE onto the VCO. 

# Useage

By going to "Cloud Assembly"->"Blueprints"->"Upload", you should be able to upload the ``template.yaml`` with the given name and towards project you defined previously. In my case, I called it "vVCE Blueprint" and upload it to project called "Tests".  

<img src="../screenshots/Blueprint_upload.png" width="1024">  


# Overview of the Blueprint

After uploading and opening the blueprint you will see that vRA has constructed a topology based on the definition of the YAML. 

<img src="../screenshots/Blueprint_Overview.png" width="1024">

The below will describe the template and each section of the YAML.

## Inputs Section in YAML

The input section in the "Blueprint" provides the end-user the option to enter values, so the Blueprint can consume those. When the Blueprint gets shared in "Service Broker" under catalog, the end-user using that Blueprint gets a input form onto which he/she is asked to input the values needed for the Blueprint. 

<img src="../screenshots/Service_Broker_Input_Form.png" width="1024">

Those inputs can also be tested in the "Blueprint" itself when by performing a "Test"

<img src="../screenshots/Blueprint_Testing.png" width="1024">

The "Blueprint" can consume those variables because vRA8 creates an object called `input` and associates the variables defined as attributes within that object. Lets consider what I have done, as an example how it works.

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

`host`, `code` and `password` are variables which I defined in this case, so they can be used later in the template via `${input.host}`, `${input.code}`, `${input.password}` respectively. Those variables have properties associated to them: 
- `type` to provide vRA8 the context of the variable, such that, the end-user input form can be created accordingly. Other types are number, integer, Boolean, or object 
- `default` to provide a prepopulated value for that variable.
- `description` to provide a help text to the end-user on the input form.
- `title` to provide a friendly name on the  end-user input form for that variable (provides better user expierence).

In this case, those variables are used to pass towards the VCE to activate against a VCO and create a default root password. In addition, the variable `code` will also be used in "Extensibility", to check if an activation code needs to be generated (if the value is "GENERATE") or use the provided activation code for the VCE. Under the section [Extensibility](../extensibility/) the notation on "how we check this variable" but for now please refer to [Resources](#Resources-Section-in-YAML) to understand "how we use those variables in the Blueprint". 

For more information on how inputs can be customised please refer to [How user input can customize a vRealize Automation Cloud Assembly blueprint
](https://docs.vmware.com/en/vRealize-Automation/8.0/Using-and-Managing-Cloud-Assembly/GUID-6BA1DA96-5C20-44BF-9C81-F8132B9B4872.html)

## Resources Section in YAML

### Compute
### Network

# Resources to keep in mind:
- [vRA8 Resource Schema](https://code.vmware.com/apis/894/vrealize-automation-resource-type-schema)
- [What are some blueprint code examples](https://docs.vmware.com/en/vRealize-Automation/8.0/Using-and-Managing-Cloud-Assembly/GUID-4717026E-D11A-48FE-93A9-E409A623C723.html)
 
