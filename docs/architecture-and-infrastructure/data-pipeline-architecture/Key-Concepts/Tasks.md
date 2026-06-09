---
title: Tasks
---

## What is a task?

A **task** is a data quality problem that requires action from a data provider, typically an local planning authority (LPA). Tasks are surfaced to providers through the [Submit service](https://submit.planning.data.gov.uk/) so they can identify and fix problems with their data.

Tasks are distinct from [issues](https://datasette.planning.data.gov.uk/digital-land/issue): issues are granular, row-level records of individual data problems produced during pipeline processing. A task is a higher-level, actionable summary — one task may represent many individual issues of the same type on the same resource.

There are two types of task, each with a different source:

### Log tasks

A log task is created when the pipeline **cannot reach or download data from an endpoint**. This happens when the endpoint returns a non-200 HTTP status code (e.g. 404 Not Found, 500 Internal Server Error). The task tells the LPA that their endpoint is inaccessible and needs to be checked.

The `details` field for a log task contains the HTTP status code and any exception message:

```json
{"status": 404, "exception": "Not Found"}
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
| `severity` | Always `error` |
| `responsibility` | Always `external` (provider must fix) |
| `task_source` | Either `log` or `issue` |
| `entry_date` | Date the task was generated |
| `reference` | 16-character unique identifier, derived as a truncated SHA-256 hash of key task fields |

## How tasks are generated

Tasks are generated nightly as part of the [build-digital-land-builder pipeline](https://github.com/digital-land/airflow-dags/blob/main/dags/digital_land_builder.py). See the generate-tasks process documentation for technical details.

The full task table is regenerated from scratch each night and stored as a [Delta Lake](https://delta.io/) table, making it queryable via the Submit service.