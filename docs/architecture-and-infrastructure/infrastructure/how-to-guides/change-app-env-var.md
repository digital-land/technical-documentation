# Change an application environment variable

## Background

 * Applications run as containers on an AWS ECS cluster

 * Environment variables are detailed within the ECS Task Definition for an application
 
 * Task Definitions are provisioned via the application module of the infrastructure code repository

 * The application module receives environment variables as a parameter of type: map 

## Steps

To change an application's environment variables:

  1. Navigate to the correct system folder within the infrastructure code repository, e.g. the main application is found within the platform system
  1. Locate the module for the application in question, e.g. `module "application_main" {...}`
  1. One of the module parameters is named `environment` and should contain a map of environment keys to values.
  1. To add a new variable, simply append a new key value pair to the map.  
  1. You can also change existing values in the map
  1. It's also possible to remove a key value pair which is no longer needed.  Consider what impact this might have on the application.
  1. Run a Terraform plan in the usual way to review that your changes are as expected
  1. Finally, run a Terrraform apply if you are happy to proceed

 > [!TIP]
 > Always try to make changes in a backwards (and forwards) compatible manner