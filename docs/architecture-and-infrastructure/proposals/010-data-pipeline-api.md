# Open Design Proposal - 010 - Data Pipeline API

## Author(s)

 * [Chris Cundill](chrisc@diligentsoft.co)

## Introduction

An internal API is proposed for providing access to data pipeline metadata, which includes:

* Logs

* Issues

* Processed & converted files

* Performance aggregations

* Specification

* Configuration


## Status

> OPEN

 * Draft: proposal is still being authored and is not officially open for comment yet
 * Open: proposal is open for comment
 * Closed: proposal is closed for comment with implementation expected
 * On Hold: proposal is on hold due to concerns raised/project changes with implementation not expected

## Detail

### Overview

Until the time of writing (October '24), the need for access to information about the data collection pipelines has been largely satisfied through Datasette, which has been configured to ingest SQLite files stored on EFS volumes.

It is no secret to the team that our use of Datasette stretches beyond the purpose for which it was originally designed. Recent advances with the Submit tool have further proven the difficulty of relying upon Datasette for OLAP style queries.  We have effectively been using Datasette as an API for data collection pipeline metadata - a task which it doesn't naturally suit.  Performance and stability are just two of the problems presented by our attempts to employ Datasette as a drop-in replacement for an API.

Another problem with using Datasette as an API, is the lack of versioning for endpoints. It becomes very brittle and the only method is to create shadow a database.

An internal API, separate from our existing public platform API is proposed to provide access to the data consumed and produced by the data collection pipelines.  This metadata includes:

* Logs

* Issues

* Processed & converted files

* Performance aggregations

* Specification

* Configuration

#### API Spec

An [example of the potential shape of the API](https://app.swaggerhub.com/apis/CHRISCUNDILL_1/data-collection-pipelines/1.0.0-oas3.1) has been provided in OpenAPI specification format.

#### Public access

> The API will be _publicly_ internal, meaning it will be coded in the open and generally accessible.  The demarcation of "internal"
is important since it communicates the intent that API is primarily for satisfying the needs of internal software tools. 
> Should it become apparent that certain endpoints have wider-appeal, they could be promoted to the public platform API.

#### Versioning

For versioning of endpoints and the associated request & response schemas, the root of the API path will contain a version, i.e. `/v1`.  For example, the path to the logs endpoint would as follows:

 * https://pipeline-api.planning.data.gov.uk/v1/logs

Ideally, a maximum of two versions of the same resource would be maintained at any one time, e.g. 

 * https://pipeline-api.planning.data.gov.uk/v1/logs
 * https://pipeline-api.planning.data.gov.uk/v2/logs

Importantly, a deprecation date should be agreed for the older version, and all known API consumers should be notified of such.

### Container diagram

#### Pipeline API only

The following container diagram illustrates how the Pipeline API will be able to communicate across a number of different data sources and formats to provide a single view of pipeline metadata.

![Pipeline API Container](/images/proposals/010-data-pipeline-api/containers-pipeline-api-only.drawio.png)

#### Pipeline API within System Context

The following container diagram shows how the Pipeline API interacts within the Data Collection Pipeline system context:

![Pipeline System Containers](/images/proposals/010-data-pipeline-api/containers.drawio.png)

Note that the Pipeline API reads collection and pipeline metadata in Parquet format from the existing Collection Archive bucket. The existing Collection Task will be modified to write data in Parquet format, as well as CSV and SQLite.

Remember that the [overall system context diagram](/architecture-and-infrastructure/solution-design/) is helpful if you're not so familiar with the architecture of the Digital Planning Data service.

## Implementation considerations

* New code repositories, GitHub pipelines, ECR image repositories and ECS tasks will be needed for:

  * Internal API
    * Service should be able to migrate/mange own database schemas
    * No need for CloudFront distribution not absolutely necessary
    * Public load balancer will be required
    * Use version number at root of API paths, e.g. v1

* New AWS resources will need to be provisioned for:

  * Internal API
    * Create ECS Service to run on Fargate


## Design Comments/Questions

No feedback yet.
