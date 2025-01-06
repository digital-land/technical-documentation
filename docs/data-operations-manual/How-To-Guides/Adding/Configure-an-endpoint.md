# Configure an endpoint

## [collection/endpoint](https://github.com/digital-land/specification/blob/main/content/dataset/endpoint.md?plain=1)

Endpoints identify the URLs which are used to collect data from.

Important fields:

- `attribution` \- statement about the source of the data
- `collection` \- repeats the name of the thing we are collecting
- `documentation-url` \- the web link to the providers documentation about the data
- `endpoint-url` \- the URL of the endpoint itself
- `endpoint` \- the endpoint hash
- `entry-date` \- the date the endpoint record was added
- `end-date` \- the date from which an endpoint is no longer valid
- `plugin` \- any plugin that is required to successfully collect from an endpoint, e.g. `wfs`, `arcgis`
- `start-date` \- the date from which an endpoint is valid

`https://github.com/digital-land/digital-land-python/tree/main/digital_land/plugins`

## [collection/source](https://github.com/digital-land/specification/blob/main/content/dataset/source.md?plain=1)

Sources identify where we get the data from, including providing a documentation-url to the publishers website which can provide additional information on data downloaded from the source. Sources are separate to endpoints but each endpoint should be associated with a source. \-

Important fields:

