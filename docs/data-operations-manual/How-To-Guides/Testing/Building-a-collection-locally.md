# Building a collection locally

Before we commit any changes to main, we need to be sure that the changes have the desired effect. To do this, we build a datasette database locally for any collection.

Testing can be done from the `config` repo. Testing the entire collection can take a while so it's quicker focussing on only the newly added endpoint data.

> **NOTE!**  
> This assumes you have the collection setup. If not, simple run the commands `make makerules COLLECTION=[collection_name]` and `make init COLLECTION=[collection_name]`

1. In the dataset's `collection` folder, edit all the csv files to only include the newest record, everything else should be removed. So `endpoints.csv` and `source.csv` should only have the headers and the newly added endpoints/sources. `old-resource.csv` should be empty (unless the change was retiring a resource). Remove the `resource.csv` and `log.csv` as well as the samely named folders (with everything in it) as these can sometimes cause errors.

2. In the dataset's `pipeline` folder, anything targetting another resource/endpoint should be removed. This includes the following files `[column.csv, combine.csv, old-entity.csv, and patch.csv]`. This is done to ensure that no errors will appear during the collection and transformation of the resource as well as the creation of the sql database.

3. Run the pipeline in the collection repo by running `make COLLECTION=[collection_name]` e.g. `make COLLECTION=brownfield-land`.

4. After the pipeline has finished running, use `make datasette COLLECTION=[collection_name]` to interrogate the local datasets; this will enable you to check that the data is on the local platform as expected. Check that the expected data is there and no issues that are unexpected show up.

> **NOTE!**  
> If testing the entire collection is required, only removing the `resource` and `log` files and folders is required. To speed up the download process, it’s best to run the tasks in parallel, as downloading each resource individually could take hours for some of the larger datasets. You can achieve this by using the -j option with the make command, for example:
> `make -j 16 COLLECTION=[collection_name]`
> The -j option specifies the number of jobs (commands) to run concurrently. The higher the number, the more tasks will run at the same time, which can significantly speed up the process. You can adjust this number depending on the number of CPU cores available on your machine. For example, if your machine has 8 cores, you could use `-j 8`; for 16 cores, you might try `-j 16`.

> **Test and rebuild quicker!**  
> Sometimes it might be necessary to test multiple times to get the right configuration down. To make this easier and quicker, `make clobber COLLECTION=[collection_name]` can be used. This keeps the downloaded resources but removes all the logs.