# Add a new dataset and collection

The following instructions are for when adding an entirely new dataset to the platform which does not have a corresponding collection repo.

If you’re adding a new dataset to an existing collection you can follow the same process, but ignore steps 2 and 3.

#### 1. Ensure the collection is noted in the dataset specification

Not doing this won't result in any specific errors but it should be done to ensure that the list of collections in the specification is up to date. 

Go to https://github.com/digital-land/specification/tree/main/content/dataset and check if there is a .md file for your new dataset 

E.g., if you plan to add a dataset named article-4-direction you want to check that https://github.com/digital-land/specification/tree/main/content/dataset/article-4-direction.md exists. That’s all!

If it doesn’t exist, raise this issue with the Data Design team and they should be able to set it up.

#### 2. Create the new collection repo 
Next, you will need to create a new collection repo named after the dataset you wish to add. This can be easily done with the collection-template repo found here (https://github.com/digital-land/collection-template).	Select Use this template at the top right to be redirected to the repo creation page. When creating the repo, make sure to set the owner as digital-land and set the visibility to public. 

 IMPORTANT: The name of the collection repo must end with "-collection". For example, for  the "article-4-direction" dataset, it would need to be called article-4-direction-collection. Failing to do this will cause issues in the pipeline.

#### 3. Create Collection and Pipeline folders in the [config repo](https://github.com/digital-land/config)

Next, you’ll want to make sure your local config main is up to date with the remote main. Then create a new branch. The [config repo](https://github.com/digital-land/config) currently contains collection and pipeline folders for each unique collection held within the pipeline. In this case, there won’t be one for the new collection.
You need to create new folders ( `collection` and `pipeline`) and the required files within those folders for the collection that needs to be created. There is a really handy script for this step, simply run create_collection.py like so: 
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
  * filter.csv
  * lookup.csv
  * old-entity.csv
  * patch.csv
  * skip.csv
  * transform.csv



#### 5. Add endpoint(s) for the new dataset (optionally mapping and default values,)
In case a column-field mapping was provided, you’ll need to add the mapping to column.csv. Make sure to map to the correct data, we want to map some column to its equivalent `field` e.g the dataset might have a different name for the reference so we need to map this to our `reference` field.

In case there is a defaultValue given for a field in the schema, we want to add this to the default-value.csv.

Follow steps 3 and 4 in ‘Adding an Endpoint’ for instructions on adding mapping and default values.

Next, you can just proceed to add an endpoint. Validating the data through the endpoint checker will not work at this point but we can manually check whether the endpoint_url and documentation_url work as well as whether the required fields specified in the schema are present.   There will be no further need to validate it. Once the PR is merged, you can go to the next step.

### 6. Test locally

Clone the collection repo you created in step 2. Create a virtual environment with the following command
 python3 -m venv --prompt . .venv --clear --upgrade-deps

You then need to update the collection with the dataset with the following commands:
* make makerules
* make init
* make collect
* make


If everything is done correctly, you should be able to run `make datasette` and then see a local datasette version with the new dataset on it.

> Tip: When running make datasette and it returns that there is no sql file, make sure that the corresponding collection in config has an endpoint and source, else the database for it will not be set up!

 > You’ll want to check the amount of records created in the dataset, this really should be equal to the amount of entries in the raw dataset. Also check the issues table for anything that sticks out and is fixable on our end

### 7. Update run.yml

Finally, you need to uncomment the cron in the collection repo’s run.yml file found in .github/workflows. It should look like this:
````
name: Call Collection Run
on:
  schedule:
    - cron: 0 0 * * *
  workflow_dispatch: null
jobs:
  call-workflow:
    uses: digital-land/collection-template/.github/workflows/callable_run.yml@main
    secrets: inherit
````
Then run the workflow. To run the workflow, go to Actions -> Call Collection Run -> Run workflow on main.


If the run was successful , there will be a green tick next to the newly run action. If it was unsuccessful, check the logs to find out what the issue was. 

### 8. Update specification

Once the workdlow has run successfully, all that is needed is to add the collection name to the specification. The specification currently should be empty. Change it. So `collection: '' ` should be changed to `collection: '[COLLECTION_NAME]'`.

Once the change has merged, you’re all done!

> Tip: If, despite all this, the collection does not appear on datasette, try running the workflow again, or wait until the next cycle of digital-land-builder has run.
