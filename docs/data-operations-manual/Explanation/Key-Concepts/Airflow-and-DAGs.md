## Airflow & DAGs

The data collection pipelines are run in Airflow on AWS managed service known as [MWAA](https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html).

Airflow's jobs are defined using a Directed Acyclic Graph (DAG).  The DAGs are generated via the [airflow-dags](https://github.com/digital-land/airflow-dags/) repo. 
