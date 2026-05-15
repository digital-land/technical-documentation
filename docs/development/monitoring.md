---
title: Monitoring
---

Across our infrastructure we host multiple applications and data pipelines all under  constant development. Natural this system requires multiple methods of monitoring to keep track of what's going on.

We're still developing and improving our approach to monitoring so please reach out with any new ideas or improvements!

### Slack notifications

The most useful tool at our disposable is the delivery of key notifications in our Slack notifications channel. If you are not part of this reach out to the tech ead to get access. There are several key types of notifications:

* Sentry Alerts - We have integrated sentry into our running applications. When a new issue is raised in sentry a notification is posted in the channel. The infrastructure team will monitor these alerts, triage any issues and possibly pass those onto the relevant team for resolution.
* Deployment Notifications - These are posted by AWS when a new image is created and published by one of our applications to one of our Elastic Container Registries (ECR). It shows the progress as a new container is deployed via blue-green deployment. Make sure to review these when you deploy changes to one of our environments.
* GitHub Action (GHA) Failures - We still run a lot of processing in GitHub actions across multiple repositories. When one of these fails the details are posted in with a link to the action This only covers data processing actions at the moment. 
* Security Scans - We have security scans set up on our main application. These do both static and dynamic audits of code each  week and the reports are posted. We're hoping to apply these scans to multiple repos in the future.

### Sentry

We use Sentry across our applications to capture errors and track metrics. Accounts can be set up by the tech lead.

#### Logging configuration

The standard Sentry logging configuration is:

```python
sentry_logging = LoggingIntegration(
    sentry_logs_level=logging.WARNING,
    level=logging.INFO,       # Capture INFO logs as breadcrumbs only
    event_level=logging.ERROR, # Only send ERROR and above to Sentry as issues
)
```

What this means in practice:

- **INFO** logs are captured as breadcrumbs — they appear as context on an issue but do not create one themselves
- **WARNING** and above are captured by Sentry's log stream
- **ERROR** and **CRITICAL** create Sentry issues and trigger alerts
- Handled exceptions and lower-severity log lines are not surfaced as issues

#### Metrics

We are implementing Sentry metrics to monitor frequent but handled error conditions — things that don't throw an unhandled exception but are worth tracking, for example:

- Datasette query failures
- Slow database queries
- Other semi-error states that are caught and handled

For each of these we define a metric and set an alert threshold. When the threshold is breached, an alert is sent to the **planning-data-alerts** Slack channel. Currently threshold breach alerts go to **planning-data-notifications**, with the intention to move them to **planning-data-alerts** as the setup matures.

#### Triage process

All unresolved Sentry issues appear in the **planning-data-notifications** Slack channel.

Every two weeks the team holds a Sentry triage meeting to review unresolved production issues across each monitored service. For each issue the outcome is one of:

1. **Ticket to fix** — a known bug, create a ticket and assign it
2. **Ticket to investigate** — cause is unclear, create a ticket to dig into it
3. **Archive** — noise or expected behaviour, archive the issue in Sentry
4. **Improve the alert** — the alert lacks context; set up a better metric monitor with more detail before the next review

The meeting works through each service we monitor in turn, ensuring nothing is left unresolved or unactioned. Any ticket created in the meeting should have an owner assigned before the meeting ends.

#### Alert fatigue

If an alert is firing repeatedly and being routinely archived or ignored, it should either be turned off or converted into a metric with a threshold. An alert that no one acts on is worse than no alert — it trains the team to ignore the channel. If you notice this pattern outside of the triage meeting, raise it rather than continuing to archive.

###  Cloudwatch Dashboards

We have several dashboards that can give some metrics based on the logs in our infrastructure. We can give permissions to these dashboards for those that need it





Pipeline status dashboard: https://digital-land-dashboard.herokuapp.com/
digital-land.info service is also instrumented with [Sentry](https://sentry.io/organizations/dluhc-digital-land/issues/)