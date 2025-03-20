# Validating an endpoint

1. **Check required information is available**  
   In order to add an endpoint we require the following information: 
   
   * the organisation
   * the endpoint_url
   * the documentation_url
   * the licence
   
   If any are missing and they can't be worked out independently, then ask the LPA to give more information.

1. **Use check service to test whether the data matches the specifications**

   For ODP datasets the [Check Service](https://submit.planning.data.gov.uk/check/) will test most of the things we need. Select the required dataset and submit the endpoint URL to see the results.

   The service will tell you if there are issues which must be fixed before the data can be added. For any other issues it is ok to go ahead and add the data so that the provider can then fix issues and improve the quality over time.

   NOTE the check service:

   * does not work with WFS data
   * does not check for geometry duplicates in conservation-area data

   In these situations you should also use the endpoint checker (see steps below).

1. **(Optional) Use the endpoint checker to check for any issues**  
   
   > NOTE:   
   > This step should only be followed if you are validating a `conservation-area` endpoint, or if the Check service won't work for some reason.
   
   The endpoint checker works by downloading a resource from the endpoint and running the pipeline locally to check if it can be processed while also highlighting any other quality issues. It checks:

   - Can the resource be downloaded successfully?
   - Are there any unassigned entities? 
   - Checks if column mapping works correctly
   - Checks if there are any issues 
   - Checks for duplicate entities between current database and new endpoint entities

   To run the endpoint checker populate the key variables in the notebook, like in this example:

   ```
   # required
   collection_name = 'article-4-direction-collection'
   dataset = 'article-4-direction'
   organisation = 'local-authority-eng:SAW'
   endpoint_url = 'https://www.sandwell.gov.uk/downloads/file/2894/article-4-direction-dataset'
   documentation_url = "https://www.sandwell.gov.uk/downloads/download/868/article-4-directions-planning-data"
   licence = "ogl3"
   data_dir = '../data/endpoint_checker'
   
   # optional
   start_date= ""
   plugin = ""                        # "wfs" or "arcgis"
   reference_column = ""
   additional_column_mappings = None
   additional_concats = None
   ```

   **Cases when to use other variables:**  
   When the columns supplied don't match the fields in the data specifications they can be remapped using the `additional_column_mappings` variable, like so:

   ```
   additional_column_mappings=[{'dataset':'conservation-area','endpoint':'6dad8060cbdf75cf7c28c511b107a367e7c0435e04d130793b8464454bfd384c','column' : 'fid', 'field':'reference'}]
   ```

   Or concat config can be supplied with `additional_concats`, like below. (see [configure an endpoint](../Adding/Configure-an-endpoint.md) for an explanation.)

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

   Once the endpoint checker has run you can carry out the following checks.

   i. **Check for unassigned entities**  
      There should be the same number as the number of new records in the endpoint.

   ii. **Check the expected columns have been mapped**  
      After the "Check logs collated from the pipeline process" cell you'll see a printout of the columns that have been mapped. If there are any missing you should use the `additional_column_mappings` to test making additional mappings. You should map as many other fields as possible to the specifications.

   iii. **Check for issues at ‘Issues Logs’**  
      Make sure there are no internal errors showing up. If they do, these need to be fixed before continuing. The fix depends on the error warning. It could be a simple one that can be fixed with some mapping.

   iv. **Check for duplicates at ‘Duplicates with different entity numbers’**  
      If there are duplicates printed out, and the duplicates have different entity numbers, then you will need to merge these duplicates after running the `add-endpoint-and-lookups` command. This should be done by changing entity number of newly generated entity to the older entity it is a duplicate of.

   v. **Check for unique counts in ‘Duplicate Values in Reference Columns’**  
      In the printed out table, the amount of _nunique_ must be the same as _count_ and _size_. This tells us that all the data is unique. If they are not unique, we need to get back to the LPA and require them to update their endpoint to only have unique references.
   

Once the steps above have been followed you should be certain of the following:

* The endpoint contains the expected data
* The dataset has a unique `reference` field (or an equivalent which can be mapped to `reference`)
* Any other fields supplied which can be mapped to the specification
* Any error-level issues have been fixed
* *If it's a spatial dataset*, that it has a `geometry` field, or a `point` field in the case of `tree` data
* *If it's a conservation-area dataset*, whether it contains any spatial duplicates with existing datasets which will need to be merged

<br></br>

Now use the [adding an Endpoint](../../Adding/Add-an-endpoint) guide to add the data.
