# Validating an endpoint

1. **Check required information is available**  
   Before we can continue with anything, we need to make sure that we have the following information: _the organisation, the endpoint_url, the documentation_url,_ and _the licence_. If even one of them is missing, we can’t continue with the process and require the LPA to give us the correct information.

   There are certain fields that we require to be in the data (while some fields are required in all datasets, additional fields might be required depending on the dataset). In the first instance, this is what we check. _If any other fields are present, the data should still be added. Any fields that are missing should be reported in the provided [feedback form](https://drive.google.com/drive/folders/1YEKupdAVcdCt6YVG6NC3iUftAsQhk9Zq)._

   We don’t need to do this manually, instead, we can use [_CHECK_](https://check.staging.digital-land.info/) or the [_endpoint_checker_](https://github.com/digital-land/jupyter-analysis/blob/main/endpoint_checker/endpoint_checker.ipynb). The endpoint checker is the most up to date and trustworthy check we have at the moment, so use it in most cases. CHECK is just a quick and easier way to find out if there is something wrong with the data but just because it does not flag anything up does not mean that the data is perfect. It also does not work for brownfield data. Hence we use the endpoint checker.

2. **Update endpoint checker variables**  
   The endpoint checker works as follows:  
   In most cases, we just need to add the correct _collection_name_, _dataset_, _organisation, endpoint_url, documentation_url, and licence_. The script will perform a variety of checks.
   _The endpoint checker works by running the pipeline on the given endpoint to check if it will be successful while also highlighting useful information as a summary as to whether the endpoint would be successful on our platform. It essentially downloads the resource through the endpoint and attempts to run the pipeline locally. It checks:_

- _Can the resource be downloaded successfully?_
- _Are there any unassigned entities? (If so, these are what will later be added in the `lookup.csv`)_
- _Checks if the column mapping was done correctly (If, in this stage, a particular column is empty or has missing values, the column mapping likely needs investigating)_
- _Checks if there are any issues ( internal issues with an ‘error’ severity need to be fixed before moving on)_
- _Checks for duplicate entities between current database and new endpoint entities_
  - _Any entities that are duplicates, we need to merge them (check merge entities section for this)_

The correct variables need to be provided to the endpoint checker in order for it to work. The following is an example of updated variables:

```
collection_name = 'article-4-direction-collection'
dataset = 'article-4-direction'
organisation = 'local-authority-eng:SAW'
endpoint_url = 'https://www.sandwell.gov.uk/downloads/file/2894/article-4-direction-dataset'
documentation_url = "https://www.sandwell.gov.uk/downloads/download/868/article-4-directions-planning-data"
start_date=""
plugin = ''
licence = "ogl3"
reference_column = ""
additional_column_mappings=None
additional_concats=None
data_dir = '../data/endpoint_checker'
```

In most cases, the only variables that need to be changed are _collection-name, dataset, organisation, enpoint_url, documentation_url,_ and _licence_.

**Cases when to use other variables:**  
 Certain endpoint_urls types might require a plugin \[I don’t know which ones, ask later\]. The required licence will be indicated in the documentation_url. At times, additional column mappings need to be done. This is the case when the headers in the data we have been provided do not match the headers we need. Here we are mapping the provided `fid` to our `reference` field.

```
additional_column_mappings=[{'dataset':'conservation-area','endpoint':'6dad8060cbdf75cf7c28c511b107a367e7c0435e04d130793b8464454bfd384c','column' : 'fid', 'field':'reference'}]
```

If additional_concats needs to be used, it can be used like so \[again, unsure of when this is actually used\]:

```
additional_concats = [{
    'dataset':'tree-preservation-zone',
    'endpoint':'de1eb90a8b037292ef8ae14bfabd1184847ef99b7c6296bb6e75379e6c1f9572',
    'resource':'e6b0ccaf9b50a7f57a543484fd291dbe43f52a6231b681c3a7cc5e35a6aba254',
    'field':'reference',
    'fields':'REFVAL;LABEL',
    'separator':'/'
}]
```

3. **Check for issues at ‘Issues Logs’**  
   Make sure there are no internal errors showing up. If they do, these need to be fixed before continuing. The fix depends on the error warning. It could be a simple one that can be fixed with some mapping.

4. **Check for duplicates at ‘Duplicates with different entity numbers’**  
   If there are duplicates printed out, and the duplicates have different entity numbers, then you will need to merge these duplicates after adding the endpoint. Follow the instructions in [Merging Entities](../../Maintaining/Merge-entities) for this.

5. **Check for unique counts in ‘Duplicate Values in Reference Columns’**  
   In the printed out table, the amount of _nunique_ must be the same as _count_ and _size_. This tells us that all the data is unique. If they are not unique, we need to get back to the LPA and require them to update their endpoint to only have unique references.
   In an ideal world, no issues will be flagged up. This means that:

- Unassigned entities will be listed out
- The final dataset will be shown
- The amount of unique rows will be equal to the number of rows in the dataset
  If everything worked correctly, we will have successfully validated the data and can now move on to adding the data. This is done by adding to the endpoint, source, and lookup files. More on that in the [Adding an Endpoint](../../Adding/Add-an-endpoint) step.
