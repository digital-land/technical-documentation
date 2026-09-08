---
title: Configuration
---

Configuration is how the data management team describes what should happen to data as it moves through the pipeline: which endpoints to collect from, how columns map onto our schemas, which entities belong to which organisation, and what tests should be run. It lives in the [config repository](https://github.com/digital-land/config) as a set of CSV files per collection.

The configuration workflow processes those files into forms the rest of the platform can query, rather than every job having to read the raw CSVs.

## When it runs

The `configuration` DAG is `schedule=None`, and **nothing triggers it automatically** — it is not part of the nightly `trigger-collection-dags-scheduled` sequence. It runs when someone triggers it, typically after a change to the config repository.

This is worth knowing when config changes appear not to have taken effect: the collection workflows read configuration directly from the config files in S3, but anything reading the processed configuration tables will not see a change until this DAG has been run.

## The steps

| Task | Runs on | What it does |
|---|---|---|
| `get-tasks-emr-app-id` | Airflow | Finds the EMR Serverless application to submit the job to |
| `assemble-tasks` | EMR Serverless | Runs `run_config.py` from [pyspark-jobs](https://github.com/digital-land/pyspark-jobs), reading the config files from `s3://{env}-collection-data/` |

The `assemble-tasks` task id is misleading — it is a copy of the naming used in the reporting workflow, and this task has nothing to do with the task table. It runs the configuration job.

The DAG takes a `debug` parameter, which turns on debug logging for the Spark job.

## What it produces

Configuration data in the parquet datasets bucket (`s3://{env}-parquet-datasets/`) as Delta tables, and configuration data in the digital land database.

## Repositories

| Repository | Part it plays |
|---|---|
| [airflow-dags](https://github.com/digital-land/airflow-dags) | The DAG, in `dags/configuration.py` |
| [config](https://github.com/digital-land/config) | The configuration files themselves, owned by the data management team |
| [pyspark-jobs](https://github.com/digital-land/pyspark-jobs) | The EMR Serverless job which processes them |
