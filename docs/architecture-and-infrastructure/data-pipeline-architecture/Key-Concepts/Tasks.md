---
title: Tasks
---

## What is a task?

A **task** is a data quality problem that requires action from a data provider, typically an local planning authority (LPA). Tasks are surfaced to providers through the [Submit service](https://submit.planning.data.gov.uk/) so they can identify and fix problems with their data.

Tasks are distinct from [issues](https://datasette.planning.data.gov.uk/digital-land/issue): issues are granular, row-level records of individual data problems produced during pipeline processing. A task is a higher-level, actionable summary — one task may represent many individual issues of the same type on the same resource.

There are two types of task, each with a different source:

### Log tasks

A log task is created when the pipeline **cannot collect data from an endpoint**. Only the endpoint's latest collection is used, so the task clears once the endpoint collects successfully again.

This happens when:

- **The endpoint is inaccessible:** it returns a non-200 HTTP status code (e.g. 404 Not Found, 500 Internal Server Error), or the connection fails. Severity `error`.
- **The endpoint returns a 200 but no data:**
  - **An error page or unreadable response** (e.g. a WFS `ExceptionReport`, an HTML error page, an authentication error). Severity `error`.
  - **A valid file with no rows** (e.g. a CSV with only a header, or an empty WFS/GeoJSON `FeatureCollection`). Severity `notice`, because an empty file may be correct (e.g. the provider has nothing to publish yet).

A 200 response is treated as having no data when its resource failed to convert, or when it produced no entities from at most one line. To tell an error page from a valid empty file, the pipeline reads the start of the resource: it is a valid empty file if it is a `FeatureCollection`, or if its first line is a header with at least one column that maps to the dataset's fields. A resource that has rows but produces no entities (e.g. every row is missing a reference) does not get a log task; issue tasks already cover it.

The `details` field for a log task contains the HTTP status code and any exception message:

```json
{"status": 404, "exception": "Not Found"}
```

For a 200 with no data, the exception is one of two fixed messages:

```json
{"status": 200, "exception": "Endpoint returned a response that could not be read as data"}
{"status": 200, "exception": "Endpoint returned a valid file with no data"}
```

### Issue tasks

An issue task is created when data was successfully downloaded but contains errors that the pipeline cannot automatically fix. Only issues with severity `error` and responsibility `external` become tasks — these are problems that must be fixed by the data provider, not by the data management team.

Issue tasks are grouped: multiple rows with the same issue type, field, resource, and dataset are collapsed into a single task with a count. The `details` field records what the problem is:

```json
{"issue_type": "invalid-geometry", "count": 3, "field": "geometry"}
```


## Task columns

| Column | Description |
|---|---|
| `dataset` | The dataset the task relates to (e.g. `conservation-area`) |
| `organisation` | The organisation responsible for fixing it |
| `endpoint` | The endpoint hash the task relates to |
| `resource` | The resource hash (empty for log tasks where no resource was downloaded) |
| `details` | JSON string — structure varies by `task_source`, see above |
| `severity` | `error`, except log tasks for a valid file with no data, which are `notice` |
| `responsibility` | Always `external` (provider must fix) |
| `task_source` | Either `log` or `issue` |
| `entry_date` | Date the task was generated |
| `reference` | 16-character unique identifier, derived as a truncated SHA-256 hash of key task fields |

## How tasks are generated

Tasks are generated nightly as part of the [build-digital-land-builder pipeline](https://github.com/digital-land/airflow-dags/blob/main/dags/digital_land_builder.py). See the generate-tasks process documentation for technical details.

The full task table is regenerated from scratch each night and stored as a [Delta Lake](https://delta.io/) table, making it queryable via the Submit service.