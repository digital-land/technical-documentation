---
title: Smoke testing
description: How to verify that a deployed Check and Provide environment is working, from a quick health check to a full end-to-end journey.
---

## Purpose

This page describes how to confirm a deployed Check and Provide environment is actually working — after a release, during an incident, or when someone reports a problem.

There are three levels of check. They cover **different things**, so pick based on what you need to know rather than always reaching for the cheapest or the most thorough.

| Level | Time | Covers | Does not cover |
| --- | --- | --- | --- |
| [Health endpoint](#1-health-endpoint) | Seconds | Whether dependencies are reachable | Whether any journey works |
| [Acceptance tests](#2-acceptance-tests) | Minutes, automated | The check journey, including failure cases | The data quality dashboards |
| [Manual end-to-end](#3-manual-end-to-end) | Minutes, manual | Dashboards and the check journey together | The provide journey |

None of these exercise the provide journey to completion, because doing so would raise a real Jira request.

## 1. Health endpoint

Request `/health` on the environment, for example `https://provide.development.planning.data.gov.uk/health`.

The response reports the overall status, the environment, the running commit, and the status of each dependency:

- `s3-bucket` — uploaded file storage
- `request-api` — the async request backend
- `datasette` — reference data
- `redis` — sessions and caches, marked as not required

Overall status is `ok` when everything is up, `degraded` when only a non-required dependency is down, and `down` when a required one is. A `down` response also returns HTTP 500.

This tells you whether the service can reach what it needs. It tells you nothing about whether the journeys work, so a healthy response is a starting point rather than a conclusion.

> Note that this endpoint returns `ok` rather than the `healthy` described in the [monitoring guidance](/development/monitoring/). The dependency-level detail follows the guidance; the status wording does not.

## 2. Acceptance tests

The service repository has an acceptance suite that drives a real browser against a **deployed** environment rather than a local one. This is the automated equivalent of the manual journey below, and should be the default choice.

```sh
cd submit
npm run test:acceptance
```

`NODE_ENV=development` is set by the script, so it targets `https://provide.development.planning.data.gov.uk/`. The target comes from the `url` value in the matching config file, so a different environment can be checked by changing `NODE_ENV`.

`test/acceptance/request_check.test.js` deep-links into the check tool as Adur District Council and runs a check against:

- a well-formed file, expecting a clean result
- a file with known errors, expecting those errors to be reported
- a URL with an expired SSL certificate, expecting the certificate failure to be reported
- an HTML page rather than a data file, expecting that to be rejected

It therefore covers most of the [URL failure modes](../check-data/#url-failures) as well as the happy path. The fixtures come from the [PublishExamples](https://github.com/digital-land/PublishExamples) repository, so the test does not depend on a third party keeping a file available.

What it does not cover is the `/organisations` dashboards — it enters the check tool by deep link rather than by navigating from a dashboard page.

## 3. Manual end-to-end

Use this when you want to confirm the dashboards and the check journey work **together**, which is the one thing the other two levels do not tell you.

1. Open the organisation overview page for a known-good dataset and organisation:
   `https://provide.development.planning.data.gov.uk/organisations/local-authority:ADU/brownfield-land/overview`
2. Confirm the page renders, and copy the endpoint URL shown on it. At the time of writing that is
   `https://www.adur-worthing.gov.uk/media/Media,146509,smxx.csv`
3. Go to Check and Provide, choose the brownfield land dataset, and submit that URL
4. The check should complete and come back clean

This works because the endpoint is one the platform already collects, so it is known to be valid. Step 1 exercises the dashboard reads — Datasette and the platform API — and steps 3 and 4 exercise the check path through the async request backend. A failure at step 1 and a failure at step 4 point at quite different problems.

### Caveats

**It depends on a third-party URL.** If Adur and Worthing move or remove that file, this test will fail in a way that looks like a Check and Provide fault. Before concluding the service is broken, confirm the URL still resolves — and if it does not, take the current endpoint URL from step 1 rather than the one written above.

**It is manual.** The improvement worth making is extending the acceptance suite to cover the dashboard-to-check hop, which would fold this level into level 2 and remove the dependency on a live council endpoint.

## Related documentation

- [Check data](../check-data/) — what the check flow does and how URL failures are handled
- [Monitoring](/development/monitoring/) — the health check standard
- [Deploy and release procedure](/development/deploy-and-release-procedure/)
- [Run book](/run-book/) — handling incidents
