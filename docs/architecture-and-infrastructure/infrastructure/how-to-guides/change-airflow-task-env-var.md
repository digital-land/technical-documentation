---
title: Change an Airflow task environment variable
---

## Background

 * Airflow tasks run on an AWS MWAA environment
 
 * Environment variables are detailed in the tasks within a Directed Acyclic Graph (DAG)
 
 * DAGs are provisioned via Python files within the `/dags` directory of the [airflow-dags](https://github.com/digital-land/airflow-dags/) code repository

## Steps

To change an Airflow task's environment variables:

  1. Navigate to the [airflow-dags](https://github.com/digital-land/airflow-dags/) code repository
  1. Navigate to the Python file which generates the DAG for the Airflow task you want to change, e.g. for collection tasks that would be the file `/dags/collection_generator.py`
  1. Within the DAG, you will likely be able to easily identify where  environment variable key-value pairs are defined.  For example, the collection tasks make use of an `EcsRunTaskOperator` which contains an overrides parameter for the ECS container which ultimately runs the task.  One of the overrides parameters is named `environment` and should contain an array of name-value maps.
  1. To add a new variable, simply append a new key value pair to the collection.  
  1. You can also change an existing value
  1. It's also possible to remove a key value pair which is no longer needed.  Consider what impact this might have on the task. 
  1. Run a Terraform plan in the usual way to review that your changes are as expected
  1. Finally, run a Terrraform apply if you are happy to proceed

 > [!TIP]
 > Always try to make changes in a backwards (and forwards) compatible manner