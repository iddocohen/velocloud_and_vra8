# Introduction

Blueprints represent the most important entity within vRealize Automation – they define how to provision and manage the lifecycle of resources in vRealize Automation (aka, infrastrucutre as a code).In this section, we will go deeper on the different sections of the blueprint and why we configure those for the VCE.

In summary the main objectives of this blueprint:
- Create the VCE within vSphere and create 6 interfaces.
  - Those 6 interfaces must be configured towards the right networks (done via constraints).
  - Associate right compute resources on VCO.
- Create an input form for variables we need for provisioning the VCE itself and the automation of register the VCE onto the VCO. 

# Useage

By going to "Cloud Assembly"->"Blueprints"->"Upload", you should be able to upload the ``template.yaml`` with the given name and towards project you defined previously. In my case, I called it "vVCE Blueprint" and upload it to project called "Tests".  
<p align="center"><img src="../screenshots/Blueprint_upload.png" width="1024"></p>

# Overview of the Blueprint

After uploading and opening the blueprint you will see that vRA has constructed a topology based on the definition of the YAML. 

<p align="center"><img src="../screenshots/Blueprint_Overview.png" width="1024"></p>

The below will describe the template and each section of the YAML.

## Inputs Section in YAML

The input section in the "Blueprint" provides the end-user the option to enter values, so the Blueprint can consume those. When the Blueprint gets shared in "Service Broker" under catalog, the end-user using that Blueprint gets a input form onto which he/she is asked to input the values needed for the Blueprint. 

<p align="center"><img src="../screenshots/Service_Broker_Input_Form.png" height="640"></p>

Those inputs can also be tested in the "Blueprint" itself when by performing a "Test"

<p align="center"><img src="../screenshots/Blueprint_Testing.png" width="1024"></p>

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

In this case, those variables have been created to pass towards the VCE to successfully activate against a VCO and to provison the VCE with a default password. In addition, the variable `code` will also be used in "Extensibility" to check if the activation code needs to be generated (aka, VCE was not created first on the VCO) or use the provided activation code for the VCE. With this ability full automation can be archived, that is, a VCE can be created on compute host and created on VCO at the same time.   

