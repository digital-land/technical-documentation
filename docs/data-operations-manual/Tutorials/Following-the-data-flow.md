---
title: Purpose
---

This tutorial isn't for a particular task, instead it aims to demonstrate the data that is produced as a result of adding a new endpoint to our configuration.

You can follow it before or after you've followed the [adding data](../Adding-data) process yourself, but the idea is that by following the links here you'll start to build up a more complete picture of how data is collected, processed and published on our platform, which will help understand the data adding process better.

If you've not added an endpoint yourself yet, have a look at the example Pull Request in the Configuration section below, which was made to add a new endpoint for Southwark.

Otherwise, if you have recently added an endpoint yourself you could follow the links in the Platform and Datasette sections and update the queries to check that one instead.


# The data flow
## Configuration

See the following PR: [https://github.com/digital-land/config/pull/463](https://github.com/digital-land/config/pull/463)

It's adding a new `tree-preservation-zone` endpoint for Southwark.

Three files are updated: 

* `collection/endpoint.csv`
* `collection/source.csv`
* `pipeline/lookup.csv`

These are the key files which tell the pipeline where to collect data from and how to process it. Once these changes are made in the config repo, the overnight pipeline run will collect any new data from the endpoint.

## Platform

You can see this endpoint is live on our different services:

* Southwark's Submit service [dashboard page](https://submit.planning.data.gov.uk/organisations/local-authority:SWK)
* Planning.data.gov.uk [search page](https://www.planning.data.gov.uk/entity/?dataset=tree-preservation-zone&organisation_entity=329)


## Datasette

This is how we interact with the dataset files which are produced by the pipeline, as well as some other databases which summarise data that's useful for reporting.

### Performance tables

https://datasette.planning.data.gov.uk/performance

These tables summarise information about provisions, endpoints, resources, and issues to make it easier to see what's going on at a high level.

Check for the Southwark endpoint that's been added to see how it's captured in these tables.

* [`provision_summary`](https://datasette.planning.data.gov.uk/performance/provision_summary?_sort=rowid&organisation__contains=SWK) table can be queried by `organisation` to see all of the data we're expecting an organisation to provide, and its status.
* [`reporting_historic_endpoints`](https://datasette.planning.data.gov.uk/performance/reporting_historic_endpoints?_sort=rowid&dataset__exact=tree-preservation-zone&organisation__contains=SWK) shows all of the Southwark TPZ endpoints that we've added, and the resources that have been collected from them. Take a look at the start and end dates for endpoints and resources to see the changes that have happened over time. You can query this table to find provisions based on the `dataset` and `organisation`.
* Find the endpoint in the [`endpoint_dataset_issue_type_summary`](https://datasette.planning.data.gov.uk/performance/endpoint_dataset_issue_type_summary?_sort=rowid&endpoint__exact=090ff21f75d6ff5b97c0d49434679839fd1eb64d781db6285abf574307f970bc) table. This shows any issues that have been logged for the endpoint and all of its resources.


### tree-preservation-zone dataset

Every night the pipeline runs and uses the configuration data to collect and process all of the data for each dataset. It produces a `.sqlite3` database for each separate dataset; these databases have a common architecture across all datasets and store all of the data which is then served on the platform.

This is the datasette page for the TPZ dataset: https://datasette.planning.data.gov.uk/tree-preservation-zone

Explore each of the tables to see how they relate to the configuration changes that were made above, and the data that the pipeline processed from Southwark's new endpoint after the changes were made. We'll use one of the resources that was collected from the Southwark TPZ endpoint as an example: `ff3c0871f2b415dea86fffa4058633d914c01b0df048077ad48ad4dda6ca0db0`.

* [`dataset_resource`](https://datasette.planning.data.gov.uk/tree-preservation-zone/dataset_resource?_sort=rowid&resource__exact=ff3c0871f2b415dea86fffa4058633d914c01b0df048077ad48ad4dda6ca0db0) shows some processing information about the resource.
* [`column_field`](https://datasette.planning.data.gov.uk/tree-preservation-zone/column_field?_sort=rowid&resource__exact=ff3c0871f2b415dea86fffa4058633d914c01b0df048077ad48ad4dda6ca0db0) shows how the columns in the resource have been mapped to the fields of our data specification
* [`issue`](https://datasette.planning.data.gov.uk/tree-preservation-zone/issue?_sort=rowid&resource__exact=ff3c0871f2b415dea86fffa4058633d914c01b0df048077ad48ad4dda6ca0db0) shows any issues that have been logged while processing the resource
* [`fact`](https://datasette.planning.data.gov.uk/tree-preservation-zone/fact?_sort=fact&entity__exact=19130279) records all of the facts that have been linked to an entity
* these facts can be traced back to particular resources using the [`fact_resource` table](https://datasette.planning.data.gov.uk/tree-preservation-zone/fact_resource?_sort=rowid&resource__exact=ff3c0871f2b415dea86fffa4058633d914c01b0df048077ad48ad4dda6ca0db0), which records the hashes of all the facts that were recorded from the resource



For more detail on the relationship between resources, facts and entities, see [this blog post](https://digital-land.github.io/blog-post/storing-and-updating-data/) 