## Pipeline configuration 

Configuration files control where data is collected from and how data is transformed from resources into the fact and entity model described above. Each collection has its own set of configuration files organised into two folders: `collection` and `pipeline`. 

Each configuration file in `pipeline` can be used to apply configurations to a particular dataset, endpoint, or resource in the collection by using the dataset name or endpoint/resource hash values in the corresponding fields of the configuration file. The `endpoint` and `resource` fields can be left blank to apply a configuration to all resources in a dataset (useful to set default configurations), or just the `resource` field left blank to apply a configuration to all resources from an endpoint.

E.g. this line below in the listed-building column.csv would apply a column re-mapping from `ListEntry` to `reference` for all endpoints and resources in the `listed-building` collection:

```
dataset,endpoint,resource,column,field,start-date,end-date,entry-date
listed-building,,,ListEntry,reference,,,

```

> [!NOTE] 
> In most cases we prefer configuration to be made against an endpoint rather than a resource, as this means that the configuration persists when an endpoint is updated and a new resource is created.

For more information on the configuration options read [How to configure an endpoint](../../How-To-Guides/Adding/Configure-an-endpoint)

