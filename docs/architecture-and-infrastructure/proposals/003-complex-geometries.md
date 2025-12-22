---
title: Open Design Proposal - 003 - Querying on Complex geometries
---

Author(s) - [Samriti Sadhu](mailto:ssadhu@scottlogic.com)
## Introduction
Some of the API queries are exremely slow and often result in 502s, particularly when querying near large and complex datasets such as flood-risk-zone. To improve query performance, we propose using ST_Subdivide function of postgis to split large geometries into smaller, more manageable components and store them in a separate table. This approach will optimize spatial queries.

### Result
The execution time was reduced from ~30 seconds to ~4 seconds for an example API query in local environment, significantly improving performance. 
example query: [Link Here](https://www.planning.data.gov.uk/entity.json?longitude=-1.5093779539231569&latitude=53.36780846610864&entries=current&geometry_relation=intersects&limit=100&exclude_field=geometry,point)

## Status

 Open 

## Detail

### Overview
Significant performance degradation in spatial queries was observed, especially when dealing with large bounding boxes containing complex geometries. This was because some dastasets and entities like flood risk zones contained highly detailed geometries that extended across large areas, generating extensive bounding boxes. As a result, even when the queried points were outside the actual geometry, the large bounding box caused the geometry to be considered in spatial queries for that area. See the example below.

![Calculation of Bouding box for a large complex geometry](/images/geometry_bounding_box.drawio.png)

#### Things Tried

1. Index Optimization
Tried optimizing the existing spatial indexes to improve query performance. This involved re-indexing the entity.geometry column and ensuring that appropriate index types (e.g., GiST, SPGIST) were applied. Despite these optimizations, there wasn't significant performance improvements due to the size and complexity of the geometries involved.

2. Refining Spatial Queries
In an attempt to optimize the spatial queries, the ST_Subdivide function was used directly within the query. This approach aimed to split large geometries on the fly during query execution. However, it was found that applying ST_Subdivide in the query itself resulted in increased execution times, as the subdivision process was performed alongside the spatial filtering. This approach was not ideal, as it added computational overhead during query processing.

#### Implementation

A new table, **entity_subdivided**, will be introduced to store subdivided geometries derived from entity.geometry of complex datasets like flood-risk-zone. The subdivision will be done using ST_Subdivide, ensuring that large and complex geometries are broken into smaller parts while maintaining spatial accuracy.
The entity_subdivided table will store the multiple subdivided geometries corresponding to each entity hence a One-to-Many Relationship.

##### Key Changes:

* A new table **entity_subdivided** to store subdivided geometries.

![Class diagram for entity_subdivided](/images/entity_subdivided.drawio (1).png)

* Queries involving spatial filters will use entity_subdivided table's geometry instead of entity.geometry for datasets like flood-risk-zone.
* Modification wherever needed of existing queries to join entity and entity_subdivided.
* Changes in digital-land-postgres to update entity_subdivided table.

#### Deployment and Testing Plan
* Migration Script: Create a script to create new table entity_subdivided, applying ST_Subdivide to complex datasets
* Data Integrity Checks: Ensure that subdivided geometries remain valid and do not introduce self-intersections.


## Questions to consider

* How will updates to geometries in entity_subdivided be handled? 
A: This needs to be done along with entity table in digital-land-postgres.

* will there be DB updates or data migrations?
A: Yes, a new table needs to be created and updated with subdivided geometries from entity table for complex datasets like flood-risk-zone


## Design Comments

