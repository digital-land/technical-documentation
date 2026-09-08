---
title: Processes
---

This section covers the processes that we run across our pipelines. There may be some minor differences, such as where results are stored, depending on how and where they are run, but the following pages cover the concepts within each stage with links to the code that needs to be run.

Processes are the individual stages. For how they are orchestrated together to produce a dataset, see [workflows](/architecture-and-infrastructure/data-pipeline-architecture/workflows).

* [Collect](/architecture-and-infrastructure/data-pipeline-architecture/processes/collect) - download resources from a set of endpoints
* [Plan](/architecture-and-infrastructure/data-pipeline-architecture/processes/plan) - create log and resource csvs, and a makefile to be used in the transform and assemble processes
* [Transform](/architecture-and-infrastructure/data-pipeline-architecture/processes/transform) - process a resource against a dataset to produce facts and their provenance
* [Generate tasks](/architecture-and-infrastructure/data-pipeline-architecture/processes/generate-tasks) - build the task table of data quality problems from collection logs and issues
