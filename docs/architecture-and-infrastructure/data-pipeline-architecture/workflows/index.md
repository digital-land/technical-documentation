---
title: Workflows
---

A **workflow** is a set of processes orchestrated together to produce a particular output. Each one
is an Airflow DAG (or a family of generated DAGs) in the
[airflow-dags repository](https://github.com/digital-land/airflow-dags).

This is the high level view: what each workflow is for, when it runs, what it produces and which
repositories are involved. The individual stages that workflows are built from are documented
separately under [processes](/architecture-and-infrastructure/data-pipeline-architecture/processes).

## The workflows

* [Collections](/architecture-and-infrastructure/data-pipeline-architecture/workflows/collections) - collect data from external endpoints and publish it as a dataset. One DAG per collection, generated from the specification.

The following workflows are not yet documented in their own pages. Until they are, they are described
in [batch processing and our pipelines](/architecture-and-infrastructure/data-pipeline-architecture/batch-processing).

* **Reporting** - `build-digital-land-builder` builds `digital-land.sqlite3` and loads it into the platform, and also runs the task and provision quality jobs. `build-performance-dataset` builds `performance.sqlite3`.
* **Configuration** - the `configuration` DAG processes our configuration files into the parquet datasets bucket and the digital land database.

## Other DAGs

These are real workflows but are smaller in scope, and do not currently have their own pages:

| DAG | What it does |
|---|---|
| `trigger-collection-dags-scheduled` | The nightly "DAG of DAGs" that runs everything else in the right order |
| `trigger-collection-dags-manual` | The same ordering, triggered on demand rather than on a schedule |
| `organisation-collection`, `organisation-builder` | Build the organisation data package, which most collections depend on |
| `maintain-delta-tables` | Weekly maintenance of the Delta tables in the parquet datasets bucket |
| `manual-postgres-loader`, `manual-tiles-loader` | Manually re-run a load step without re-running its collection |

