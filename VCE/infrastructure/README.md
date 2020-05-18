# Introduction

This section will be covering screenshots around my infrastructure environment in "Cloud Assembly". 

## Project


### Summary view

<p align="center"><img src="../screenshots/Infrastructure_Project_Overview.png" width="1024"></p>

Associated to this project one can see the 7 "Actions" associated to it, the 1 "Blueprint" and the 1 "Cloud Zone". If copying the exact project configuration, you should have those numbers as a sanity check. 

### Users

<p align="center"><img src="../screenshots/Infrastructure_Project_Users.png" width="1024"></p>

No special configuration done other then switching on "Deployments are shared between all users in the project". This lets different users to use all deployments and such useful. 

### 
<p align="center"><img src="../screenshots/Infrastructure_Project_Provisioning.png" width="1024"></p>

Under "Cloud Zones" I added my "lab / Datacenter" environment, so vRA8 knows which environment to use for provisioning. No "Constraints" have been defined here.

One could consider to set "Request Timeout" to ensure that "Actions" will fail after given time..