- `documentation-url` \- the URL of the webpage that links to the endpoint
- `end-date` \- used to end a source
- `endpoint` \- the hash for the endpoint associated with the source
- `licence` \- the licence type provided with the source, one of [these types](https://datasette.planning.data.gov.uk/digital-land/licence)
- `organisation` \- the organisation providing the source
- `pipelines` \- the pipelines used to process the source, multiple should be separated by a semi-colon
- `source` \- the hash for the source

## [collection/old-resource](https://github.com/digital-land/specification/blob/main/content/dataset/old-resource.md?plain=1)

This table is used to identify resources which should no longer be processed. When a resource is added here all of the facts it generated will be deleted (though the resource itself will be retained).

Important fields:

- `old-resource` \- the hash of the resource being ended
- `status` \- the status code for this entry, use `410` for ended _(\!\! are there others which can be used?_)
- `resource` \- _uncertain, can a resource be re-directed?_
- `notes` \- to record why this configuration change was made

## [pipeline/column](https://github.com/digital-land/specification/blob/main/content/dataset/column.md?plain=1)

This table is used to add extra mappings from the resource column headers to our specification field names, for example mapping a field named `UID` in a resource to our `reference` field.

Important fields:

- `column` \- the column header in the resource being mapped
- `field` \- the field name in our specification the column header should be mapped to

## [pipeline/combine](https://github.com/digital-land/specification/blob/main/content/dataset/combine.md?plain=1)

Used to combine values across multiple rows. The grouping is based on the reference field so this only works when there are multiple rows per reference (note this happens after concat so concat can be used to create a reference from multiple fields and control the grouping to some extent)

> _Example_  
> In the `agricultural-land-classification` collection the `geometry` field of the Natural England is grouped by the reference, resulting in individual polygons being grouped into a multipolygon or geometry collection.
>
> See: [https://github.com/digital-land/config/blob/main/pipeline/agricultural-land-classification/combine.csv\#L2](https://github.com/digital-land/config/blob/main/pipeline/agricultural-land-classification/combine.csv#L2)

Important fields:

- `field` \- the field that should be grouped
- `separator` \- a separator to use between the grouped field values, e.g. a hyphen or semicolon to separate strings

_Uncertain about how different field types are combined, need more detail_.

## [pipeline/concat](https://github.com/digital-land/specification/blob/main/content/dataset/concat.md?plain=1)

Used to combine values across multiple fields into a single one.

> _Example_  
> Concatenate the values from `name` and `area_ref` fields to create a unique value for `reference` when there is no unique reference provided in the resource
>
> See: [https://github.com/digital-land/config/blob/main/pipeline/agricultural-land-classification/concat.csv\#L2](https://github.com/digital-land/config/blob/main/pipeline/agricultural-land-classification/concat.csv#L2)

Important fields:

- `field` \- the field to use the concatenated value in
- `fields` \- a list of the fields in the resource (or our schema?) to concatenate, separated by a semicolon
- `separator` \- an optional separator to use between the concatenated values
- `prepend` \- optional text to add before the concatenated values
- `append` \- optional text to add after the concatenated values

## [pipeline/convert](https://github.com/digital-land/specification/blob/main/content/dataset/convert.md?plain=1)

_Unsure\!_

## [pipeline/default-value](https://github.com/digital-land/specification/blob/main/content/dataset/default-value.md?plain=1)

Used to set a default value for all values in a field

> _Example_  
> Set the value of `flood-risk-level` to 2 for all values from an endpoint in the `flood-risk-zone`, because the data is provided split into a different endpoint per flood risk level but each resource doesn’t record the level explicitly in a field.
>
> See: [https://github.com/digital-land/config/blob/main/pipeline/flood-risk-zone/default-value.csv\#L3](https://github.com/digital-land/config/blob/main/pipeline/flood-risk-zone/default-value.csv#L3)

Important fields:

- `field` \- the field to use the default value in
- `value` \- the value to enter as default in the field

## [pipeline/default](https://github.com/digital-land/specification/blob/main/content/dataset/default.md?plain=1)

_I think to set a default value using another field in the resource, but uncertain how this is different to column. Need more info._

## [pipeline/entity-organisation](https://github.com/digital-land/specification/blob/main/content/dataset/entity-organisation.md?plain=1)

Used to set the entity range for organisations within the conservation-area collection. This is done to ensure that entities within a range are linked to a certain organisation in the case that we have lookup entries for the same entity from different organisations. This helps prioritise data from the authoritative source.

> _Example_  
> For `the conservation-area` dataset, we have an entry for `local-authority:BAB` with a `entity-minimum` of `44005968` and `entity-maximum` for `44005997`. This sets out that any entity within that range will be part of that organisation. More ranges for that organisation and dataset can be added in following rows e.g. setting the next range as `44008683 -> 44008684`
>
> Important fields:

- `dataset` \- the dataset to target e.g `conservation-area-document`
- `organisation` \- the organisation to apply to e.g `local-authority:BAB`
- `entity-minimum` \- sets the starting point of that range (inclusive)
- `entity-maximum` \- sets the ending point of that range (inclusive)

## [pipeline/expect](https://github.com/digital-land/specification/blob/main/content/dataset/expect.md?plain=1)

This file is used to define rules that will be used by the pipeline code to generate and test expectations. The fields define the operation that will be used and the parameters to pass it, as well as what the expected result is and some metadata for the expectation that will appear in the [expectation table](https://datasette.planning.data.gov.uk/digital-land/expectation) in datasette.

Important fields:

- `dataset` \- The dataset or list of datasets (separated by ';') within the collection, which the expectation should be executed against. 
- `organisations` \- the organisation or list of organisations which the expectation should be executed for, e.g. `local-authority:BAB` (list separated by ';').

    If given a list, the rule will create multiple expectations, each which will be executed against only entities within each organisation.

    You can also use a dataset to specify a list of organisations, e.g. `local-authority`, or `national-park-authority`. Or leave the field blank if the expectation should be executed at a dataset level.

- `operation` \- the expectation operation to be executed. Must be defined in [digital-land/expectations/operation.py](https://github.com/digital-land/digital-land-python/blob/main/digital_land/expectations/operation.py).

- `parameters` \- a JSON string passing the operation parameters. Keys should be enclosed in double quotes, and values in double quotes and braces. This is to handle jinja formatting, which can use class attributes to parameterise  some of the inputs, e.g. 

    `"{""lpa"":""{{ organisation.local_planning_authority }}""}"`

- `name` \- the name for any expectations that will be created by the rule. It's best to not use parameters in this field as a generic name for each expectation created by the same rule makes it easier to quickly compare results in the [expectation table](https://datasette.planning.data.gov.uk/digital-land/expectation).


- `description` \- a description for the expectation. This can accept  jinja formatting to output parameters in the same way as the as the `parameters` field, e.g.

    ```A test to check there are no listed-building-outline entities outside of the boundary for {{ organisation.name }}```

## [pipeline/filter](https://github.com/digital-land/specification/blob/main/content/dataset/filter.md?plain=1)

Used to filter a resource so that only a subset of the records are processed, based on whether the values in one of the resources fields are in a user-defined list.

> _Example_  
> To only add records from a resource where the `tree-preservation-zone-type` field has a value of “Area” to the `tree-preservation-zone` dataset.
>
> See: [https://github.com/digital-land/config/blob/main/pipeline/tree-preservation-order/filter.csv\#L6](https://github.com/digital-land/config/blob/main/pipeline/tree-preservation-order/filter.csv#L6)

Important fields:

- `field` \- the field to search for the pattern
- `pattern` \- the pattern to search for in the field (can just be a string, _does this accept regex like in patch?_)

> **NOTE!**  
> Filter config for a dataset will only work for fields that are in the dataset schema. So if you need to filter based on a column that's in the source data and not in the schema, you will first need to map it to a schema column using `column.csv` config.

## [pipeline/lookup](https://github.com/digital-land/specification/blob/main/content/dataset/lookup.md?plain=1)

Used to map the relationships between the reference that a data provider uses to describe a thing, to the entity number that we have assigned to that thing. It is important to appreciate that there can be a 1:1 or a many:1 relationship here because we may collect data from multiple providers who publish information about the same thing (e.g. both LPAs and Historic England publish conservation area data, so we may map a reference from each to the same entity).

These records are produced at the entity assignment phase when an endpoint is added for the first time. Verifying that the lookups have been produced as expected, and also managing any merging with existing entities is an important stage of the [Adding an endpoint](https://github.com/digital-land/digital-land/wiki/Adding-An-Endpoint) process.

Important fields:

- `prefix` \- the dataset this entity is a part of
- `resource` \- (not used?)
- `organisation` \- the organisation who provides data about this entity
- `reference` \- the identifier used by the provider to refer to this entity
- `entity` \- the reference we have generated to refer to this entity

## [pipeline/old-entity](https://github.com/digital-land/specification/blob/main/content/dataset/old-entity.md?plain=1)

Used to redirect and remove entities.

To prevent an entity from appearing on the platform, add a record with status 410 and the entity number to the file and it will be removed.

To redirect an entity, use status 301 along with current entity number and the target entity number. (mainly used for merging geographically duplicated entities)

Important fields:

- `old-entity` \- current entity number
- `status` \- 301 (redirect) / 410 (remove)
- `entity`\- target entity number

## [pipeline/patch](https://github.com/digital-land/specification/blob/main/content/dataset/patch.md?plain=1)

Used to replace values that match a particular string or string pattern with another value.

> _Example_  
> Change any string in the `listed-building-grade` field of a resource in the `listed-building` collection that contains the numeric character “2” to be “II” instead, in order to match the specification.
>
> See: [https://github.com/digital-land/config/blob/main/pipeline/listed-building/patch.csv\#L10](https://github.com/digital-land/config/blob/main/pipeline/listed-building/patch.csv#L10)

Important fields:

- `endpoint` \- (optional if targetting specific endpoit) the endpoint hash to target a specific endpoint for a patch
- `field` \- the field to search for the pattern
- `pattern` \- the pattern to search for in the field (_should this be a regex pattern?_)
- `value` \- the value to use as a replacement for incoming values that match the pattern

## [pipeline/skip](https://github.com/digital-land/specification/blob/main/content/dataset/skip.md?plain=1)

Sometimes, the raw data contains extraneous lines that can cause issues during processing. To address this, the `skip.csv` file is used to skip specific lines from the raw data.

> _Example_  
> Consider this [endpoint url](https://www.worcestershire.gov.uk/sites/default/files/2023-12/2023-12-21_csv_file_1_developer-agreement_202312_education.csv), the file begins with some extra data that we need to skip.
>
> See: [https://github.com/digital-land/config/blob/main/pipeline/developer-contributions/skip.csv\#L7](https://github.com/digital-land/config/blob/main/pipeline/developer-contributions/skip.csv#L7)

Important fields:

- `pattern` - the pattern to search for in the raw endpoint file

## [pipeline/transform](https://github.com/digital-land/specification/blob/main/content/dataset/transform.md?plain=1)

_Unsure\!_
