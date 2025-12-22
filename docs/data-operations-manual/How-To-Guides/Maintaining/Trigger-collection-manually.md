---
title: Trigger collection manually
---

Data collection pipelines are executed via [Airflow](/data-operations-manual/Explanation/Key-Concepts/Airflow-and-DAGs).

Collections are usually run on a scheduled-basis by having them selected in the [scheduling configuration of airflow-dags](https://github.com/digital-land/airflow-dags/blob/main/bin/generate_dag_config.py#L13) repo.  However, if you want to execute a collection run manually, you can do so by
 navigating to the [Airflow UI](/data-operations-manual/Explanation/Key-Concepts/Airflow-and-DAGs/#airflow-ui), finding the relevant collection DAG and clicking the corresponding play button (blue triangle) to trigger an execution e.g. 

![Airflow DAG play button execution](/images/data-operations-manual/airflow-dag-play-button.png)

Depending on the collection, this can take a while but after it has finished running you can check on datasette if the expected data is on the platform.
