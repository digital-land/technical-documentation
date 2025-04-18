# Assign Entities

1. **Download resource from CDN**

   First, we need to manually download the resource directly from the CDN. For this, we require the resource hash which can be found in the [`reporting_latest_endpoints` datasette](https://datasette.planning.data.gov.uk/digital-land/reporting_latest_endpoints?_sort=rowid&endpoint__exact=a16e45dbefe2d67a6d27c086768b6c3610d4e057bb19627da0cbdb13e3f0d2cd). The link has an example endpoint populated, just replace this with the actual endpoint.

   Once you have the resource hash, edit the following link with the correct information

   [https://files.planning.data.gov.uk/\[collection-name\]-collection/collection/resource/\[resource-hash](https://files.planning.data.gov.uk/[collection-name]-collection/collection/resource/[resource-hash)\]

   Here is an example link with ‘tree-preservation-order-collection’ as _collection-name_ and ed778c73ea51338d6576fb5992b189f2b94d9f3d5e199f46c1af520d6b0b3e6c as _resource-hash_:

   [https://files.planning.data.gov.uk/tree-preservation-order-collection/collection/resource/ed778c73ea51338d6576fb5992b189f2b94d9f3d5e199f46c1af520d6b0b3e6c](https://files.planning.data.gov.uk/tree-preservation-order-collection/collection/resource/ed778c73ea51338d6576fb5992b189f2b94d9f3d5e199f46c1af520d6b0b3e6c)

   Download the file to your local config repository and add it to the config. The location does not matter but this example puts it in a resource folder in the dataset’s collection folder.

2. **Run assign-entities script**
   Run the following command with your corresponding variables:

```
digital-land assign-entities [PATH_TO_RESOURCE] [ENDPOINT] [COLLECTION-NAME] [DATASET] [ORGANISATION] -c ./collection/[COLLECTION-NAME]/ -p ./pipeline/[COLLECTION-NAME]/
```

For example, using the example from step 1, the script would look like this:

```
digital-land assign-entities collection/tree-preservation-order/resource/4e0de67249898504311f4dde8ebf11bcb1bac52652320505113f4dc85635ea3e  3aeef0b2fb0bb0c85a25bd4491b3c56f70924d6a8ae9d9e22764885965a2b4c7 tree-preservation-order tree-preservation-order local-authority-eng:MDW -c ./collection/tree-preservation-order/ -p ./pipeline/tree-preservation-order/
```

3. **Check results**  
   Confirm the desired result in the lookup.csv file, the amount of entities that needed to be assigned should be the same amount that have been added in the lookup file.