# Standard process


The trigger for this process should be a new Jira ticket on the [data managment board](https://mhclgdigital.atlassian.net/jira/software/projects/DATA/boards/229) for adding data. This ticket should link to a [Digital Land Service Desk](https://mhclgdigital.atlassian.net/jira/servicedesk/projects/DLSD) ticket which contains the correspondence with the customer.

When you pick up the ticket, follow the steps below.

### 1. Validate endpoint

Follow the [validate an endpoint](../../How-To-Guides/Validating/Validate-an-endpoint) process to check whether the data meets the specifications. If you find any issues you should respond the the data provider and ask if they can fix them.

Before adding new data you should also **check whether there is already data for this provision on the platform**. You can do this using the [LPA dashboard in the publish service](https://submit.planning.data.gov.uk/organisations), our [config manager reports](https://config-manager-prototype.herokuapp.com/reporting/odp-summary/status), or by using the [search page on planning.data](https://www.planning.data.gov.uk/entity/).

If there is existing data you may need to retire an old endpoint alongside adding the new one. The scenarios further down this page will help you work out the right process to follow.

> **NOTE**  - If adding a **single source dataset**:  
> The validation process will not be so standard. We should receive a description of the dataset from data design in the ticket. Check that the data on the endpoint matches the description.

### 2. Add endpoint

Follow the [add an endpoint](../../How-To-Guides/Adding/Add-an-endpoint) process to set up the configuration for the new endpoint in the config repo. 

Push your changes but **do not merge them before moving on to the next step**.

### 3. QA endpoint configuration

In order to make sure the configuration for the new endpoint is checked properly you should raise a PR for your changes and fill out the template that is automatically generated. This will make it clear what sort of change is being made, and also give you a QA checklist to fill out.

When creating a branch in git use the following naming convention:

> Adding data branch name: `[initials]/add-[ORG]-[DATASET]`
>  
> e.g. If Joe Bloggs is adding Article 4 direction data for Bristol he'd call his branch: `jb/add-BST-A4D`

Acronyms for collections could be: `A4D` for article-4-direction, `CA` for conservation-area, `LB` for listed-building, and `TPO` for tree-preservation-order.

For organisation you should use the the `organisation` value from the [organisation table](https://datasette.planning.data.gov.uk/digital-land/organisation) with the prefix (e.g. `local-authority`) removed.

Once it's been raised, share your PR with a colleague in data management team to review, and they should follow the same checks in the checklist.


### 4. Merge changes (and run workflow)

Once your PR is approved the changes can be merged. At this point you could also run the action workflow to build the updated dataset (see the last step of the [add an endpoint](../../How-To-Guides/Adding/Add-an-endpoint) process).

> **NOTE**  - If adding a **national dataset**: 
> You should first run the action workflow in the development Airflow environment. This will publish the new data on the development planning data site so that the data design team can review it before going live. 
> 
> Currently, the live Airflow workflow runs each night and will pick up your changes, so you should run the dev workflow as early as possible in the day and let design know they have the rest of the day to review them. If you need to make significant changes, revert your commit from config `main` so they don't go live.

### 5. Review new data on platform
Once the workflow has been run (either manually, or in the automated overnight process) you should carry out some last QA checks:

- Check that there are the expected number of new entities on the platform (you can use the search page to do this, either with the [location parameter](https://www.planning.data.gov.uk/entity/?dataset=conservation-area&geometry_curie=statistical-geography%3AE09000022) or the [`organisation_entity` parameter](https://www.planning.data.gov.uk/entity/?dataset=conservation-area&organisation_entity=192) if the new data doesn't have a location).
- Check if the new data is on the [LPA dashboard in the publish service](https://submit.planning.data.gov.uk/organisations).

### 6. Close ticket

Once the final checks are complete you can close the tickets:

- Reply to the customer in [Digital Land Service Desk](https://mhclgdigital.atlassian.net/jira/servicedesk/projects/DLSD) using the canned responses to let them know data is live.
- Move Jira tickets to done

# New endpoint scenarios
When adding data from a new endpoint you may need to follow slightly different steps based on the context, like exactly what data is being provided, how it's being provided, and whether data for the provision already exists. 

The sections below aim to explain some common scenarios to make it clear what steps should be followed, and what the expected outcome should be.

## New endpoint for a _single_, new ODP provision

**Scenario**: Supplier has published an endpoint for a dataset for the first time.  
E.g., Barnet has published their article-4-direction-area dataset.

**Resolution**: Follow the [Validate Endpoint](../../How-To-Guides/Validating/Validate-an-endpoint) process.  
Follow the [Add Endpoint](../../How-To-Guides/Adding/Add-an-endpoint) process.

**Outcome**:  
Configuration \-  
New entries in endpoint.csv, source.csv, and lookup.csv  
New entries in pipeline files based on requirement.  
Platform \-  
Entities associated with the endpoint appear on the site.

## New endpoint for _multiple_, new ODP provisions

**Scenario:** Supplier has published an endpoint for multiple datasets for the first time.  
E.g., Barnet has published their tree-preservation-order and tree datasets in one endpoint.

**Resolution:**

- Follow the [Validate Endpoint](../../How-To-Guides/Validating/Validate-an-endpoint) process.
- Follow the [Add Endpoint](../../How-To-Guides/Adding/Add-an-endpoint) process.
- Carefully follow the [Handling Combined Endpoints](../../How-To-Guides/Adding/Add-an-endpoint#Handling-Combined-Endpoints) section in the Add Endpoint process, which covers configuring multiple endpoints on the same link.

**Outcome:**  
Configuration \-  
 New entries in endpoint.csv, source.csv, and lookup.csv  
New entries in pipeline files based on requirement.  
Platform \-  
 Entities associated with the endpoint appear on the site.

## New endpoint with geographical duplicates

**Scenario:** A provider has shared a new endpoint to be added to the platform. During the [endpoint validation step](../../How-To-Guides/Validating/Validate-an-endpoint), geographical duplicates with existing data on the platform are identified.

E.g., North Somerset LPA share an endpoint for conservation-area data for us to add to the site. The endpoint checker flags that there are geographical duplicates in this dataset with conservation-area entities from Historic England that are already on the platform.

Note: this is most likely at the moment to happen for the conservation-area dataset, where we have both authoritative (LPAs) and alternative (Historic England) data providers.

**Resolution:**

- Follow the [Add Endpoint](../../How-To-Guides/Adding/Add-an-endpoint) process as normal up to step 5
- After step 5, once the new entries for the lookup.csv have been generated, use the outputs from the “**Duplicates with different entity numbers”** section of the endpoint checker to replace the newly generated entity numbers for any duplicates, with the entity numbers of the existing entity that they match.

**Outcome:**

Configuration \-  
New entries in endpoint.csv, source.csv, and lookup.csv  
New entries in pipeline files based on requirement.  
Platform \-  
Facts from the resources for the two separate records mapped to the same entity will appear on the platform under the same entity number


## New endpoint for existing provision

### Entities added

**Scenario:** Supplier has published a new endpoint for a dataset for the second time. The new endpoint has new entities.  
E.g., Platform has an endpoint for article-4-direction-area dataset from Barnet. Later, Barnet provides a new endpoint for the same dataset. The updated endpoint includes additional/new entities while retaining the reference for existing entities.

**Resolution:**

- Retire old endpoint using the [End Endpoint](../../How-To-Guides/Retiring/Retire-endpoints) process (ODP provisions only)
- Follow the [Add Endpoint](../../How-To-Guides/Adding/Add-an-endpoint) process for the new endpoint.

**Outcome:**  
Configuration \-  
New entries in endpoint.csv, source.csv, and lookup.csv  
New entries in pipeline files based on requirement.  
End-date added in endpoint.csv and source.csv for the old endpoint.  
The entities already generated from the old endpoint remain in lookup.csv.

Platform \-  
Endpoint updated for dataset  
Added/new entities appear on the site.  
Facts from the new resource get linked to the existing entities


### Data updated

**Scenario:** A new national dataset endpoint is published when the platform currently includes an endpoint for this dataset. All of the references are the same as the previous endpoint but some of the other fields may contain updated data, e.g. newer boundaries in the geometry field.

E.g., green-belt annual release

**Resolution:**

- Retire old endpoint using the [End an Endpoint](../../How-To-Guides/Retiring/Retire-endpoints) process (ODP provision only)
- Follow the [Add Endpoint](../../How-To-Guides/Adding/Add-an-endpoint) process.

No need to add lookups as the references remain the same.

**Outcome:**  
Configuration \-  
New entries in endpoint.csv and source.csv  
Platform \-  
Endpoint updated for national dataset.  
Facts from latest resource linked to existing entities.
