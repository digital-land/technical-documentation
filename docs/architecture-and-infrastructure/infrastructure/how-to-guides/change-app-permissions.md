---
title: Change permissions for an application
---

## Background

* Permissions are ultimately defined in AWS Identity & Access Management (IAM)

* Applications run as containers on an AWS ECS cluster

* The ECS Task Definition for an application contains a task role parameter which refers to an IAM role 

* An IAM role has one or more IAM policies attached

* IAM policies contain allow and deny statements for AWS resources, controlling what can and can't be accessed

## Steps

> [!TIP]
> Determining the exact IAM permissions required can be an iterative process and it's often better to firstly make your changes manually in a non-production environment.  Once you've settled on the correct combination, remembering the principle of least privilege, you can go ahead and convert your change into Terraform code using the steps below.

To change the permissions for an application:

1. Navigate to the correct system folder within the infrastructure code repository, e.g. the main application is found within the platform system
1. Locate the module for the application in question, e.g. `module "application_main" {...}`
1. One of the module parameters is named `additional_permissions` and should contain a map of permission objects.  Permission objects must define the actions that can be performed on specific resources.
1. New permissions can be added, while existing entries can be changed or removed.
1. Run a Terraform plan in the usual way to review that your changes are as expected
1. Finally, run a Terrraform apply if you are happy to proceed 

