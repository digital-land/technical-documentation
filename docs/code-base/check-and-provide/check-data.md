---
title: Check data
description: The technical flow used by Check and Provide to validate a data owner's URL or file against a dataset specification.
---

## Purpose

The check flow validates planning data against a dataset specification and reports what is wrong with it, without changing anything on the platform.

Check and Provide collects the input, validates it before a request is created, and presents the results. The async request backend performs the fetching, conversion and validation.

A data owner can run a check as many times as they like. Most use it iteratively: check, fix, check again, until the report comes back clean.

## Inputs

The flow uses:

- the dataset, and for some datasets a geometry type
- the providing organisation
- either an endpoint URL, or an uploaded file
- optional column mappings, where the data owner's column names do not match the specification

Dataset and organisation can be supplied as query parameters, which lets the data quality dashboards link straight into a pre-filled check.

## Request and processing flow

| Stage | Technical behaviour |
| --- | --- |
| Journey state | The application stores the dataset, organisation and upload method in the user session |
| Pre-flight validation | For a URL, the application makes a HEAD request before creating an async request, rejecting URLs that are malformed, missing, blocked or too large. For a file, it checks type, size and file name |
| Request creation | The application submits an async `check_url` or `check_file` request and stores the returned request identifier in the session |
| Polling | The status page polls an internal endpoint until the async request reports that processing has finished |
| Column mapping | Where unmapped specification fields and unused source columns both remain, the application offers a mapping step and resubmits as a new request |
| Results | The application retrieves the completed request and its response details, and renders the issues found |

Results pages are addressable and can be shared. Arriving at a results URL directly repairs the session from the request itself, so a shared link behaves the same as walking the journey.

## Processing results

The async request backend returns the converted rows, a column mapping log and a task log describing the issues found.

Check and Provide uses these to render:

| Result | Purpose |
| --- | --- |
| Issue summary | Groups the issues found by type and field |
| Issue detail | Shows the affected rows or entities for a single issue type |
| Data table | Shows the submitted records after conversion |
| Map | Renders submitted geometry for spatial datasets, with the organisation's boundary for context |
| Confirmation | For a passed URL check, offers the option to go on and [provide the endpoint](../provide-data/) |

Issues are attributed as either the data owner's responsibility or the platform's. Only the data owner's are presented as things to fix.

## URL failures

Because the service fetches a URL the data owner controls, a large part of the check flow is handling URLs that cannot be fetched. Failures are caught in two places, and it matters which:

- **Before the request is created** — malformed URLs, 404s, 403s from bot protection or a firewall, and responses that are too large. These produce a form error, so the data owner sees the problem immediately.
- **By the async request backend** — SSL certificate failures, and pages that return HTML instead of data. These produce a failed request, reported on the results page.

Two cases are not currently caught by either. A JavaScript bot challenge returns a valid response to the checks the service makes, so the check proceeds and fails later with an unhelpful message. A link to a data portal viewer page, rather than the download endpoint behind it, is reachable and returns HTML, so the data owner has to find the real URL themselves.

The [check data guide](https://digital-land.github.io/submit/tutorial-check-data.html) in the service repository lists each failure, where it is caught and how to reproduce it.

## Service boundaries

Check and Provide owns input validation, request coordination and the presentation of results.

The async request backend owns fetching, conversion and validation. The issue types, severities and conversion behaviour that shape a report come from the pipeline code, not from this application — a result that looks wrong is usually explained there rather than here.

## Related documentation

- [Check data guide](https://digital-land.github.io/submit/tutorial-check-data.html) — the journey at code level
- [Get started and deep links](https://digital-land.github.io/submit/tutorial-get-started.html) — how the dashboards link into a pre-filled check
- [Provide data](../provide-data/) — what happens after a passed URL check
- [Smoke testing](../smoke-testing/) — verifying the flow works in a deployed environment
