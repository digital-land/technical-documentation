---
title: Reporting
---

The reporting workflow builds the platform wide databases and the cross collection tables. Where the [collections](/architecture-and-infrastructure/data-pipeline-architecture/workflows/collections) workflow produces one dataset at a time, reporting looks across every collection at once: what we hold, where it came from, and what is wrong with it.

It is the last thing to run each night, because most of what it reports on is produced by the collection workflows that run before it.

## When it runs

`build-digital-land-builder` is `schedule=None` and is triggered by `trigger-collection-dags-scheduled` once every collection DAG has finished. It uses the `ALL_DONE` trigger rule, so it still runs when some collections have failed — a broken collection should not stop us reporting on the rest.

`build-performance-dataset` is a separate DAG which is **not** triggered by the nightly run — it only runs when someone triggers it. It runs `build-performance.sh` on the collection task definition, and its DAG description says it generates provision quality parquet and uploads it to S3. Note that `performance.sqlite3` itself is built by the main build above, not by this DAG.

## The steps

Two independent branches hang off `configure-dag`, and they run in parallel.

The **build branch** produces the databases and loads them:

| Task | Runs on | What it does |
|---|---|---|
| `build-digital-land-builder` | ECS Fargate | Runs [digital-land-builder-task](https://github.com/digital-land/digital-land-builder-task), which builds `digital-land.sqlite3` and then, in a third pass, `performance.sqlite3` |
| `digital-land-postgres-loader` | ECS Fargate | Loads the digital land database into the platform database |
| `invalidate-cloudfront-cache` | Airflow | Clears the CDN so the new data is actually served rather than a cached copy |
| `wait-before-reporting`, `run-reporting-task` | Airflow, ECS Fargate | Production only. Waits ten minutes for datasette to become consistent, then runs [reporting-task](https://github.com/digital-land/reporting-task) |

The **cross collection branch** produces the tables we surface to data providers:

| Task | Runs on | What it does |
|---|---|---|
| `get-emr-app-id` | Airflow | Finds the EMR Serverless application to submit jobs to |
| `assemble-tasks` | EMR Serverless | Builds the [task](/architecture-and-infrastructure/data-pipeline-architecture/Key-Concepts/Tasks) table from collection logs, issues and expectations |
| `provision-quality` | EMR Serverless | Builds the [provision quality](/architecture-and-infrastructure/data-pipeline-architecture/Key-Concepts/Provision-Quality) tables |

Both of these read directly from the collection data bucket rather than from the built `digital-land.sqlite3`, which is why they do not have to wait for the build. Keeping them off the critical path matters, because the whole workflow has to finish before the platform is refreshed in the morning.

## Tools and services

Airflow (AWS MWAA) orchestrates the workflow, ECS Fargate runs the build and load containers, EMR Serverless runs the two PySpark jobs, and CloudFront serves the results once its cache has been invalidated.

## Repositories

| Repository | Part it plays |
|---|---|
| [airflow-dags](https://github.com/digital-land/airflow-dags) | The DAG, in `dags/digital_land_builder.py` |
| [digital-land-builder-task](https://github.com/digital-land/digital-land-builder-task) | Builds `digital-land.sqlite3` and `performance.sqlite3` |
| [digital-land-postgres](https://github.com/digital-land/digital-land-postgres) | Loads the digital land database into the platform |
| [pyspark-jobs](https://github.com/digital-land/pyspark-jobs) | The `assemble-tasks` and `provision-quality` EMR jobs |
| [reporting-task](https://github.com/digital-land/reporting-task) | The production only reporting step |
