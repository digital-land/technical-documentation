---
title: Deploy And Release Procedure
---

When working across our applications, processes and packages you will at some stage need to deploy code across our development, staging and production environment. While this process may change across different repositories this page contains some generalised guidance that can be applied in different areas. We use Continuous deployment to minimise the work needed by developers.

## Deploying an application

Across our service there are currently three main applications (if something is named wrong please update!):

* Planning data Platform - the main website you'll find at [planning.data.gov.uk]
* Providers Service - a set of tools to help data providers provide urls for us to collect data from. can be found at [check.planning.data.gov.uk]
* Async Processor API - Not visible on the internet this app connects to a message que and worker processors to complete tasks asynchronously as needed

For each of these we aim to keep a consistent approach to deploying code changes across our environments and finally into production. This process is as follows. Before following the below process changes should be made and tested locally.

### Step 1: Create a PR, Ensure Tests are passing

No code should be pushed directly into the main branch. This can lead to errors being created in our environment and having to revert to previous commits on the main branch. By pushing to a new branch it can reduce the chance of this happening. So always create a new branch to hold your code.

Creating a PR for you code is essential it's how code changes can be shared between developers and allows them to review your code! Our CI/CD pipelines should automatically trigger unit, integration and acceptance tests against your code changes. Ensure that all of these are passing before you progress to the next step. If they are failing then it is likely that something is broken in your code.

### Step 2: Deploy to the development environment 

For Each application there should be the ability to deploy to the development environment that with have in AWS. Please reach out to the ifnrastructure team if this is not clear or not possible. We are working on unifying this across repositories.

This allows you to check the changes you have made are working correctly in a working cloud environment (an oppertunity for manual testing or possible user testing if you are on a product focussed team!)

It also ensure that your changes can be deployed correctly to an environment. This may not affect the majority of code changes but especially when configuration is changed this allows you to check. our CI/CD pipelines in github work by publishing a new docker image to our image repository, AWS then deploys this image into our infrastructure. When deploying to development you should monitor the deployment notification that are raised in the #planning-data-platform slack channel.

**Note** - this step may not be needed for smaller changes but it always worth considering. There is also only one dev environment so it may be worth talking to your team incase someone is using it or if you exoect to be using it for a prolonged amount of time.

### Step 3: Get a PR review and merge into the `main` branch

Before you can deploy your code into any other environments you will need to get a review from another developer, your teams should have a process in place for who can review the PR but the infrastructure team is happy to help if you want a more central review of your code. IT is important all tests are passing before you start this step

The review process may alter your code as it is discussed between the developers, ensure that the tests are still passing before any merges happen, each repo should run tests for every push that is made to a branch so they will be automatically re-triggered we still advise that tests are ran locally before pushes are made.

Once the PR has been approved the code is ready to be merged into main! 

**Note** - Failing tests should stop merges into main. If this is not the case please reach out to the infra team to improve the CI/CD pipeline!

### Step 4: Monitor staging deployment and get an admin to deploy to prod

When you merge into main the continuous integration pipeline will be triggered and it will automatically publish images to both the. development and staging ECR repositories. Once these actions are complete AWS CodeDeploy will take these images and use a blue-green deployment to replace the old containers with the new ones.

The status of these deployments will be sent to our notifications slack channel. You should monitor the staging message to ensure that the deployment went through correctly and isn't rolled back. Once it's in the environment you should do some brief manual tests.

If anything goes wrong at this stage (or indeed if you have any questions  at any stage) reach out to the infrastructure team for help.


