# Maintaining Data

The scenarios are split into data being added and data being removed. In reality, endpoint updates could be a combination of both, in which case you will need to follow each process for entities which have been added or removed.

## New endpoint for existing provision

### Entities added

**Scenario:** Supplier has published a new endpoint for a dataset for the second time. The new endpoint has new entities.  
E.g., Platform has an endpoint for article-4-direction-area dataset from Barnet. Later, Barnet provides a new endpoint for the same dataset. The updated endpoint includes additional/new entities while retaining the reference for existing entities.

**Resolution:** 

* Retire old endpoint using the [End Endpoint](../Retire-endpoints) process (ODP provisions only)  
* Follow the [Add Endpoint](../Add-an-endpoint) process for the new endpoint.

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

### Entities removed

**Scenario:** Supplier has published a new endpoint for a dataset for the second time. The new endpoint has some missing entities.  
E.g., Platform has an endpoint for article-4-direction-area dataset from Barnet. Later, Barnet provides a new endpoint for the same dataset. The updated endpoint retains references for some entities, but a few are missing.

**Resolution:** 

* Retire old endpoint using the [End Endpoint](../Retire-endpoints) process (ODP provisions only)  
* Follow the [Add Endpoint](../Add-an-endpoint) process.  
* Cross-verify the references between resources.  
  * The entities generated from the old endpoint remain in lookup.csv.  
  * Use the [retire entities](../Retire-entities) process to retire entities that no longer exist on the new endpoint

**Outcome:**  
Follow [**Instructions for working with removed/old entities**](#instruction-for-working-with-removedold-entities) 

Configuration \-   
New entries in endpoint.csv, source.csv, and lookup.csv  
New entries in pipeline files based on requirement.  
End-date added in endpoint.csv and source.csv for the old endpoint.  
New entries in old-entity.csv  
Platform \-   
Endpoint updated for dataset  
Removed/old entities disappear from the site.  
Facts from the new resource get linked to the existing entities

### Data updated

**Scenario:** A new national dataset endpoint is published when the platform currently includes an endpoint for this dataset. All of the references are the same as the previous endpoint but some of the other fields may contain updated data, e.g. newer boundaries in the geometry field.

E.g., green-belt annual release

**Resolution:** 

* Retire old endpoint using the [End an Endpoint](../Retire-endpoints) process (ODP provision only)  
* Follow the [Add Endpoint](../Add-an-endpoint) process.

No need to add lookups as the references remain the same.

**Outcome:**  
Configuration \-   
New entries in endpoint.csv and source.csv  
Platform \-   
Endpoint updated for national dataset.  
Facts from latest resource linked to existing entities.

## Updated endpoint for existing provision

### Entities added

**Scenario:** Supplier adds new records to an existing endpoint.  
E.g., Barnet has updated their article-4-direction-area dataset with new records.  
Consider that Barnet’s endpoint contains records with reference values 1, 2, 3, 4, and 5, all of which are present on the platform. Later, new records with reference values 6 and 7 are added.

When new records are identified on an endpoint, the system creates a new resource and generates an “Unknown Entity” issue for the newly created resource.

**Resolution:** 

* Check for unknown entity issues by downloading the [Config Manager Issue Report](https://config-manager-prototype.herokuapp.com/reporting/odp-summary/issue).  
* Follow the [Assign Entities](../Assign-entities) process for the latest resource to add new entities.

**Outcome:**   
Configuration \-   
New entries in lookup.csv  
Platform \-   
Added/new entities appear on the site.  
“Unknown Entity” issue for the resource no longer exists.

### Entities removed

**Scenario:** Supplier removes records from an existing endpoint.  
E.g., Barnet has updated their article-4-direction-area dataset by removing records.  
Consider Barnet’s endpoint contains records with reference values 1, 2, 3, 4, and 5, which are present on the platform. Later, existing records with reference values 4 and 5 are removed.

**Resolution:** 

* Check for mismatches in the [Entity Count Comparison](https://github.com/digital-land/jupyter-analysis/blob/main/service_report/Compare_entity_count.ipynb) notebook (The Jupyter Notebook downloads a CSV file that can be used to get the deleted entity numbers). A mismatch may arise if a resource has duplicate references or if an organisation has multiple endpoints for a dataset. Examine the case closely to confirm that the mismatch is due to deleted entities.  
* Cross-verify the references between resources to identify entities which have been removed  
* Check with the LPA to ensure that they have removed the entities that were identified.  
* Follow the [Retire Entities](../Retire-entities) process for entities that have been removed. 

\!\!\! Note: the retire entities process should be followed here even if all entities have been deleted from the existing endpoint, as utilising old-entity.csv provides better control.

**Outcome:**   
Configuration \-   
New entries in old-entity.csv  
Platform \-   
Removed/old entities disappear from the site.

