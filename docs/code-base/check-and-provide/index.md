---
title: Check and Provide
description: A high-level technical overview of the service data owners use to check and provide planning data.
---

## What Check and Provide does

Check and Provide is the service data owners use to validate planning data against a dataset specification and then offer it to the Planning Data platform. It is the entry point for data arriving on the platform, and it sits in front of the manage service.

> Checking is validation without commitment: a data owner points the service at a URL or uploads a file, and gets back a report of what is wrong. Nothing is added to the platform, and there is no obligation to go further. Providing is the separate, opt-in step that follows a successful URL check — it raises a request with the data management team so the endpoint can be configured and collected.

The service supports two main flows:

- [Check data](check-data/) validates a URL or uploaded file against the dataset specification and reports the issues found.
- [Provide data](provide-data/) takes a URL that has passed a check and raises a request to have that endpoint added to the platform.

Alongside these, the service publishes data quality dashboards at `/organisations`, which show a local planning authority what it has provided and what is wrong with it.

Check and Provide coordinates these flows without performing the validation itself. The longer-running conversion and validation work is delegated to the async request backend.

## Who uses Check and Provide

Check and Provide is used by data owners publishing planning data — mostly local planning authorities, but also consultants and anyone else preparing data on their behalf. The service is open and requires no sign-in, so a check can be run by anyone with a URL or a file.

Data managers and developers also use the dashboards when investigating the quality of a particular organisation's data.

## Technical overview

Check and Provide is a server-rendered web application. It provides the user interface and coordinates requests between data owners, shared Planning Data services and Jira.

| Area | Technology or approach |
| --- | --- |
| Application | Node.js and the Express web framework |
| Application structure | Setup modules assemble the app; pages are built as chains of small middleware functions |
| Web pages | Server-rendered Nunjucks templates using GOV.UK Frontend |
| Multi-step journeys | `hmpo-form-wizard`, with each journey defined by its steps, fields and controllers |
| Session storage | Express sessions, persisted in Redis where available and falling back to an in-memory store |
| Reference data | Datasette queries, with some reads served by the Planning Data platform API |
| File storage | Amazon S3 for uploaded files |
| Longer-running processing | Delegated to the async request backend rather than performed in a web request |
| Outbound requests | Jira Service Desk for provide requests, GOV.UK Notify for confirmation emails |
| Packaging | A Docker container containing the Node application and compiled frontend assets |
| Delivery | GitHub Actions runs tests, builds the container image and publishes it to Amazon Elastic Container Registry in the `eu-west-2` AWS region |

The repository supports development, staging and production service environments. The infrastructure that runs the published container is managed separately from the application repository.

### Caching

A small number of reference lists are cached in Redis to avoid repeating expensive queries:

| Cached data | Lifetime |
| --- | --- |
| Organisation list and related reference lookups | 6 hours |
| Dataset subject map (the grouped dataset list shown in the UI) | 1 minute in local and development, 1 hour elsewhere |

These caches hold derived, non-sensitive lists rather than user data. If Redis is unavailable the service still runs, but rebuilds these lists more often, which makes pages slower and increases load on upstream services. Sessions are also affected: without Redis they are held in memory, so they are lost on restart and are not shared between instances.

## Application responsibilities

The Express application:

- presents the check and provide journeys
- validates user input before a request is created, including a pre-flight check that the submitted URL is reachable
- submits check requests to the async request backend and polls for results
- presents validation results, issue detail and maps of submitted geometry
- publishes data quality dashboards for local planning authorities
- raises a Jira request when a data owner chooses to provide a checked endpoint
- sends confirmation emails through GOV.UK Notify

This separation keeps the web application focused on user interaction and orchestration. The async request backend performs the conversion and validation work.

## System context

A data owner checks their data, fixes what the report tells them to fix, and then provides the endpoint. That submission creates a Jira request containing the dataset, organisation, endpoint and documentation details the data management team needs.

<div class="manage-service-flow" role="region" aria-label="Flow showing how data moves from a data owner through checking and providing to the Planning Data platform" tabindex="0">
<pre>
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│    <strong><u>Data owner</u></strong>    │   │    <strong><u>Check data</u></strong>    │   │     <strong><u>Results</u></strong>      │   │   <strong><u>Provide data</u></strong>   │
│                  │   │                  │   │                  │   │                  │
│ Publish endpoint │──▶│ Validate against │──▶│ Issues to fix,   │──▶│ Raise a request  │
│ or upload a file │   │ the specification│   │ or a clean check │   │ for the endpoint │
└──────────────────┘   └──────────────────┘   └──────────────────┘   └────────┬─────────┘
                                                                              │
                                                                              ▼
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│  <strong><u>Planning Data</u></strong>   │   │  <strong><u>Data pipelines</u></strong>  │   │  <strong><u>Manage service</u></strong>  │   │   <strong><u>Jira request</u></strong>   │
│                  │   │                  │   │                  │   │                  │
│ Data published   │◀──│ Collect and      │◀──│ Add endpoint to  │◀──│ Endpoint details │
│ on the platform  │   │ process the data │   │ configuration    │   │ for review       │
└──────────────────┘   └──────────────────┘   └──────────────────┘   └──────────────────┘
</pre>
</div>

Check and Provide owns the left-hand half of this flow. Once the Jira request is raised the endpoint is handled by the [manage service](../manage-service/), and the data pipelines later collect and process it.

Only a checked **URL** can be provided. A file check has no endpoint for the pipelines to collect from, so it ends at the results page.

## Main integrations

| Service or repository | Integration |
| --- | --- |
| [Async request backend](https://github.com/digital-land/async-request-backend) | Fetches, converts and validates submitted data and returns issues |
| Datasette | Provides dataset, organisation, specification and issue reference data |
| [Planning Data website and API](https://www.planning.data.gov.uk/) | Provides published entity and task information used by the dashboards |
| [Specification](https://github.com/digital-land/specification) | Defines datasets, fields and provision rules, and supplies the relationship diagrams shown in guidance |
| [Config repository](https://github.com/digital-land/config) | Holds the collection and pipeline configuration that a provided endpoint is eventually added to |
| Jira Service Desk | Receives provide requests for the data management team |
| GOV.UK Notify | Sends confirmation emails |
| Amazon S3 | Stores uploaded files pending checking |
| Redis | Stores sessions and cached reference lists |

Note that `digital-land-python` is **not** a direct dependency. It runs inside the async request backend and the collection pipelines, so check results reflect its behaviour without this application using it.

## Detailed documentation

Implementation-level detail is published from the service repository:

- [Architecture](https://digital-land.github.io/submit/tutorial-architecture.html) — boot sequence, routes, form wizards, error handling and configuration
- [Middleware guidelines](https://digital-land.github.io/submit/tutorial-middleware-guidelines.html) — conventions for adding a route
- [Check data](https://digital-land.github.io/submit/tutorial-check-data.html) and [Submit data](https://digital-land.github.io/submit/tutorial-submit-data.html) — the two journeys at code level
- [Review data quality](https://digital-land.github.io/submit/tutorial-review-data-quality.html) — the dashboards
- [Dependencies](https://digital-land.github.io/submit/tutorial-dependencies.html) — services and external systems

Related technical documentation:

- [Solution design — Check Service](/architecture-and-infrastructure/solution-design/check-service/) — container diagrams
- [Smoke testing](smoke-testing/) — how to verify a deployed environment
- [Data pipeline architecture](/architecture-and-infrastructure/data-pipeline-architecture/)
