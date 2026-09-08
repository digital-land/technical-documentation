---
title: Batch Processing & Our Pipelines
---

**These are the pipelines which load data into the platform**. 

The main implementation of our data architecture is via a set of pipelines which are scheduled (or manually triggered) via airflow. We schedule them once a night. 

The workflows themselves are described in [workflows](/architecture-and-infrastructure/data-pipeline-architecture/workflows). The collections workflow now has its own page there; the two below will follow.

Airflow utilises DAGs to trigger a set of jobs/tasks. We have DAGs representing these pipelines, and DAGs which trigger other DAGs to run multiple pipelines in the correct order.

### Data Package Pipelines

This hasn't been generalised yet so may need some thought on generalisation moving forward. This pipeline is very simple as it just builds the organisation.csv.

It is another DAG in airflow and is triggered once the required data collection pipelines have been run. 

The build is run using [data-package-builder-task](https://github.com/digital-land/data-package-builder-task)


### Digital Land Pipeline

A very specific pipeline which builds the digital-land.sqlite3 and loads the relevant information from it into the platform. It also runs the jobs which build the task and provision quality tables.

This runs in airflow as the `build-digital-land-builder` DAG, defined in [digital_land_builder.py](https://github.com/digital-land/airflow-dags/blob/main/dags/digital_land_builder.py). The build itself uses the [digital-land-builder](https://github.com/digital-land/digital-land-builder) repository.

`performance.sqlite3` is built separately, by the `build-performance-dataset` DAG.

Once the sqlite file is uploaded to s3 we use the same code as in the data collection pipelines to load data into our postgis using [digital-land-postgres](https://github.com/digital-land/digital-land-postgres)
