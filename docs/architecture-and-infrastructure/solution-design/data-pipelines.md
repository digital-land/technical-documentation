# Solution design - Data Pipelines

Our data pipelines system is set upp to complete batch and dynamic pocessing to support the service. It's worth reviewing our data architecture to understand the data flow of pipelines.

### C4 System Diagram

![Data Pipelines container structure](/images/data-pipelines/containers.drawio.png)

> 🔜 The dynamic processing we can perform is currently in the provide service diagrams and should be moved into here or it's own system.

### Interaction

![Data Pipelines container interaction](/images/data-pipelines/container-interaction.drawio.png)

### Infrastructure Diagram

![Data Collection Pipeline Infrastructure](/images/data-collection-pipeline-deployment.drawio.png)

### Workflow Orchestrator

The workflow orchestrator is an instance of airflow running using AWS's [Managed Workflow's for Apache Airflow Service (MWAA)](https://aws.amazon.com/managed-workflows-for-apache-airflow/).
The code for this is in our infrastructure repository. For information on the Airflow DAGs that are ran see the Workflow Definition Store below.

#### Alerting and Monitoring

Alerts:
- Slack is integrated into the production MWAA instance and can be used to alert when DAGs fail.

Notifications:
- None right now

Key Metrics:
- (provided) MemoryUtilisation (both for BaseWorker and Additional Worker Clusters) - We have experienced 'zombie tasks' in the past and we identified that the workers were reaching above 90% utlisation.
- (provided) CPUUtilization (both for BaseWorker and Additional Worker Clusters) - while this hasn't caused any outages it's worth examining

> 🔜 We need to add Alerts and notifications for the metrics above. This will be done through AWS alarms. Production alarms will be alerts and other environment alarms will be notifications

## Code

### Classes (WIP)

![Data Pipelines classes](/images/data-pipelines/classes.drawio.png)

## References

- [Managed Workflow's for Apache Airflow Service (MWAA)](https://aws.amazon.com/managed-workflows-for-apache-airflow/)
- [Airflow](https://airflow.apache.org/docs/apache-airflow/stable/index.html)

