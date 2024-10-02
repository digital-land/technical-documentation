# Add an endpoint

**Prerequisites:**

- Cloned  the [config repo](https://github.com/digital-land/config) by running `git clone [gitURL]` and updated it with `make init` in your virtual environment  
- Validated the data. If you haven’t done this yet, follow the steps in ‘[Validating an Endpoint](Validate-an-endpoint)’ before continuing. 

> [!NOTE]  
> The endpoint_checker will pre-populate some of the commands mentioned in the steps below, check the end of the notebook underneath ‘_scripting_’.


1. **Create an import file**  
   If you don’t already have an import.csv file in the root of the config file, simply create one with the command `touch import.csv`

1. **Add configurations**

   >[!TIP]  
   >Check the [Endpoint-edge-cases](Add-an-endpoint#Endpoint edge-cases) section below for guidance on how to handle configuration for some non-standard scenarios, like a single endpoint being used for multiple provisions, or an endpoint for the `tree` dataset with polygon instead of point geometry.

   1. **Populate the import file**

      The following columns need to be included in `import.csv`:

      * `endpoint-url` - the url that the collector needs to extract data from
      * `documentation-url` - a url on the provider's website which contains information about the data
      * `start-date` - the date that the collector should start from (this can be in the past)
      * `plugins` - if a plugin is required to extract that data then it can be noted here otherwise leave blank
      * `pipelines` - the pipelines that need to be ran on resources collected from this endpoint. These are equivalent to the datasets and where more than one is necessary they should be separated by `;`
      * `organisation` - the organisation which the endpoint belongs to. The name should be in [this list](https://datasette.planning.data.gov.uk/digital-land/organisation)
      * `licence` - the type of licence the data is published with. This can usually be found at the dataset's documentation url.

      The endpoint checker should output text you can copy into `import.csv` with the required headers and values, or alternatively copy the headers below:

      ```
      organisation,endpoint-url,documentation-url,start-date,pipelines,plugin,licence
      ```

      Using the same example from [validating an endpoint](Validate-an-endpoint), the `import.csv` should look like this:  
         
      ```
      organisation,documentation-url,endpoint-url,start-date,pipelines,plugin,licence
      local-authority-eng:SAW,https://www.sandwell.gov.uk/downloads/download/868/article-4-directions-planning-data,https://www.sandwell.gov.uk/downloads/file/2894/article-4-direction-dataset,,article-4-direction,,ogl3
      ```


   1. **Make changes to pipeline configuration files**  

      Use the [how to configure an endpoint guide](Configure-an-endpoint) to see how each of the configuration files works.

      The most common step here will be using `column.csv` to add in extra column mappings.


1. **Run add_endpoint_and_lookups script**  
   Run the following command inside the config repository within the virtual environmen:

   ```
   digital-land add-endpoints-and-lookups [INPUT-CSV-PATH] [COLLECTION_NAME] -c ./collection/[COLLECTION_NAME] -p ./pipeline/[COLLECTION_NAME]
   ```

   The completed command will be given in the _scripting_ section of the endpoint_checker.

   For example (the actual command will vary based on the dataset added, article-4-direction is used as an example):

   ```
   digital-land add-endpoints-and-lookups ./import.csv article-4-direction -c./collection/article-4-direction -p ./pipeline/article-4-direction

   ```

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
   Once the changes have been made and pushed, checkout the relevant collections repository i.e., if the data added was conservation-area, checkout the conversation-area collection repository. Run the pipeline in the collection repo by running `make`. After the pipeline has finished running, use `make datasette` to interrogate the local datasets; this will enable you to check that the data is on the local platform as expected. In `lookups`, check if the entities added in the lookup.csv in step 4 are there.  

1. **Push changes**  
   Use git to push changes up to the repository, each night when the collection runs the files are downloaded from here. It is a good idea to name the commit after the organisation you are importing.  

1. **Run action workflow (optional)**  
   Optionally, you can run the overnight workflow yourself if you don’t want to wait until the next day to check if the data is actually on the platform. Navigate to the corresponding collection’s repository actions page e.g. [article-4-direction-collection](https://github.com/digital-land/article-4-direction-collection/actions) and under ‘Call Collection Run’, run the workflow manually. Depending on the collection, this can take a while but after it has finished running you can check on datasette if the data is on the platform.


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

At times, the endpoints we receive might include Tree and TPZ data. In cases like these, we need to add to the `filter.csv` file in the `tree-preservation-order pipeline`. The filter works based on the `tree-preservation-zone-type` pattern. Any data that corresponds to an `Area` pattern relates to a TPZ while data corresponding to an `Individual` pattern relates to a Tree.

For example:
```
tree-preservation-zone,28cff16a15892b5d99e0fbdb99921bf1cfce6ac4a72017c54c012c4c07378169,tree-preservation-zone-type,Area,,,,,
tree,28cff16a15892b5d99e0fbdb99921bf1cfce6ac4a72017c54c012c4c07378169,tree-preservation-zone-type,Individual,,,,,
```
To find out whether there are multiple datasets in an endpoint, look at the raw data by searching for tree-preservation-zone-type. Based on the value, it will either belong to TPZ or tree.

### Tree data with polygon instead of point

By default, the tree dataset `wkt` field (which is the incoming geometry from the resource) is mapped to `point`, with by a global mapping in `column.csv`. When a provider gives us a `polygon` data instead of a `point`, we need to add a mapping in the `column.csv`file for the specific endpoint or resource from `wkt` to `geometry` which will override the default mapping.

For example:
```
tree,422e2a9f2fb1d809d8849e05556aa7c232060673c1cc51d84bcf9bb586d5de52,,WKT,geometry,,,
```

As an example, this [datasette query](https://datasette.planning.data.gov.uk/digital-land/column_field?_sort=rowid&resource__exact=0889c8a96914abc22521f738a6cbad7b104ccff6256118a0a39bf94912cb38d4) shows a resource where we were provided a `polygon` dataset for tree so we mapped `wkt` to `geometry`.
Whereas [this](https://datasette.planning.data.gov.uk/digital-land/column_field?resource=05182443ad8ea72ec17fd2f46dd6e19126e86ddbc2d5f386bb2dab8b5f922d49) one was a `point` format so we did not need to override the mapping. You’ll notice that the field related to the column `wkt` is point.