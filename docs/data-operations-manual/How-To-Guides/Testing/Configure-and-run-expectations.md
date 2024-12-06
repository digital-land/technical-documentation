
## Creating a new expectation

Expecation is the term used to describe making assertions about our data for the purposes of data quality.

A single assertion might be something like: 

> *conservation-area entities belonging to the London Borough of Lambeth should not have geometries which are beyond the Lambeth local-planning-authority boundary*

Understanding whether or not this assertion is true helps us identify data quality issues.

Expectations can be created using rules defined in the pipeline configuration file `expect.csv` (see the relevant section in the [configure and endpoint guide](../Adding/Configure-an-endpoint.md) for more detail). The pipeline code uses these rules to create sets of expectations. And each of these expectations defines a single assertion which is made by executing an operation with a given set of parameters against a given set of data. Each assertion produces an entry for the expectation log which should show whether the assertion is True or False.

Operations are functions defined in [digital-land/expectations/operation.py](https://github.com/digital-land/digital-land-python/blob/main/digital_land/expectations/operation.py) and designed to work on a particular format of data (e.g. sqlite or csv). They can accept any required arguments but must return three things:

- `result`, a boolean value based on whether the expectation has been met or not
- `message`, a string giving summarised context to the result
-  `details`, a dictionary object which can be used to pass back more detailed context for the result, such as a list of entities which did not meet the expectation.

## Testing expectations

See the relevant section in the [configure and endpoint guide](../Adding/Configure-an-endpoint.md) to see how to define how expectations should be configured for execution against a dataset.

### Re-building the collection

Once expectations are defined in `expect.csv`, all you need to do is [build the collection locally](Building-a-collection-locally.md) to see the results. However, if you want to make changes and test there are some other steps you can follow to save having to re-build the entire collection from scratch after each change.

Any rules in `expect.csv` are loaded into `var/[COLLECTION-NAME]/cache/config.sqlite3`, which means that in order for any changes to `expect.csv` to be reflected you need to re-run `make init` for the collection, which will rebuild the config sqlite db.

So if you want to make expectation rule changes and test them without having to download all the of the collection files again, one option is to:

- make changes to `expect.csv`
- re-run `make init` to rebuild `config.sqlite3`
- run `rm -rf dataset` to remove dataset files
- run `make dataset` to build the dataset

### Checking expectation logs

Expectation logs are saved to the config directory `.parquet` files in the following location:

     `log/expectation/dataset=[DATASET-NAME]/[DATASET-NAME].parquet`

One of the quickest ways to examine these is just [install DuckDB](https://duckdb.org/docs/installation/) and use the Command Line Interface to query the parquet files.

Once installed you can run `duckdb` to activate it. You can then type a SQL command followed by a semicolon, and execute with enter. DuckDB allows you to read all files that match a glob pattern, like:

``` 
SELECT *
FROM `log/expectation/dataset=conservation-area/*.parquet`
LIMIT 10;
```
