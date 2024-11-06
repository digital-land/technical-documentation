# Add an endpoint

**Prerequisites:**

- Clone the [config repo](https://github.com/digital-land/config) by running `git clone [gitURL]` and update it with `make init` in your virtual environment
- Validate the data. If you haven’t done this yet, follow the steps in ‘[Validating an Endpoint](../../Validating/Validate-an-endpoint)’ before continuing.

> **NOTE!**  
> The endpoint*checker will pre-populate some of the commands mentioned in the steps below, check the end of the notebook underneath ‘\_scripting*’.

1. **Create an import file**  
   If you don’t already have an import.csv file in the root of the config file, simply create one with the command `touch import.csv`

1. **Add configurations**

   > **NOTE!**  
   > Check the [Endpoint-edge-cases](https://digital-land.github.io/technical-documentation/data-operations-manual/How-To-Guides/Adding/Add-an-endpoint/#endpoint-edge-cases) section below for guidance on how to handle configuration for some non-standard scenarios, like a single endpoint being used for multiple provisions, or an endpoint for the `tree` dataset with polygon instead of point geometry.

   1. **Populate the import file**

      The following columns need to be included in `import.csv`:

      - `endpoint-url` - the url that the collector needs to extract data from
      - `documentation-url` - a url on the provider's website which contains information about the data
      - `start-date` - the date that the collector should start from (this can be in the past)
      - `plugins` - if a plugin is required to extract that data then it can be noted here otherwise leave blank
      - `pipelines` - the pipelines that need to be ran on resources collected from this endpoint. These are equivalent to the datasets and where more than one is necessary they should be separated by `;`
      - `organisation` - the organisation which the endpoint belongs to. The name should be in [this list](https://datasette.planning.data.gov.uk/digital-land/organisation)
      - `licence` - the type of licence the data is published with. This can usually be found at the dataset's documentation url.

      The endpoint checker should output text you can copy into `import.csv` with the required headers and values, or alternatively copy the headers below:

      ```
      organisation,endpoint-url,documentation-url,start-date,pipelines,plugin,licence
      ```

      Using the same example from [validating an endpoint](../../Validating//Validate-an-endpoint), the `import.csv` should look like this:

      ```
      organisation,documentation-url,endpoint-url,start-date,pipelines,plugin,licence
      local-authority-eng:SAW,https://www.sandwell.gov.uk/downloads/download/868/article-4-directions-planning-data,https://www.sandwell.gov.uk/downloads/file/2894/article-4-direction-dataset,,article-4-direction,,ogl3
      ```

   1. **Make changes to pipeline configuration files**

      Use the [how to configure an endpoint guide](../Configure-an-endpoint) to see how each of the configuration files works.

      The most common step here will be using `column.csv` to add in extra column mappings.

1. **Run add_endpoint_and_lookups script**  
   Run the following command inside the config repository within the virtual environment:

   ```
   digital-land add-endpoints-and-lookups [INPUT-CSV-PATH] [COLLECTION_NAME] -c ./collection/[COLLECTION_NAME] -p ./pipeline/[COLLECTION_NAME]
   ```

   The completed command will be given in the _scripting_ section of the endpoint_checker.

   For example (the actual command will vary based on the dataset added, article-4-direction is used as an example):

   ```
   digital-land add-endpoints-and-lookups ./import.csv article-4-direction -c./collection/article-4-direction -p ./pipeline/article-4-direction

   ```

   **Improved Method:**
   This method defines the required prerequisite parameters for us.

   Syntax
   ```
   make add-data COLLECTION=[COLLECTION_NAME] INPUT_CSV=[INPUT_FILE]
   ```

   For example
   ```
   make add-data COLLECTION=conservation-area INPUT_CSV=import.csv
   ```

1. **(Optiona) Update entity-organisation.csv**  

   If the data that has been added is part of the `conservation-area` collection e.g `conservation-area` and `conservation-area-document`, the entity range must be added as a new row. This is done using the entities generated in `lookup`. Use the first and the last of the entity numbers of the newly generated lookups e.g if `44012346` is the first and `44012370` the last, use these as `entity-minimum` and `entity-maximum`.

   For an explanation of how the file works, see [entity-organisation](Configure-an-endpoint.md).




1. **Check results**  
   After running the command, the endpoint.csv, lookup.csv, and source.csv should be modified.

   - A new line should be added to endpoint.csv and source.csv.
   - For each new lookup, a new line should be added to the lookup.csv.  
     The console output will show a list of new lookups entries organised by organisation and resource-hash. Seeing this is a good indication that the command ran successfully.
     For example:

   ```
   ----------------------------------------------------------------------
   >>> organisations:['local-authority-eng:SAW']
   >>> resource:2b142efd3bcfe29660a3b912c4f742b9c7ff31c8ca0a02d93c9aa8b60e8e2469
   ----------------------------------------------------------------------
   article-4-direction,,local-authority-eng:SAW,A4D1,6100323
   article-4-direction,,local-authority-eng:SAW,A4D2,6100324
   ...
   ```

1. **Test locally**  
   Once the changes have been made and pushed, the next step is to test locally if the changes have the desired effect. 
   Testing can be done from the `config` repo. Testing the entire collection can take a while so it's quicker focussing on only the newly added endpoint data.

   1. In the dataset's `collection` folder, edit all the csv files to only include the newest record, everything else should be removed. So `endpoints.csv` and `source.csv` should only have the headers and the newly added endpoints/sources. `old-resource.csv` should be empty (unless the change was retiring a resource). Remove the `resource.csv` and `log.csv` as well as the samely named folders (with everything in it)

   2. In the dataset's `pipeline` folder, anything targetting another resource/endpoint should be removed. This includes files the following files `[column.csv, combine.csv, old-entity.csv, and patch.csv]`. This is done to ensure that no errors will appear during the collection and transformation of the resource as well as the creation of the sql database.
   
   3. Run the pipeline in the collection repo by running `make COLLECTION=collection_name` e.g. `make COLLECTION=brownfield-land`.

   4. After the pipeline has finished running, use `make datasette COLLECTION=collection-name` to interrogate the local datasets; this will enable you to check that the data is on the local platform as expected. Check that the expected data is there and no issues that are unexpected show up.

   >**NOTE!**  
   >If testing the entire collection is required, only removing the folders and files in step 1 are required. Since downloading each resource inividually will take hours, it is best to run the the entire process run in parallel. This can be done by adding `-j 16` to the command e.g `make -j 16 COLLECTION=collection_name`. The -j option specifies the number of jobs (commands) to run simultaneously during the process. The more cores your machine has, the higher the number (or lower) the number can be i.e. `-8` or `-32`.


1. **Push changes**  
   Use git to push changes up to the repository, each night when the collection runs the files are downloaded from here. It is a good idea to name the commit after the organisation you are importing.

1. **Run action workflow (optional)**  
   Optionally, you can manually execute the workflow that usually runs overnight yourself - if you don’t want to wait until the next day - to check if the data is actually on the platform. Simply follow the instructions in the [guide for triggering a collection manually](/data-operations-manual/How-To-Guides/Maintaining/Trigger-collection-manually).

## Endpoint edge-cases

### Handling Combined Endpoints

Note that, when adding an endpoint that feeds into separate datasets or pipelines (such as an endpoint with data for _tree-preservation-zone_ and _tree)_, the pipeline field in the import.csv file should be formatted to contains both datasets as follows:

```
pipelines
tree-preservation-zone;tree
```

When handling this type of endpoint, two possible scenarios may arise.

1. The endpoint includes two datasets: one spatial and one non-spatial \- It may be necessary to use separate columns as a reference field for each dataset. In such cases, add a column mapping for each dataset contained within the endpoint in the column.csv file.

2. The endpoint includes two datasets both being spatial \- For scenarios where the endpoint includes a column that determines the dataset, use the filter.csv file. Follow the instructions in ‘[TPZ and Tree data in the same endpoint](#tpz-and-tree-data-in-same-endpoint)’ for this scenario.

### TPZ and Tree data in the same endoint

We might receive an endpoint that contains both Tree and TPZ data. When this happens we can usually use a `filter.csv` configuration to process a subset of the endpoint data for each dataset. Data supplied like this should have a `tree-preservation-zone-type` field for the TPZ data, which should contain one of `area`, `woodland` or `group` for TPZs and `individual` for trees.

>**NOTE!**  
>`filter.csv` config for a dataset will only work with a field that is in the dataset schema, and the `tree-preservation-zone-type` is not in the `tree` schema. So if you need to filter tree data using this field, it will first need to be mapped to a field in the `tree` schema that can then be used by `filter.csv`. You can use the `tree-preservation-order-tree` field (which isn't in the website guidance or tech spec, but is in the [specification repo spec](https://github.com/digital-land/specification/blob/main/content/dataset/tree.md)), like this [example in column.csv](https://github.com/digital-land/config/blob/main/pipeline/tree-preservation-order/column.csv#L201).


For example:

`column.csv` config
```
dataset,endpoint,resource,column,field,start-date,end-date,entry-date
tree,d6abdbc3123bc4b60ee9d34ab1ec52dda34d67e6260802df6a944a5f7d09352b,,tree_preservation_zone_type,tree-preservation-order-tree,,,
```

`filter.csv` config
```
dataset,resource,field,pattern,entry-number,start-date,end-date,entry-date,endpoint
tree-preservation-zone,,tree-preservation-zone-type,(?!Individual),,,,,d6abdbc3123bc4b60ee9d34ab1ec52dda34d67e6260802df6a944a5f7d09352b
tree,,tree-preservation-order-tree,Individual,,,,,d6abdbc3123bc4b60ee9d34ab1ec52dda34d67e6260802df6a944a5f7d09352b
```


### Tree data with polygon instead of point

By default, the tree dataset `wkt` field (which is the incoming geometry from the resource) is mapped to `point`, with by a global mapping in `column.csv`. When a provider gives us a `polygon` data instead of a `point`, we need to add a mapping in the `column.csv`file for the specific endpoint or resource from `wkt` to `geometry` which will override the default mapping.

For example:

```
tree,422e2a9f2fb1d809d8849e05556aa7c232060673c1cc51d84bcf9bb586d5de52,,WKT,geometry,,,
```

As an example, this [datasette query](https://datasette.planning.data.gov.uk/digital-land/column_field?_sort=rowid&resource__exact=0889c8a96914abc22521f738a6cbad7b104ccff6256118a0a39bf94912cb38d4) shows a resource where we were provided a `polygon` dataset for tree so we mapped `wkt` to `geometry`.
Whereas [this](https://datasette.planning.data.gov.uk/digital-land/column_field?resource=05182443ad8ea72ec17fd2f46dd6e19126e86ddbc2d5f386bb2dab8b5f922d49) one was a `point` format so we did not need to override the mapping. You’ll notice that the field related to the column `wkt` is point.
