---
title: Deploy And Release Procedure
---

When working across our repositories you will at some stage need to deploy or release code changes. While the exact process varies across repositories, this page contains generalised guidance that can be applied in different contexts — whether you are shipping a web application, a data pipeline, a package, or a configuration change. We use continuous deployment to minimise the manual work needed by developers. For a deeper understanding of how our CI/CD pipelines are structured and what they must do, see the [CI/CD strategy](../architecture-and-infrastructure/ci-cd-strategy.md).

## Step 1: Create a PR and ensure tests are passing

No code should be pushed directly into the main branch. Always create a new branch to hold your changes and raise a pull request (PR) from it.

A PR is how code changes are shared and reviewed across the team. Our CI/CD pipelines should automatically trigger tests against your branch — ensure all of these are passing before you progress. Failing tests likely indicate something is broken in your code. See the [CI/CD strategy — Test](../architecture-and-infrastructure/ci-cd-strategy.md#test) for what the test workflow must cover.

For guidance on how to raise a PR and request a review effectively, see the [Pull Request best practices](best-practice/pull-requests.md).

**For applications:** our CI/CD pipelines in GitHub build and publish a new Docker image on each push to a branch. Ensure the image builds successfully as part of this step.

## Step 2: Test your changes in an appropriate environment

Before merging, it is worth validating that your changes work correctly outside of your local machine. What this looks like depends on the type of change:

- **Applications:** deploy to the development environment in AWS to confirm the change works in a live cloud environment. This is an opportunity for manual testing or user testing if you are on a product-focused team. It also verifies that configuration changes deploy correctly. When deploying to development, monitor the deployment notifications raised in the relevant Slack channel. Note that there is only one dev environment — check with your team before using it for prolonged periods or if another deployment is already in progress.
- **Data pipelines:** run the pipeline locally or against a test dataset to confirm the output is correct.
- **Packages or libraries:** verify the package can be installed and used correctly by a consuming project.

This step may not be necessary for smaller or lower-risk changes, but it is always worth considering before proceeding.

To do this for applications there should be one of the following GitHub actions:

-  Publish - pushes a container image to an ECR repository in the relevant environment (normally in AWS). There will then be an automatic deployment process which updates it's messages into the notifications slack channel. you can select the branch and environment you want to deploy to.
- Publish & Deploy - does both the publishing into ECR and triggers the deployment. We haven't rolled this out across most repositories yet.



## Step 3: Get a PR review and merge into the `main` branch

Before your code can be deployed to any shared environment, it must be reviewed by another developer. See the [Pull Request best practices](best-practice/pull-requests.md) for guidance on organising reviews and what both the author and reviewer are responsible for — including the important point that **merging is the responsibility of the PR author, not the reviewer**.

The review process may result in further changes being requested. Ensure all tests are still passing after any updates — tests are automatically re-triggered on each push, but it is good practice to run them locally before pushing. If a reviewer is a designer then they may want to see the app deployed to an environment, see step 2 for this.

Once the PR is approved and tests are green, merge into `main`.

**Note:** failing tests should block merges into `main`. If this is not the case for your repository, reach out to the infrastructure team to improve the CI/CD pipeline.

## Step 4: Monitor the deployment or release

After merging, the next steps depend on the type of change:

- **Applications:** merging into `main` triggers the CI/CD pipeline, which publishes new images and deploys them to staging (and development) automatically using a blue-green deployment via AWS CodeDeploy. Monitor the deployment notifications in the relevant Slack channel to confirm the staging deployment completes without being rolled back. Once deployed, do a brief round of manual testing in staging before the change is promoted to production by an admin. See the [CI/CD strategy — For Applications](../architecture-and-infrastructure/ci-cd-strategy.md#for-applications) for more detail on how this works.
- **Data pipelines:** verify the next scheduled run completes successfully and produces the expected output. Check any alerting or monitoring dashboards relevant to the pipeline.
- **Packages:** confirm the published version is available and that any consuming projects can install and use it correctly.

If anything goes wrong at any stage, or if you have questions, reach out to the infrastructure team for help.
