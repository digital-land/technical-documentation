# Configure an endpoint

## [collection/endpoint](https://github.com/digital-land/specification/blob/main/content/dataset/endpoint.md?plain=1) 

Endpoints identify the URLs which are used to collect data from. 


Important fields:

* `attribution` \- statement about the source of the data  
* `collection` \- repeats the name of the thing we are collecting  
* `documentation-url` \- the web link to the providers documentation about the data  
* `endpoint-url` \- the URL of the endpoint itself  
* `endpoint` \- the endpoint hash  
* `entry-date` \- the date the endpoint record was added  
* `end-date` \- the date from which an endpoint is no longer valid  
* `plugin` \- any plugin that is required to successfully collect from an endpoint, e.g. `wfs`, `arcgis`  
* `start-date` \- the date from which an endpoint is valid

`https://github.com/digital-land/digital-land-python/tree/main/digital_land/plugins`

## [collection/source](https://github.com/digital-land/specification/blob/main/content/dataset/source.md?plain=1)

Sources identify where we get the data from, including providing a documentation-url to the publishers website which can provide additional information on data downloaded from the source. Sources are separate to endpoints but each endpoint should be associated with a source. \-

Important fields:

* `documentation-url` \- the URL of the webpage that links to the endpoint   
* `end-date` \- used to end a source  
* `endpoint` \- the hash for the endpoint associated with the source  
* `licence` \- the licence type provided with the source, one of [these types](https://datasette.planning.data.gov.uk/digital-land/licence)  
* `organisation` \- the organisation providing the source  
* `pipelines` \- the pipelines used to process the source, multiple should be separated by a semi-colon  
* `source` \- the hash for the source

## [collection/old-resource](https://github.com/digital-land/specification/blob/main/content/dataset/old-resource.md?plain=1) 

This table is used to identify resources which should no longer be processed. When a resource is added here all of the facts it generated will be deleted (though the resource itself will be retained).

Important fields:

* `old-resource` \- the hash of the resource being ended  
* `status` \- the status code for this entry, use `410` for ended *(\!\! are there others which can be used?*)  
* `resource` \- *uncertain, can a resource be re-directed?*  
* `notes` \- to record why this configuration change was made

## [pipeline/column](https://github.com/digital-land/specification/blob/main/content/dataset/column.md?plain=1)

This table is used to add extra mappings from the resource column headers to our specification field names, for example mapping a field named `UID` in a resource to our `reference` field.

Important fields:

* `column` \- the column header in the resource being mapped  
* `field` \- the field name in our specification the column header should be mapped to

## [pipeline/combine](https://github.com/digital-land/specification/blob/main/content/dataset/combine.md?plain=1) 

Used to combine values across multiple rows. The grouping is based on the reference field so this only works when there are multiple rows per reference (note this happens after concat so concat can be used to create a reference from multiple fields and control the grouping to some extent)

> *Example*   
> In the `agricultural-land-classification` collection the `geometry` field of the Natural England is grouped by the reference, resulting in individual polygons being grouped into a multipolygon or geometry collection.  
> 
> See: [https://github.com/digital-land/config/blob/main/pipeline/agricultural-land-classification/combine.csv\#L2](https://github.com/digital-land/config/blob/main/pipeline/agricultural-land-classification/combine.csv#L2) 

Important fields:

* `field` \- the field that should be grouped  
* `separator` \- a separator to use between the grouped field values, e.g. a hyphen or semicolon to separate strings

*Uncertain about how different field types are combined, need more detail*.

## [pipeline/concat](https://github.com/digital-land/specification/blob/main/content/dataset/concat.md?plain=1) 

Used to combine values across multiple fields into a single one.

> *Example*  
> Concatenate the values from `name` and `area_ref` fields to create a unique value for `reference` when there is no unique reference provided in the resource  
> 
> See: [https://github.com/digital-land/config/blob/main/pipeline/agricultural-land-classification/concat.csv\#L2](https://github.com/digital-land/config/blob/main/pipeline/agricultural-land-classification/concat.csv#L2)

Important fields:

* `field` \- the field to use the concatenated value in  
* `fields` \- a list of the fields in the resource (or our schema?) to concatenate, separated by a semicolon  
* `separator` \- an optional separator to use between the concatenated values
* `prepend` \- optional text to add before the concatenated values
* `append` \-  optional text to add after the concatenated values

## [pipeline/convert](https://github.com/digital-land/specification/blob/main/content/dataset/convert.md?plain=1) 

*Unsure\!*

## [pipeline/default-value](https://github.com/digital-land/specification/blob/main/content/dataset/default-value.md?plain=1)

Used to set a default value for all values in a field

> *Example*  
> Set the value of `flood-risk-level` to 2 for all values from an endpoint in the `flood-risk-zone`, because the data is provided split into a different endpoint per flood risk level but each resource doesn’t record the level explicitly in a field. 
>
> See: [https://github.com/digital-land/config/blob/main/pipeline/flood-risk-zone/default-value.csv\#L3](https://github.com/digital-land/config/blob/main/pipeline/flood-risk-zone/default-value.csv#L3) 

Important fields:

* `field` \- the field to use the default value in  
* `value` \- the value to enter as default in the field

## [pipeline/default](https://github.com/digital-land/specification/blob/main/content/dataset/default.md?plain=1)

*I think to set a default value using another field in the resource, but uncertain how this is different to column. Need more info.*

## [pipeline/filter](https://github.com/digital-land/specification/blob/main/content/dataset/filter.md?plain=1) 

Used to filter a resource so that only a subset of the records are processed, based on whether the values in one of the resources fields are in a user-defined list.

> *Example*  
> To only add records from a resource where the `tree-preservation-zone-type` field has a value of “Area” to the `tree-preservation-zone` dataset.
>  
>  See: [https://github.com/digital-land/config/blob/main/pipeline/tree-preservation-order/filter.csv\#L6](https://github.com/digital-land/config/blob/main/pipeline/tree-preservation-order/filter.csv#L6)

Important fields:

* `field` \- the field to search for the pattern  
* `pattern` \- the pattern to search for in the field (can just be a string, *does this accept regex like in patch?*)

## [pipeline/lookup](https://github.com/digital-land/specification/blob/main/content/dataset/lookup.md?plain=1)

Used to map the relationships between the reference that a data provider uses to describe a thing, to the entity number that we have assigned to that thing. It is important to appreciate that there can be a 1:1 or a many:1 relationship here because we may collect data from multiple providers who publish information about the same thing (e.g. both LPAs and Historic England publish conservation area data, so we may map a reference from each to the same entity).

These records are produced at the entity assignment phase when an endpoint is added for the first time. Verifying that the lookups have been produced as expected, and also managing any merging with existing entities is an important stage of the [Adding an endpoint](https://github.com/digital-land/digital-land/wiki/Adding-An-Endpoint) process.

Important fields:

* `prefix` \- the dataset this entity is a part of  
* `resource` \- (not used?)  
* `organisation` \- the organisation who provides data about this entity  
* `reference` \- the identifier used by the provider to refer to this entity  
* `entity` \- the reference we have generated to refer to this entity

## [pipeline/old-entity](https://github.com/digital-land/specification/blob/main/content/dataset/old-entity.md?plain=1) 

Used to redirect and remove entities.

To prevent an entity from appearing on the platform, add a record with status 410 and the entity number to the file and it will be removed.

To redirect an entity, use status 301 along with current entity number and the target entity number. (mainly used for merging geographically duplicated entities)

Important fields:

* `old-entity` \- current entity number  
* `status` \- 301 (redirect) / 410 (remove)  
* `entity`\- target entity number

## [pipeline/patch](https://github.com/digital-land/specification/blob/main/content/dataset/patch.md?plain=1)

Used to replace values that match a particular string or string pattern with another value.

> *Example*  
> Change any string in the `listed-building-grade` field of a resource in the `listed-building` collection that contains the numeric character “2” to be “II” instead, in order to match the specification.
>  
>  See: [https://github.com/digital-land/config/blob/main/pipeline/listed-building/patch.csv\#L10](https://github.com/digital-land/config/blob/main/pipeline/listed-building/patch.csv#L10)

Important fields:

* `field` \- the field to search for the pattern  
* `pattern` \- the pattern to search for in the field (*should this be a regex pattern?*)   
* `value` \- the value to use as a replacement for incoming values that match the pattern

## [pipeline/skip](https://github.com/digital-land/specification/blob/main/content/dataset/skip.md?plain=1) 

Sometimes, the raw data contains extraneous lines that can cause issues during processing. To address this, the `skip.csv` file is used to skip specific lines from the raw data.

> *Example*  
> Consider this [endpoint url](https://www.worcestershire.gov.uk/sites/default/files/2023-12/2023-12-21_csv_file_1_developer-agreement_202312_education.csv), the file begins with some extra data that we need to skip. 
>  
> See: [https://github.com/digital-land/config/blob/main/pipeline/developer-contributions/skip.csv\#L7](https://github.com/digital-land/config/blob/main/pipeline/developer-contributions/skip.csv#L7)

Important fields:

* `pattern` - the pattern to search for in the raw endpoint file

## [pipeline/transform](https://github.com/digital-land/specification/blob/main/content/dataset/transform.md?plain=1)

*Unsure\!*
