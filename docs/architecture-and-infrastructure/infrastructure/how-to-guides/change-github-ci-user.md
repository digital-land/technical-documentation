Permissions are found within the IAM policies attached to the build user assigned to a GitHub repository


# Change permissions for a GitHub CI user

## Background

  * Permissions are ultimately defined in AWS Identity & Access Management (IAM)

  * GitHub CI builds run on GitHub's own infrastructure and must authenticate with AWS for any interactions with AWS resources

  * GitHub actions within the digital-land organisation typically authenticate as an IAM user which is specific to an application and usually has the suffix "-deployer"

  * The IAM user has one or more IAM policies attached

  * By default, the IAM user has policies attached which allow images to be pushed to ECR (i.e. docker container images) as well as updates to Lambda code

  * IAM policies contain allow and deny statements for AWS resources, controlling what can and can't be accessed

## Steps

> [!TIP]
> Determining the exact IAM permissions required can be an iterative process and it's often better to firstly make your changes manually in a non-production environment.  Once you've settled on the correct combination, remembering the principle of least privilege, you can go ahead and convert your change into Terraform code using the steps below.

> [!CAUTION]
> Unlike application permissions, the definition of GitHub CI user permissions within the application module are not parameterised.  When making changes, proceed with caution since the changes will affect multiple GitHub CI pipelines.  A useful piece of refactoring in future would be to parameterise permissions in a similar way to application permissions which uses the additional_permissions parameter.

To change the permissions for a GitHub CI user:

  1. Locate the `deployment_user.tf` file within the `application` module of the infrastructure code repository
  1. Next, find the aws_iam_policy_document which contains permissions for the deployer user
  1. New permissions can be added, while existing entries can be changed or removed.
  1. Run a Terraform plan in the usual way to review that your changes are as expected
  1. Finally, run a Terrraform apply if you are happy to proceed 

