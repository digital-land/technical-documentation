---
title: Debugging Live Services
---

## Async processor API

TBC

## Main application (digital-land.info)

TBC

## Planning data design

TBC

## Check and Provide service

For what the service does and how it is put together, see the [Check and Provide](/code-base/check-and-provide/) section. Two pages are particularly useful when something is wrong in a live environment:

- [Smoke testing](/code-base/check-and-provide/smoke-testing/) — how to confirm whether an environment is actually broken, starting with the `/health` endpoint
- [Check data](/code-base/check-and-provide/check-data/#url-failures) — the URL failure modes, which explain most reported "the check is broken" cases

### Before you dig in

Request `/health` on the environment first — for example `https://provide.planning.data.gov.uk/health`. It reports the status of the async request backend, Datasette, S3 and Redis individually, so it will tell you immediately whether the problem is Check and Provide or something it depends on.

### Check service error

When the check service is returning an error, the best way to debug it is to use the async processor API to check the data.

To do this, follow the steps below:

1. Get a check request ID from the check service.
   This can be found in the URL of the check tool. It will be a long string of characters, for example: `https://provide.planning.data.gov.uk/check/results/bJKVgr5DmDCwXYgCLX4umk/28` the ID would be `bJKVgr5DmDCwXYgCLX4umk`.
2. Use the async processor API to check the data, at `{async-api}/requests/{check_request_id}`.
   Use the same host the service itself uses for that environment:

   | Environment | Async request API |
   | --- | --- |
   | Production | `https://pub-async.planning.data.gov.uk` |
   | Staging | `https://pub-async.staging.planning.data.gov.uk` |
   | Development | `https://pub-async.development.planning.data.gov.uk` |

   This will return the check request status and the results.
   The results will be a JSON object with the following fields:
   - `status`: The status of the check request.
   - `response.data`: The results of the check request.
   - `response.error`: The errors of the check request.
3. The status can be `COMPLETE`, but may still have `response.error`. Note that both `COMPLETE` and `FAILED` mean processing has stopped — the service treats either as finished, so a failed request must be identified by its status rather than by whether it has completed.
4. If the status is `COMPLETE` and there is no `response.error`, then the data is valid.

### The check reports something the user disagrees with

Issue types, severities, conversion and field mapping are produced by the pipeline code inside the async request backend, not by Check and Provide. The service only renders what it is given, so a result that looks wrong is usually explained in the backend rather than in the frontend application.
