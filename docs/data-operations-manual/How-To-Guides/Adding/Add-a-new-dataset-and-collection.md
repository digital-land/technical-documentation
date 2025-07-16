# Add a new dataset and collection

The following instructions are for when adding an entirely new dataset to the platform which does not have a corresponding collection configuration.

If you’re adding a new dataset to an existing collection you can follow the same process, but ignore step 2.

#### 1. Ensure the collection is noted in the dataset specification

Skipping this step won't result in any specific errors but is strongly recommended to ensure that the list of collections in the specification is up to date. 

Go to https://github.com/digital-land/specification/tree/main/content/dataset and check if there is a .md file for your new dataset 

E.g., if you plan to add a dataset named article-4-direction you want to check that https://github.com/digital-land/specification/tree/main/content/dataset/article-4-direction.md exists. That’s all!

If it doesn’t exist, raise this issue with the Data Design team and they should be able to set it up.

#### 2. Create Collection and Pipeline config in the [config repo](https://github.com/digital-land/config)

The [config repo](https://github.com/digital-land/config)  contains collection and pipeline folders for each unique collection held within the pipeline. In this case, there won’t be one for the new collection.
You'll need to create new folders ( `collection` and `pipeline`) and the required files within those folders for the collection that needs to be created. There is a really handy script for this step, simply run create_collection.py like so: 
python create_collection.py [DATASET NAME] E.g., python create_collection.py article-4-direction

Check that this has created the following files and that only the headers are in them:
* collection
   * endpoint.csv
   * source.csv
   * old-resource.csv        
* pipeline	
  * column.csv  
  * combine.csv
  * concat.csv
  * convert.csv
  * default-value.csv
  * default.csv
  * expect.csv
  * filter.csv
  * lookup.csv
  * old-entity.csv
  * patch.csv
  * skip.csv
  * transform.csv



#### 3. Add endpoint(s) for the new dataset (optionally mapping and default values)

In case a column-field mapping was provided, you’ll need to add the mapping to column.csv. Make sure to map to the correct data, we want to map some column to its equivalent `field` e.g the dataset might have a different name for the reference so we need to map this to our `reference` field.

In case there is a defaultValue given for a field in the schema, we want to add this to the default-value.csv.

Follow steps 3 and 4 in ‘Adding an Endpoint’ for instructions on adding mapping and default values.

Next, you can just proceed to add an endpoint. Validating the data through the endpoint checker will not work at this point but we can manually check whether the endpoint_url and documentation_url work as well as whether the required fields specified in the schema are present.   There will be no further need to validate it. Once the PR is merged, you can go to the next step.

Note: If the dataset being added is a spatial dataset (i.e., it contains geometry), a column mapping must be included to map WKT to geometry. Without this mapping, the dataset will not have any geometry.

### 4. Test locally

You can run a data collection pipeline locally and then verify your new configuration.  You can achieve this in two ways.

#### 4.1 Run using config repo

The easiest option might be to just stay within the config repository. Follow the guidance in [building a collection locally](../Testing/Building-a-collection-locally)


#### 4.2 Run using collection-task repo

Clone the [collection-task](https://github.com/digital-land/collection-task) repo. 

Set the environment variables to values relevant to the collection and dataset you have added within the docker-compose.yaml file. Then run with Docker Compose using `make compose-up`

You should be able to run `make datasette` and then see a local datasette version with the new dataset on it.

#### Notes

> Tip: When running make datasette and it returns that there is no SQL file, make sure that the corresponding collection in config has an endpoint and source, else the database for it will not be set up!

 > You’ll want to check the amount of records created in the dataset, this really should be equal to the amount of entries in the raw dataset. Also check the issues table for anything that sticks out and is fixable on our end

Once you're happy with the configuration for the new collection and new dataset, have it reviewed by a colleague and then merged.


### 5. Update Specification

Next, update the collection name for the dataset in the [specification](https://github.com/digital-land/specification) repository. Navigate to specification -> content -> dataset, locate the .md file corresponding to the dataset being added, and insert the relevant collection name. This step ensures that the DAG for this collection is created in Airflow.

### 6. Regenerate Airflow DAGs

Finally, you'll need to ensure the [DAGs for Airflow](https://github.com/digital-land/airflow-dags/) are re-published to AWS.  To do this, simply follow the instructions below.   Publishing the DAGs is necessary since the latest specification needs to be read to have the relevant collection DAGs created.

####  Re-publish DAGs

 1. If you have any DAG configuration changes to make within the airflow-dags repo, raise your changes as a pull request.  Seek approval and have it merged.

 1. When you're ready to publish DAGs to AWS, run the [GitHub Action to publish DAGs](https://github.com/digital-land/airflow-dags/actions/workflows/deploy.yml). After the GitHub Action has run, you'll be able to verify the collection is present via the [Airflow UI](/data-operations-manual/Explanation/Key-Concepts/Airflow-and-DAGs/#airflow-ui).

#### Verify new collection present

If the collection is present, you should be able to execute it and view details of the last execution, e.g.
   ![Airflow DAG last execution](/images/data-operations-manual/airflow-dag-last-execution.png)

You should be able to verify that the collection is included in the trigger-collection-dags-manual DAG, e.g.

![Airflow Trigger Collection DAGs - Manual](/images/data-operations-manual/airflow-trigger-collection-dags-manual.png)

If the collection is selected for schedule, then it should also be present within the trigger-collection-dags-scheduled DAG, e.g.

![Airflow Trigger Collection DAGs - Scheduled](/images/data-operations-manual/airflow-trigger-collection-dags-scheduled.png)

First, execute the collection in the [Airflow development environment](https://pipelines.development.planning.data.gov.uk/home) to identify any potential issues early. This helps prevent failures when deploying to production.

If the run was successful, there will be a green box next to the newly run workflow. If it was unsuccessful, check the logs to find out what the issue was or reach out to the infrastructure team for assistance.

Next, execute the collection in the [Airflow staging environment](https://pipelines.staging.planning.data.gov.uk/home). If the run is successful, share the [Planning Data staging URL](https://www.staging.planning.data.gov.uk/) with Data Design team for review.

The collection will execute in production during the overnight run. If you don’t want the collection to run in production for any reason, disable the DAG for it in the [Airflow production environment](https://pipelines.planning.data.gov.uk/home).

> Tip: If, despite all this, the collection does not appear on datasette, try running the workflow again, or wait until the next cycle of digital-land-builder has run.
