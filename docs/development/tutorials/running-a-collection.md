# Running A Data Collection Pipeline

### Needs Completing

For data engineers and often others in our team this is a key process that generates the files that are later loaded into the platform.

Once you understand  how  to run it  for a  Colllection then it can be applied to any  to debug errors that may have happened over night. It would be good  to read the key  concepts in the  data operations manual for clarity on the  terms that we use. this tutorial will describe the practical applications of these concepts.

### Anatomy of a collection repository

First it's good to understand the anatomy of a collection. these fies may not exist as they are generated when initialising and running the colection.

#### Inputs

* [collection/source.csv](https://github.com/digital-land/brownfield-land/blob/main/collection/source.csv) — the list of data sources by organisation, see [specification/source](https://digital-land.github.io/specification/schema/source/)
* [collection/endpoint.csv](https://github.com/digital-land/brownfield-land/blob/main/collection/endpoint.csv) — the list of endpoint URLs for the collection, see [specification/endpoint](https://digital-land.github.io/specification/schema/endpoint)
* [collection/resource/](https://github.com/digital-land/brownfield-land/blob/main/collection/resource/) — collected resources
* [collection/resource.csv](https://github.com/digital-land/brownfield-land/blob/main/collection/resource.csv) — a list of collected resources, see [specification/resource](https://digital-land.github.io/specification/schema/resource)

#### Outputs

* [collection/log/](https://github.com/digital-land/brownfield-land/blob/main/collection/log/) — individual log JSON files, created by the collection process
* [collection/log.csv](https://github.com/digital-land/brownfield-land/blob/main/collection/log.csv) — a collection log assembled from the individual log files, see [specification/log](https://digital-land.github.io/specification/schema/log)
* [collection/resource.csv](https://github.com/digital-land/brownfield-land/blob/main/collection/resource.csv) — a list of collected resources, see [specification/resource](https://digital-land.github.io/specification/schema/resource)
* [fixed/](https://github.com/digital-land/brownfield-land/blob/main/fixed/) — contains amended resources that previously could not be processed
* [harmonised/](https://github.com/digital-land/brownfield-land/blob/main/harmonised/) — The output of the [`harmonise` stage of the pipeline](#run-the-pipeline-to-make-the-dataset)
* `/var/converted/` - contains CSV files (named by hash of resource) with outputs of intermediary steps to create `transformed/` file