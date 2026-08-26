---
title: Provide data
description: The technical flow used by Check and Provide to raise a request for a checked endpoint to be added to the platform.
---

## Purpose

The provide flow takes an endpoint URL that has passed a check and raises a request with the data management team so the endpoint can be configured and collected.

This is the point at which a data owner commits. Checking changes nothing; providing starts the process that puts their data on the Planning Data platform.

Check and Provide does not write any configuration itself. It creates a Jira request containing everything the data management team needs to add the endpoint using the [manage service](../manage-service/).

## Preconditions

The flow can only be reached from the confirmation page of a **passed URL check**. There is no other entry — no deep link, and no way to provide an endpoint that has not been checked.

Two conditions must hold:

- the session must carry the identifier of a completed check
- that check must be a URL check, not a file check

A file check has no endpoint for the pipelines to collect from, so it cannot be provided. Where either condition fails — including where the session has expired — the data owner is returned to the start of the check flow and must check the endpoint again.

## Inputs

The flow uses:

- the request identifier, dataset, organisation, endpoint URL and geometry type, all carried over from the completed check
- the name and email address of the person providing the data
- the documentation URL — the page that links to the endpoint
- confirmation that the data is published under an open licence

Only the last three are entered by the data owner. Everything else comes from the check, so the endpoint being provided is always one that has actually been validated.

## Request and processing flow

| Stage | Technical behaviour |
| --- | --- |
| Precondition check | The application retrieves the completed check request and confirms it is a URL check, then populates the journey state from its parameters |
| Data collection | The application collects contact details, the documentation URL and licence confirmation, validating each step |
| Duplicate protection | Before submitting, the application reserves the endpoint in Redis, renewing the reservation while outbound calls are in flight, so the same endpoint cannot be provided twice concurrently |
| Request creation | The application creates a Jira Service Desk request containing the dataset, organisation, endpoint and documentation details |
| Attachment | A CSV of the submitted answers is attached to the request |
| Notification | A confirmation email is sent through GOV.UK Notify |
| Confirmation | The data owner is shown the Jira reference for their request |

If the Jira request cannot be created the data owner is returned to the check-answers page with an error, and never reaches confirmation. The CSV attachment and internal note are best-effort: a failure there is logged but does not fail the submission, so a request can exist without its attachment.

On success the endpoint reservation is held for 24 hours, so a duplicate submission is rejected until the overnight import picks the endpoint up.

## Validation

Two rules are worth noting because they encode policy rather than format:

- the documentation URL must be on a `gov.uk` or `org.uk` domain, and must be a webpage rather than a data file
- the documentation URL must not be the same as the endpoint URL — it is meant to be the page that *links to* the data, so that a reader can find the data in context

Contact email addresses are similarly restricted to `gov.uk` and `org.uk` domains.

## What happens next

The request leaves the service at this point. A data manager reviews it and uses the manage service's [add data](../manage-service/add-data/) flow to write the endpoint into the [config repository](https://github.com/digital-land/config). The data pipelines read that configuration, collect the data from the endpoint and add it to the platform.

Because collection happens on a scheduled pipeline run rather than immediately, provided data appears on the platform some time after the request is raised, not at the point of submission.

## Service boundaries

Check and Provide owns the collection and validation of the submission, and creating the Jira request.

The data management team owns reviewing the request. The manage service owns writing configuration. The data pipelines own collecting and processing the endpoint.

## Related documentation

- [Submit data guide](https://digital-land.github.io/submit/tutorial-submit-data.html) — the journey at code level
- [Check data](../check-data/) — the flow that must succeed first
- [Manage service — add data](../manage-service/add-data/) — what a data manager does with the request