Under the section [Extensibility](../extensibility/) the notation on "how we check the activation code" and "how we get activation code from VCO after creating the VCE in VCO" will be elaborated but for now please refer to [Resources](#Resources-Section-in-YAML) to understand "how we use these variables in the Blueprint and pass those to the VCE itself". 

For more information on how inputs can be customised please refer to [How user input can customize a vRealize Automation Cloud Assembly blueprint
](https://docs.vmware.com/en/vRealize-Automation/8.0/Using-and-Managing-Cloud-Assembly/GUID-6BA1DA96-5C20-44BF-9C81-F8132B9B4872.html)

## Resources Section in YAML

The resource section gives one the possiblity to define the compute resources, the networks they should use and the connections between resources and the defined networks. In this template, I defined a compute resource called `vVCE` which is a `type: Cloud.vSphere.Machine` onto which I will connect 6 interfaces to, use the OVA image and send via ovfProperties some values such that the [cloud-init within the VCE](https://github.com/iddocohen/vce_cloudinit/) can use it.  

For a more meaningful topology, one could extend this template to add several compute resources and attach those via networking to the `vVCE` - that is not shown here but please ping me if you feel this is needed. 

In this section I will elaborate the properties within the section resources. In particular, I will focus on ovfProperties and networks.

### Propeties section within resources

After defining our resource name (`vVCE`) and tell vRA8 what type it is (`Cloud.vSphere.Machine`), we dive straight into properties the VM should be provisioned with or associated with.

```yml
    ...
    properties:
      cpuCount: 2
      totalMemoryMB: 4096
      imageRef: 'http://192.168.2.175/edge-VC_VMDK-x86_64-3.4.0-106-R340-20200218-GA-c57f8316dd-updatable-ext4.ova'
      ovfProperties:
        - key: password
          value: '${input.password}'
        - key: velocloud.vce.activation_code
          value: '${input.code}'
        - key: velocloud.vce.dns1
          value: 8.8.8.8
        - key: velocloud.vce.dns2
          value: 8.8.4.4
        - key: velocloud.vce.vco
          value: '${input.host}'
      networks:
        - name: '${resource.Cloud_Network_1.name}'
          network: '${resource.Cloud_Network_1.id}'
          deviceIndex: 0
        - name: '${resource.Cloud_Network_2.name}'
          network: '${resource.Cloud_Network_2.id}'
          deviceIndex: 1
        - name: '${resource.Cloud_Network_3.name}'
          network: '${resource.Cloud_Network_3.id}'
          deviceIndex: 2
        - name: '${resource.Cloud_Network_4.name}'
          network: '${resource.Cloud_Network_4.id}'
          deviceIndex: 3
        - name: '${resource.Cloud_Network_5.name}'
          network: '${resource.Cloud_Network_5.id}'
          deviceIndex: 4
        - name: '${resource.Cloud_Network_6.name}'
          network: '${resource.Cloud_Network_6.id}'
          deviceIndex: 5
   ...
```

#### cpuCount and totalMemoryMB

Lets discuss the first two obvious properties:
- `cpuCount` which defines how many CPUs the VM should have.
- `totalMemoryMB` which defines the total RAM in MB the VM should have.

In this template those values are statically defined with 2 and 4096 respectively; nevertheless, and as shown previously, we could expose those towards the end-user via `${input.variablename}` methodology, for example:

```yml
    ...
    inputs:
      cpu:
        default: 2
        type: integer
        title: CPU
        description: Number of CPU for VM
      ram:
        default: 4096
        type: integer
        title: RAM
        description: How much RAM the VM needs in MB 
    resources:
      vVCE:
        type: Cloud.vSphere.Machine
        properties:
          cpuCount: '${input.cpu}'
          totalMemoryMB: '${input.ram}'
    ...
```

to make it more dynmaic and flexible to use.

#### ImageRef

`imageRef` property is used to tell vRA8 from where to get the OVA image from. In my case, I used a HTTP server location but it could be changed to a local image within vRA8 itself (no HTTP or FTP is needed).


#### ovfProperties

Without going into detail about [Open Virtual Machine Format Specification](https://www.vmware.com/pdf/ovf_spec_draft.pdf) and [how we use OVF within cloud-init on our VCE](https://github.com/iddocohen/vce_cloudinit), it is important to note that the following OVF environment support can be found [here](https://github.com/iddocohen/vce_cloudinit/blob/master/04_config_with_ovf_properties_via_cloudinit_and_user_data/ovf-env.xml) and be used in `ovfProperties` as key value pairs in the "Blueprint", to automate configuration within the VCE itself.

Looking under the hood, lets look into the snipped related to `ovfProperties`:

```yml
    ...
      ovfProperties:
        - key: password
          value: '${input.password}'
        - key: velocloud.vce.activation_code
          value: '${input.code}'
        - key: velocloud.vce.dns1
          value: 8.8.8.8
        - key: velocloud.vce.dns2
          value: 8.8.4.4
        - key: velocloud.vce.vco
          value: '${input.host}'
    ... 
```

we can see that the same keys used are within the XML of the [OVF environment file](https://github.com/iddocohen/vce_cloudinit/blob/master/04_config_with_ovf_properties_via_cloudinit_and_user_data/ovf-env.xml) that the VCE support as `oe:key` and `oe:value`. Assuming that `${input.code}`, `${input.host}` and `${input.password}` are left with default values, hence hold `GENERATE`, `vco22-fra1.velocloud.net` and `Velocloud123`, then the OVF environment file would look something like the following:   

```xml
...
    <Property oe:key="password" oe:value="Velocloud123"/>
    <Property oe:key="velocloud.vce.activation_code" oe:value="GENERATE"/>
    <Property oe:key="velocloud.vce.dns1" oe:value="8.8.8.8"/>
    <Property oe:key="velocloud.vce.dns2" oe:value="8.8.4.4"/>
    <Property oe:key="velocloud.vce.vco" oe:value="vco22-fra1.velocloud.net"/>
...
```

the key outcome to understand, any `oe:key` and `oe:value` supported via OVF environment properties can be used to send towards the VCE, such that it can configure itself internally with those values. Please use the links above to get more inside on how OVF and cloud-init are related on the VCE.

#### networks

The "networks" section with "resources properties", defines which networks should be attached to what NIC of the VM. 

Lets look what has been defined:

```yml
...
      networks:
        - name: '${resource.Cloud_Network_1.name}'
          network: '${resource.Cloud_Network_1.id}'
          deviceIndex: 0
        - name: '${resource.Cloud_Network_2.name}'
          network: '${resource.Cloud_Network_2.id}'
          deviceIndex: 1
        - name: '${resource.Cloud_Network_3.name}'
          network: '${resource.Cloud_Network_3.id}'
          deviceIndex: 2
        - name: '${resource.Cloud_Network_4.name}'
          network: '${resource.Cloud_Network_4.id}'
          deviceIndex: 3
        - name: '${resource.Cloud_Network_5.name}'
          network: '${resource.Cloud_Network_5.id}'
          deviceIndex: 4
        - name: '${resource.Cloud_Network_6.name}'
          network: '${resource.Cloud_Network_6.id}'
          deviceIndex: 5
...
```

`deviceIndex` tells vRA8 to associate the network defined under `network` with the NIC at that given "position". That means, and lets take `deviceIndex: 0` as an example, that the interface GE1 (or eth0 in the Linux OS of the VCE) and the first interface on the VCE, will be associated with the `network` defined with the value that attribute `${resource.Cloud_Network_1.id}` holds. The object (`${resource.Cloud_Network_1}`) and its attribute `id` gets generated as soon as we define the [network resource "Cloud_Network_1"](#Network-section-within-resources).

That means a user can go ahead and pick and choose, the network resources he defined to associate those to given NIC respectively. Same network could be associated to the different NICs or subset of network resources could be associated to different NICs. A valid configuration could be:

```yml
...
      networks:
        - name: '${resource.Cloud_Network_2.name}'
          network: '${resource.Cloud_Network_2.id}'
          deviceIndex: 1
        - name: '${resource.Cloud_Network_5.name}'
          network: '${resource.Cloud_Network_5.id}'
          deviceIndex: 4
        - name: '${resource.Cloud_Network_5.name}'
          network: '${resource.Cloud_Network_5.id}'
          deviceIndex: 5
...
```

Where we would only configure GE2, GE5 and GE6 interfaces of the VCE on the ESXi host and associate `${resource.Cloud_Network_2.id}`. `${resource.Cloud_Network_5.id}` and `${resource.Cloud_Network_5.id}` networks respectively which  GE5 and GE6 would thereby use the same network. 

In our case and in the template, we associate each NIC of the VCE to its own network resource. 


*Important:* It is highly recommended to put `deviceIndex` in the above configuration. If one does not define the `deviceIndex`, then vRA8 will associated the networks defined with random NIC on the compute resource which is not deterministic behavior. 


### Network section within resources

# Resources to keep in mind:
- [vRA8 Resource Schema](https://code.vmware.com/apis/894/vrealize-automation-resource-type-schema)
- [What are some blueprint code examples](https://docs.vmware.com/en/vRealize-Automation/8.0/Using-and-Managing-Cloud-Assembly/GUID-4717026E-D11A-48FE-93A9-E409A623C723.html)
 
