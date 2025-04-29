# Retire entities

This is similar to retiring a resource in that it won’t happen often. It may sometimes be necessary to correct errors in the data provided by the LPAs. E.g., if the provided entries are located outside the LPA’s boundary or extra unnecessary entities have been provided.

\> It might be more appropriate to redirect/merge entities rather than deleting the entity. **Need to discuss, when is this the case?**

1. **Identify the entity number**  
   First, you need to identify the entity number of the entity you wish to remove. This can easily be done by filtering by the reference in [lookup on datasette](https://datasette.planning.data.gov.uk/digital-land/lookup?_sort=rowid&reference__exact=A4Da1d). The link is filtering for the reference `A4Da1d` as an example, just replace it with the appropriate reference. Copy the entity number under `entity`.  
     
2. **Populate old-entity.csv**

   Next, simply add a new row the `old-entity.csv` file located in the corresponding pipeline folder E.g., if the dataset is `article-4-direction`, populate the `old-entity.csv` file within that pipeline folder. Add the corresponding entity number, the related HTTP response error code (this should be 410 if the entity is being retired). It might also be useful to comment on the reasoning behind its deletion under `notes`.

   

For example, the populated new line could look like this:

```
7010002871,410,,new endpoint and reference field for GLO,,,
```

Once done, push the changes.