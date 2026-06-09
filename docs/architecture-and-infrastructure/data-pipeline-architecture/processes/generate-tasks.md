---
title: Generate tasks
---

# Generate tasks

The generate-tasks process reads collection logs and issue data produced by the nightly pipeline runs and produces a [task](../Key-Concepts/Tasks.md) table.
 This gives data providers a single queryable source of data quality problems they need to fix.

## When it runs

The process runs nightly as the `assemble-tasks` task in the [build-digital-land-builder DAG](https://github.com/digital-land/airflow-dags/blob/main/dags/digital_land_builder.py). It runs in parallel with the main `build-digital-land-builder` task — both start after `configure-dag` and neither depends on the other completing first.

## What it reads

For each collection in S3, the job reads three files:

| File | Path | Used for |
|---|---|---|
| Log | `{collection}/collection/log.csv` | Identifying failed endpoint requests |
| Resource | `{collection}/collection/resource.csv` | Determining which resources are currently active and which dataset they belong to |
| Source | `{collection}/collection/source.csv` | Mapping endpoint hashes to dataset names (used when an endpoint has no resource — i.e. it has never successfully downloaded) |
| Issues | `{collection}/issue/{dataset}/{resource}.csv` | Identifying data quality errors in downloaded resources |

## Filtering rules

**Log tasks** — a task is created for any log entry where `status != 200`.

**Issue tasks** — a task is created for any issue where `severity = error` AND `responsibility = external`. Issues are grouped by dataset, resource, field, and issue-type: multiple rows with the same grouping key produce one task with a count of how many rows were affected.

## What it writes

The output is a [Delta Lake](https://delta.io/) table written to `s3://{env}-parquet-datasets/task/`. The table is fully overwritten on each run — it always reflects the current state of all collections.

The table schema matches the [task columns](../Key-Concepts/Tasks.md#task-columns) defined in the key concepts page.

## Implementation

The job is implemented as a PySpark EMR Serverless job in [pyspark-jobs](https://github.com/digital-land/pyspark-jobs). The entry point is `entry_points/run_tasks.py`; the pipeline logic lives in `src/jobs/pipeline.py` (`TaskPipeline`) and `src/jobs/transform/task_transformer.py`.