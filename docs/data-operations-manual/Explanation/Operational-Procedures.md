# Operational Procedures

One of the key responsibilities of the data management team is adding new endpoints and keeping existing ones up to date. This page gives an overview of the important concepts behind the procedures we follow at different stages of the data lifecycle.

These procedures can vary based on whether a dataset is national or compiled, whether the data provider publishes updates to the same endpoint or a completely new one, and what sort of update has been made to an endpoint.

To help with this complexity, we've got a few levels of documentation to help:

1. This explanatory overview is at the highest level, and gives a basic explanation of some of the key steps in the data lifecycle.
2. Below that, the tutorials section documents some of the standard processes we follow for each of these steps, both when [adding data](../../Tutorials/Adding-Data) and [monitoring data quality](../../Tutorials/Monitoring-Data-Quality).
3. The procedure steps in the scenarios link to the most detailed level of documentation - the [how-to guides](../../How-to-guides) - which give step by step instructions for how to complete particular tasks.

## Validating data

When receiving data from the LPA, we need to first validate the data to check that it conforms to our data requirements.

Depending on the dataset, the LPAs usually use the [check service](https://submit.planning.data.gov.uk/check/) to check whether their data meets the specifications. But in most cases we still carry out validation checks ourselves before adding data.

Read the [how to validate an endpoint guide](../../How-to-guides/Validating/Validate-an-endpoint) to see the steps we follow.

## Adding data

There are two main scenarios for adding data:

- Adding a new endpoint to an existing dataset. This will usually be for a compiled, ODP dataset (e.g. adding a new endpoint from a Local Planning Authority to the `article-4-direction-area` dataset).

- Adding an endpoint for a new dataset and/or collection. This is usually for a national-scale dataset which is being added to the platform (e.g. adding `flood-storage-area` data from the Environment Agency to the platform for the first time).

The [adding data](../../Tutorials/Adding-Data) page in the tutorials section explains the process we follow for each of these scenarios.

You may find it useful to read some of the Key Concepts documentation, in particular on [pipeline processes and the data model](../Key-Concepts/pipeline-processes) and [endpoint types](../Key-Concepts/Endpoint-types).

## Maintaining data

Maintaining data means making sure that the changes a data provider makes to their data are reflected on the platform, as well as fixing any issues that occur due to incorrect configuration. All of the processes we follow here should be captured under our data quality framework, see the [monitoring data quality](../../Tutorials/Monitoring-Data-Quality) tutorial page.


## Retiring data

### Retiring endpoints

When an endpoint consistently fails, or LPAs give us a different endpoint (as opposed to the one we already have) to retrieve the data, we need to retire the old/failing endpoint. It is important to understand that while we retire an endpoint, this does not mean that the data associated with it will be retired as well. This only makes it so that the collector stops collecting new resources (data) from the endpoint. The data that has been retrieved previously from that endpoint will still be on the platform and will still be used.

When we retire an endpoint, we also need to retire the source(s) associated with it as sources are dependent on endpoints.

Read [how-to retire an endpoint](../../How-To-Guides/Retiring/Retire-endpoints) to learn more.

### Retiring resources

It won’t be necessary to do this step often, however, sometimes a resource should not continue to be processed and included in the platform. This can be for multiple reasons, and in most cases will occur when it has been found that the resource contains significant errors.

Read [how-to retire a resource](../../How-To-Guides/Retiring/Retire-resources) to learn more.

### Retiring entities

**Note:** We usually want to keep old entities on our platform as historical data. 

> **For example** a World Heritage Site was added as an entity to our platform. Although it is no longer a World Heritage Site, we want to retain the entity to indicate that it held this status during a specific period.

However, there are two situations when an entity might be removed:

1. It was added in error. In this case, we should remove it from our system.
2. It has been stopped for some reason. In this scenario, we should retain the entity.  


Ideally, we would mark such entities with end-dates to indicate they have been stopped, but implementing this requires additional work.

In a given scenario, determine the reason why the entities are no longer present.  
Check with Swati before deleting entities.
