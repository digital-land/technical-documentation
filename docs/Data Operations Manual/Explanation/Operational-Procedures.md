
One of the key responsibilities of the data management team is adding new endpoints and keeping existing ones up to date. This page gives an overview of the important concepts behind the procedures we follow at different stages of the data lifecycle.

These procedures can vary based on whether a dataset is national or compiled, whether the data provider publishes updates to the same endpoint or a completely new one, and what sort of update has been made to an endpoint.

To help with this complexity, we've got a few levels of documentation to help: 

1. This explanatory overview is at the highest level. 
2. Below that, the tutorials section covers a range of different scenarios that can occur when [adding](Adding-Data) and [maintaining](Maintaining-Data) data and explain the procedure that should be followed in each one. 
3. The procedure steps in the scenarios link to the most detailed level of documentation - the [how-to guides](How-to-guides) - which give step by step instructions for how to complete particular tasks.

## Validating data

When receiving data from the LPA, we need to first validate the data to check that it conforms to our data requirements.

Depending on the dataset, the LPAs usually use the [planning form](https://submit.planning.data.gov.uk/check/) to check if the data is good to go. They don't do that all the time though, so we still need to manually validate the data. However, the check tool does not yet work for Brownfield-land/site datasets so we always need to validate the data on our end.

Read the [how to validate an endpoint guide](Validate-an-endpoint) to see the steps we follow.


## Adding data
There are two main scenarios for adding data:

- Adding an endpoint for a new dataset and/or collection (e.g. we don't have a the dataset on file at all)
- Adding a new endpoint to an existing dataset

Based on this, the process is slightly different.

A how-to on adding a new dataset and collection can be found [here](Add-a-new-dataset-and-collection).

A how-to on adding a new endpoint to an existing dataset can be found [here](Add-an-endpoint). Endpoints can come in a variety of types. The format can differ from endpoint to endpoint as can the required plugins needed to process the endpoint correctly.

More information on types can be found [here](Endpoint-URL-Types-And-Plugins#data-formats-of-resources-that-can-be-processed)

More information on plugins can be found [here](Endpoint-URL-Types-And-Plugins#adding-query-parameters-to-arcgis-server-urls)

## Maintaining data

Maintaining data means making sure that the changes a data provider makes to their data are reflected on the platform, which might be done either by adding new endpoints or managing updates by the provider to existing ones. 

### Assigning entities
All entries on the platform must be assigned an entity number in the `lookup.csv` for the collection. This usually happens automatically when adding a new endpoint through the `add-endpoints-and-lookups` script. However, when an endpoint is already on the platform but the LPA has indicated that the endpoint has been updated with a new resource and new entries, we can’t just re-add the endpoint. Instead, we assign the new entries their entity numbers differently.

A how-to on assigning entities can be found [here](Assign-entities)

### Merging entities

There can be duplicates present in a dataset. This primarily takes place where multiple organisations are providing data against the same object (or entity). We do not automatically detect and remove these, the old-entity table is used to highlight these duplications and provide them under a single entity number.

A how-to on merging entities can be found [here](Merge-entities)

## Retiring data

### Retiring endpoints
When an endpoint consistently fails, or LPAs give us a different endpoint (as opposed to the one we already have) to retrieve the data, we need to retire the old/failing endpoint. It is important to understand that while we retire an endpoint, this does not mean that the data associated with it will be retired as well. This only makes it so that the collector stops collecting new resources (data) from the endpoint. The data that has been retrieved previously from that endpoint will still be on the platform and will still be used.

When we retire an endpoint, we also need to retire the source(s) associated with it as sources are dependent on endpoints.

Read [how-to retire an endpoint](Retire-endpoints) to learn more.

### Retiring resources

It won’t be necessary to do this step often, however, sometimes a resource should not continue to be processed and included in the platform. This can be for multiple reasons, and in most cases will occur when it has been found that the resource contains significant errors.


A how-to on retiring resources can be found [here](Retire-resources)

### Retiring entities

**Note:** We may want to keep old entities on our platform as historical data. There are two reasons an entity might be removed:

1. It was added in error. In this case, we should remove it from our system.  
2. It has been stopped for some reason. In this scenario, we should retain the entity.  
Ideally, we would mark such entities with end-dates to indicate they have been stopped, but implementing this requires additional work.

For example, a World Heritage Site was added as an entity to our platform. Although it is no longer a World Heritage Site, we want to retain the entity to indicate that it held this status during a specific period.

In a given scenario, determine the reason why the entities are no longer present.  
Check with Swati before deleting entities.