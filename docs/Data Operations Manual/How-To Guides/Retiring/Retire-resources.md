
1. **Retrieve the resource hash**

   In order to retire a resource, we will need the resource hash. This can be found in a variety of ways on [datasette](https://datasette.planning.data.gov.uk/digital-land), some of the will be listed below:

- [`lookup`](https://datasette.planning.data.gov.uk/digital-land/lookup): If you know the reference or the entity number associated with the resource, you can find the resource hash by filtering for the data you have. However, in some cases, there might not be an entity or reference row with a resource associated for whatever reason. In this case, use another method.  
- [`resource_endpoint`](https://datasette.planning.data.gov.uk/digital-land/resource_endpoint): If you know the endpoint hash of the associated resource, you can find it here using the endpoint hash.  
- [`reporting_latest_endpoints`](https://datasette.planning.data.gov.uk/digital-land/reporting_latest_endpoints): If you know the endpoint hash or the endpoint\_url, you can use these to find the resource  
    
2. **Populate `old-resource.csv`:**  
   

Using the resource hash from step ,  add a new row in `old-resource.csv` located in the config repository. Each row will have the following columns:

* `old-resource` \- the resource hash you identified above  
* `status` \- for retiring a resource this should be 410  
* `resource` \- not needed for retiring an endpoint  
* `notes` \- details on why the resource should no longer be processed E.g., ‘Errors in resource’

The following assumes a resource hash *70100002871:*

```
7010002871,410,,new endpoint and reference field for GLO,,,
```
