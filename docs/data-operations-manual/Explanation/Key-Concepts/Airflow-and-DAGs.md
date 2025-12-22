---
title: Airflow & DAGs
---

### Airflow

The data collection pipelines are run in [Airflow](https://airflow.apache.org/) on AWS managed service known as [MWAA](https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html).

### Airflow UI

The Airflow UI is a web application with a HTML Graphical User Interface.

### URL for Airflow UI

A member of the Infrastructure team will be able to provide you with the environment-specific URLs for Airflow.

### DAGs

Airflow's jobs are defined using a Directed Acyclic Graph or ([DAG](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html)) for short.  The DAGs are generated via the [airflow-dags](https://github.com/digital-land/airflow-dags/) repo. 
