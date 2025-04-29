# Retire entities

We only retire entities which have been added in error.

Entities which are no longer in use, for example where a nature reserve is de-designated, a world heritage site is de-listed, a site has been developed and removed from the brownfield-land register, or a listed building has been de-listed should continue to be in the dataset marked with an `end-date` added.
The `end-date` should be ideally added to the data source the data provider, but may be provided in a secondary source provided by us.

Where two or more entities exist for the same entity, they should be [merged](/data-operations-manual/How-To-Guides/Maintaining/Merge-entities/) rather than deleting the duplicate entity.

An entity which has been added in error can be removed by adding it to the [old-entity](https://digital-land.github.io/specification/dataset/old-entity/) config.

1. **Identify the entity number**  
   First, you need to identify the entity number of the entity you wish to remove. This can easily be done by filtering by the reference in [lookup on datasette](https://datasette.planning.data.gov.uk/digital-land/lookup?_sort=rowid&reference__exact=A4Da1d). The link is filtering for the reference `A4Da1d` as an example, just replace it with the appropriate reference. Copy the entity number under `entity`.  
     
2. **Populate old-entity.csv**

   Next, add a new row to the `old-entity.csv` file located in the corresponding pipeline folder E.g., if the dataset is `article-4-direction`, populate the `old-entity.csv` file within that pipeline folder. Add the corresponding entity number, the related HTTP response error code (this should be 410 if the entity is being retired). You should also add a comment with the reason for its deletion in the `notes` column.
   

For example, the populated new line could look like this:

```
7010002871,410,,new endpoint and reference field for GLO,,,
```

Once done, push the changes.
