---
title: Using Preview Links with Heroku for Quality Control Testing
---

## Overview
In our development workflow, we leverage Heroku preview links to facilitate quality control (QC) testing during the code review process. These preview environments allow reviewers and testers to validate changes before they are merged into the main branch and deployed to production.

## Purpose
Heroku preview links provide a dedicated, isolated environment for testing new features, bug fixes, and UI/UX changes without affecting the production or staging environments. They enable:
- Early detection of defects and regressions
- Faster feedback cycles during code reviews
- Validation of functionality in an environment similar to production
- Stakeholder previews for design and feature acceptance

## Workflow
1. **Feature Development**
   - Developers create a new feature branch and implement changes.
   - Code is pushed to a GitHub repository.

2. **Pull Request Creation**
   - A pull request (PR) is opened against the `main` or `develop` branch.
   - CI/CD pipelines are triggered to run automated tests.

3. **Heroku Preview Link Generation**
   - Heroku automatically creates a temporary preview app using the branch under review.
   - A unique Heroku preview URL is generated and added as a comment to the pull request.

4. **Quality Control Testing**
   - Reviewers access the Heroku preview link and conduct testing, including:
     - Functional validation
     - UI/UX checks
     - Accessibility audits
     - Performance testing
   - Test results and feedback are provided in PR comments.

5. **Code Review and Fixes**
   - Developers address any issues identified during testing.
   - The Heroku preview environment is automatically updated with new commits.

6. **Approval and Merge**
   - Once the PR is approved and passes QC checks, it is merged into the target branch.
   - The Heroku preview app is automatically deleted.

## Setting Up Heroku Preview Links
To set up Heroku preview links for a repository, follow these steps:

1. **Navigate to the Heroku Dashboard**
   - Go to the [Heroku Dashboard](https://dashboard.heroku.com/).

3. **Create a Heroku Pipeline**
   - Click "New" -> "Create new pipeline" and provide a name.
   - Connect the pipeline to the appropriate GitHub repository.

4. **Create a Placeholder Staging App**
   - In the pipeline, create a new Heroku app for the `staging` environment.
   - Deploy a basic placeholder version of the application to ensure the pipeline is functional.
   - WARNING: Without a placeholder staging app, if no preview links exist, the pipeline will disappear. Please see the following [support documentation](https://help.heroku.com/R8AE3YBV/why-did-my-pipeline-disappear).

5. **Enable Review Apps**
   - Under the pipeline settings, enable "Review Apps" to automatically generate preview environments for each pull request.
   - Select the option to destroy review apps automatically after PR closure.

6. **Configure Environment Variables**
   - Go to review app settings and set up any environment variables you need.
   - Ensure secrets and configurations are securely stored.

7. **Deploy and Verify**
   - Push code changes and verify that Heroku generates preview links correctly.
   - Open the provided preview link to confirm the application is running as expected.

## Best Practices
- **Ensure feature parity**: Preview apps should mimic the production environment as closely as possible.
- **Automate testing**: Integrate automated tests within the CI/CD pipeline to catch issues early.
- **Use environment variables**: Store secrets and configurations securely instead of hardcoding them.
- **Conduct cross-browser testing**: Validate UI consistency across different browsers and devices.
- **Keep preview environments temporary**: Ensure that Heroku review apps are removed after PR closure to optimize resource usage.

## Troubleshooting
- **Preview link not generated?** Check Heroku's GitHub integration settings and ensure the app is correctly configured.
- **Performance issues in preview app?** Review logs for errors and consider adjusting resource allocation.
- **Unexpected behavior in the preview app?** Verify that the correct environment variables and dependencies are set up.

## Conclusion
Heroku preview links streamline our quality control process by providing an efficient and reproducible testing environment. By integrating these links into our workflow, we enhance code review effectiveness, improve collaboration, and ensure higher-quality deployments.

