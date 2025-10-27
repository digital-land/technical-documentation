# Transform

The transform process take a resource and given a dataset name processes that resource against the dataset. This uses a set of configuration files and the specification files which instruct the process what to do.

the outputted file contains each  fact and where they've come from. Along side the file seveal logs  are also outputted that  tell us what happened during the transformation process

![Transform Process](/images/processes/transfom.drawio.png)

There is a huge nummber of inputs equired for this step. There may be some oppertunity to implify these inputs in the future:


- specification_dir - a directory containing the specification, this is used to access dataset information
- pipeline_dir - a directoy containing the pipeline configuration files. these allow specific configuations to be applied to a resource.
- dataset_resource_dir - a directory to store the dataset_resource log.
- column_field_dir - a directory  to store the column field log fo the processed resource
- conveted_resource_dir - a directory to store logs of the convert phase.
- output_log_dir - a start of unifying all of the logs into a single directory. used to put  the opeational issue log at the moment. should look at moving all logs to a system like this.
- cache_dir - a temporarry directory where intermediate files can be stored otherwise a temp directory is used. the temp directorry doesn't always play well on eveybody's system.
- config_path - the begining of moving config files into a sqlite database instead of from a directory of files. 
- input_path - the path to the file that needs transforming

The outputs are as follows:
- <resource>.csv (from output_path) - the  main output  containing each fact and where  it was in the resource  
- resource.csv - an updated resouce.csv which contains any new rersources gathered in more recent logs as well as updating old resources with any changed information in the  source or endpoint csvs

the outputs from the second step

- pipeline.mk - a file that can be used by make to process all resources and create dataset sqlite files

## digital-land-python

the plan process uses a small amount of code from digital land python repo. The two commands are found in the `commands.py` file. [`collection_save_csv`](https://github.com/digital-land/digital-land-python/blob/4a52c75b57d2c9a87e34989f3ae930ab9a7090fe/digital_land/commands.py#L129) and [collection_pipeline_makerules](https://github.com/digital-land/digital-land-python/blob/4a52c75b57d2c9a87e34989f3ae930ab9a7090fe/digital_land/commands.py#L110)


The commands offer functional ways of building the required files but the heavy  lifting is done by  the [`Collection`](https://github.com/digital-land/digital-land-python/blob/4a52c75b57d2c9a87e34989f3ae930ab9a7090fe/digital_land/collection.py#L328) class found in in [`collection.py`](https://github.com/digital-land/digital-land-python/blob/main/digital_land/collection.py).

## Batch Implementation

This process is run as part of our data collection pipelines.

they are ran during a task in our collection dags in airflow. The file generating these dags can be found [here](https://github.com/digital-land/airflow-dags).

The airflow triggers an ECS task in fargate and uses the [collection-task repository](https://github.com/digital-land/collection-task)

the script for all procesess ran in the ECS Task is [`run.sh`](https://github.com/digital-land/collection-task/blob/104df85861401d6088728039792a75038ee580ca/task/run.sh#L27)

In that script the `make collection` target is used which leads
to the digital-land clis:

`digital-land ${DIGITAL_LAND_OPTS} collection-save-csv --collection-dir $(COLLECTION_DIR) --refill-todays-logs $(REFILL_TODAYS_LOGS)`

`digital-land ${DIGITAL_LAND_OPTS} collection-pipeline-makerules --collection-dir $(COLLECTION_DIR) --specification-dir $(SPECIFICATION_DIR) --pipeline-dir $(PIPELINE_DIR) --resource-dir $(COLLECTION_DIR)resource/ --incremental-loading-override $(INCREMENTAL_LOADING_OVERRIDE) > $(COLLECTION_DIR)pipeline.mk;`

The arguement options are passed in by setting environment variables. defaults are chosen via make if not set.

Once complete results are pushed to s3 and saved using another make target