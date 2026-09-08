---
title: Batch Processing & Our Pipelines
---

**These are the pipelines which load data into the platform**. 

The main implementation of our data architecture is via a set of pipelines which are scheduled (or manually triggered) via airflow. We schedule them once a night. 

The workflows themselves are described in [workflows](/architecture-and-infrastructure/data-pipeline-architecture/workflows). The collections, reporting and configuration workflows each have their own page there. The data package pipeline below is the last one still described here.

Airflow utilises DAGs to trigger a set of jobs/tasks. We have DAGs representing these pipelines, and DAGs which trigger other DAGs to run multiple pipelines in the correct order.

### Data Package Pipelines

This hasn't been generalised yet so may need some thought on generalisation moving forward. This pipeline is very simple as it just builds the organisation.csv.

It is another DAG in airflow and is triggered once the required data collection pipelines have been run. 

The build is run using [data-package-builder-task](https://github.com/digital-land/data-package-builder-task)
