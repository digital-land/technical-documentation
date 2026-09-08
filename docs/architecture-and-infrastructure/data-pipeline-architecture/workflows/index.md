---
title: Workflows
---

A **workflow** is a set of processes orchestrated together to produce a particular output. Each one is an Airflow DAG (or a family of generated DAGs) in the [airflow-dags repository](https://github.com/digital-land/airflow-dags).

This is the high level view: what each workflow is for, when it runs, what it produces and which repositories are involved. The individual stages that workflows are built from are documented separately under [processes](/architecture-and-infrastructure/data-pipeline-architecture/processes).

## The workflows

* [Collections](/architecture-and-infrastructure/data-pipeline-architecture/workflows/collections) - collect data from external endpoints and publish it as a dataset. One DAG per collection, generated from the specification.
* [Reporting](/architecture-and-infrastructure/data-pipeline-architecture/workflows/reporting) - build the platform wide databases and the cross collection task and provision quality tables.
* [Configuration](/architecture-and-infrastructure/data-pipeline-architecture/workflows/configuration) - process the configuration files into tables the rest of the platform can query.

## Other DAGs

These are real workflows but are smaller in scope, and do not currently have their own pages:

| DAG | What it does |
|---|---|
| `trigger-collection-dags-scheduled` | The nightly "DAG of DAGs" that runs everything else in the right order |
| `trigger-collection-dags-manual` | The same ordering, triggered on demand rather than on a schedule |
| `organisation-collection`, `organisation-builder` | Build the organisation data package, which most collections depend on |
| `maintain-delta-tables` | Weekly maintenance of the Delta tables in the parquet datasets bucket |
| `manual-postgres-loader`, `manual-tiles-loader` | Manually re-run a load step without re-running its collection |

