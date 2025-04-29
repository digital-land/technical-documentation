## Pipeline process / data model 

See the [about section of the planning.data website](https://www.planning.data.gov.uk/about/)  to learn more about the website and programme objectives:

*“Our platform collects planning and housing data from local planning authorities (LPAs) and transforms it into a consistent state, across England. Anyone can view, download and analyse the data we hold.”*

We ask Local Planning Authorities (LPAs) to publish open data on their website in the form of an accessible URL, or API endpoint. These URLs are called **endpoints**.

The system that is used to take data from endpoints and process it into a consistent format is called the **pipeline**. The pipeline is able to collect data hosted in many different formats, identify common quality issues with data (and in some cases resolve them), and transform data into a consistent state to be presented on the website.


Data is organised into separate **datasets**, each of which may consist of data collected from just one or many endpoints. Datasets might be referred to as either **compiled** or **single-source** based on how data for them is provided. 

> For example the [article-4-direction-area dataset](https://www.planning.data.gov.uk/dataset/article-4-direction-area) has many providers as we collect data from LPAs to add to this dataset, and is therefore a **compiled** dataset.   
> 
> The [agricultural-land-classification dataset](https://www.planning.data.gov.uk/dataset/agricultural-land-classification) on the other hand has just one provider as it is a dataset with national coverage published by Natural England, and is therefore a **single-source** dataset.

Each dataset is organised into separate **collections**, which are groups of datasets collected together based on their similarity. For example, the `conservation-area-collection` is the home for the `conservation-area` and the `conservation-area-document` dataset. 

Each collection has its own set of configuration files. Thse files are essentially a set of data which tells the pipeline how to work, e.g. where to go to collect data from, and how to process it once it's collected. These files are all stored in the [config repo](https://github.com/digital-land/config/), split up into a `pipeline` and a `collection` folder for each collection. 

> e.g. the configuration files for the `conservation-area` collection are split into these folders:
>  * [https://github.com/digital-land/config/tree/main/collection/conservation-area](https://github.com/digital-land/config/tree/main/collection/conservation-area)  
>  * [https://github.com/digital-land/config/tree/main/pipeline/conservation-area](https://github.com/digital-land/config/tree/main/pipeline/conservation-area) 

See the [pipeline configuration](../Pipline-configuration) page for more details..

The data management team is responsible for adding data to the platform, and maintaining it once it’s there, see [here for the list of team responsibilities](https://docs.google.com/document/d/1PoAUktKj80qOTvI4BB3qZkZdwpiGEq_woEfrIdwg2Ac/edit#heading=h.aoi2nezcsd1h) in the Planning Data Service Handbook.

## Resources 

Once an endpoint is added to our data processing pipeline it will be checked each night for the latest data. When an endpoint is added for the first time we take a copy of the data; this unique copy is referred to as a **resource**. If the pipeline detects any changes in the data, no matter how small, we save a new version of the entire dataset, creating a new resource. Each separate resource gets given a unique reference which we can use to identify it.

## Facts 

The data from each resource is saved as a series of facts. If we imagine a resource as a table of data, then each combination of entry (row) and field (column) generates a separate **fact**: a record of the value for that entry and field. For example, if a table has a field called “reference”, and the value of that field for the first entry is “Ar4.28”, we record the name of the field and the value of it along with a unique reference for this fact. You can see how this appears in our system [here](https://datasette.planning.data.gov.uk/article-4-direction-area?sql=select+fr.resource%2C+f.fact%2C+f.entity%2C+f.field%2C+f.value%0D%0Afrom+fact_resource+fr%0D%0Ainner+join+fact+f+on+fr.fact+%3D+f.fact%0D%0Awhere+%0D%0A+++resource+%3D+%22684deb1f613f6e74e31858176704c33c4437996c60210975c27be5f0c82b4057%22%0D%0A+++and+field+%3D+%22reference%22%0D%0A+++and+value+%3D+%22Ar4.28%22%0D%0A%0D%0A).

So a table with 10 rows and 10 columns would generate 100 facts. And each time data changes on an endpoint, all of the facts for the new resource are recorded again, including any new facts. We can use these records to trace back through the history of data from an endpoint.

A fact has the following attributes:

* `fact` \- UUID, primary key on `fact` table in database  
* `entity` \- optional, numeric ID, `entity` to which fact applies  
* `start-date` \- optional, date at which fact begins to apply (not date at which fact is created within data platform)  
* `end-date` \- optional, date at which fact ceases to apply  
* `entry-date` \- optional, date at which fact was first collected

## Entities 

An Entity is the basic unit of data within the platform. It can take on one of many types [defined by `digital-land/specification/typology.csv`](https://github.com/digital-land/specification/blob/40c777610a8e292145635ff875203145ee5f1e49/specification/typology.csv). An entity has the following attributes:

* `entity` \- incrementing numeric ID, manually assigned on ingest, different numeric ranges represent different datasets, primary key on `entity` table in SQLite and Postgis databases  
* `start-date` \- optional, date at which entity comes into existence (not date at which entity is created within data platform)  
* `end-date` \- optional, date at which entity ceases to exists  
* `entry-date` \- optional, date at which entity was first collected  
* `dataset` \- optional, name of `dataset` (which should correspond to [`dataset` field in `digital-land/specification/dataset.csv`](https://github.com/digital-land/specification/blob/40c777610a8e292145635ff875203145ee5f1e49/specification/dataset.csv)) to which entity belongs  
* `geojson` \- optional, a JSON object conforming to [RFC 7946 specification](https://datatracker.ietf.org/doc/html/rfc7946) which specifies the geographical bounds of the entity  
* `typology` \- optional, the type of the entity which should correspond to [the `typoology` field in `digital-land/specification/typology.csv`](https://github.com/digital-land/specification/blob/40c777610a8e292145635ff875203145ee5f1e49/specification/typology.csv)  
* `json` \- optional, a JSON object containing metadata relating to the entity

Facts that are collected from resources get assigned to entities based on a  combination of the reference of the record in the resource, the organisation that provided the resource and the dataset it belongs to (*needs more clarification, or a link out to more detail somewhere*).

So as well as the default(?) attributes above, an [entity in the article-4-direction-area dataset](https://www.planning.data.gov.uk/entity/5010000101) can also have attributes like `permitted-development-rights` and `notes`.
