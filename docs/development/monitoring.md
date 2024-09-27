## Monitoring

Across our infrasture we host multiple applications and data pipelines all under  constant development. Natural this system requires multiple methods of monitoring to keep track of what's going on.

We're still developping and improving our approach to monitoring so please reach out with any new ideas or improvements!

### Slack notifications

The most useful tool at our disposable is the delivery of key notifications in our slack notifications channel. If you are not part of this reach out to the tech ead to get access. There are several key types of notifications:

* Sentry Alerts - We have integrated sentry into our running applications. When a new issue is raised in sentry a notification is posted in the channel. The infrasture team will monitor and triage these alerts but they may be passed tot he relevant teamm for resolution.
* Deployment Notifications - These are posted by AWS when a new image is created and published by one of our applications to one of our Elastic Container Registries (ECR). It shows the progress as a new container is deployed via blue-green deployment. Make sure to review these when you deploy changes to one of our environments.
* Github Action (GHA) Failures - We still run a lot of processing in github actions across multiple repositories. When one of these fails the details are posted in with a link to the action This only covers data processing actions at the momment. 
* Security Scans - We have security scans set up on our main application. These do both static and dynamic audits of code each  week and the reports are posted. We're hoping to apply these scans to multiple repos in the future.

### Sentry

As mentioned above we have integrated sentry with our appllications. This is primarily to catch unhandled and logged errors in our applications. Accounts can be set up by the tech lead. 

There may be scope to log performance and metrics via sentry in the  future too.

###  Cloudwatch Dashboards

We have several dashboards that can give some metrics based on the  logs in our infrastructure. We can give permissions to these dashboards for those that need it





Pipeline status dashboard: https://digital-land-dashboard.herokuapp.com/
digital-land.info service is also instrumented with [Sentry](https://sentry.io/organizations/dluhc-digital-land/issues/)