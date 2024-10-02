This section covers situations when we add new data onto the platform.

## New endpoint for a *single*, new ODP provision

**Scenario**: Supplier has published an endpoint for a dataset for the first time.  
E.g., Barnet has published their article-4-direction-area dataset.

**Resolution**: Follow the [Validate Endpoint](../Validate-an-endpoint) process.  
Follow the [Add Endpoint](../add-an-endpoint) process.

**Outcome**:  
Configuration \-  
New entries in endpoint.csv, source.csv, and lookup.csv  
New entries in pipeline files based on requirement.  
Platform \-  
Entities associated with the endpoint appear on the site.

## New endpoint for *multiple*, new ODP provisions

**Scenario:** Supplier has published an endpoint for multiple datasets for the first time.  
E.g., Barnet has published their tree-preservation-order and tree datasets in one endpoint.

**Resolution:** 

* Follow the [Validate Endpoint](../Validate-an-endpoint) process.  
* Follow the [Add Endpoint](../add-an-endpoint) process.  
* Carefully follow the [Handling Combined Endpoints](Add-an-endpoint#Handling-Combined-Endpoints) section in the Add Endpoint  process, which covers configuring multiple endpoints on the same link.

**Outcome:**  
Configuration \-  
	New entries in endpoint.csv, source.csv, and lookup.csv  
New entries in pipeline files based on requirement.  
Platform \-  
	Entities associated with the endpoint appear on the site.

## New endpoint with geographical duplicates

**Scenario:** A provider has shared a new endpoint to be added to the platform. During the [endpoint validation step](../Validate-an-endpoint), geographical duplicates with existing data on the platform are identified.

E.g., North Somerset LPA share an endpoint for conservation-area data for us to add to the site. The endpoint checker flags that there are geographical duplicates in this dataset with conservation-area entities from Historic England that are already on the platform.

Note: this is most likely at the moment to happen for the conservation-area dataset, where we have both authoritative (LPAs) and alternative (Historic England) data providers. 

**Resolution:** 

* Follow the [Add Endpoint](../add-an-endpoint) process as normal up to step 5  
* After step 5, once the new entries for the lookup.csv have been generated, use the outputs from the “**Duplicates with different entity numbers”** section of the endpoint checker to replace the newly generated entity numbers for any duplicates, with the entity numbers of the existing entity that they match.

**Outcome:**

Configuration \-   
New entries in endpoint.csv, source.csv, and lookup.csv  
New entries in pipeline files based on requirement.  
Platform \-   
Facts from the resources for the two separate records mapped to the same entity will appear on the platform under the same entity number