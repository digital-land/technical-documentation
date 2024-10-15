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

> [!NOTE]
> DRAFT

 * Draft: proposal is still being authored and is not officially open for comment yet
 * Open: proposal is open for comment
 * Closed: proposal is closed for comment with implementation expected
 * On Hold: proposal is on hold due to concerns raised/project changes with implementation not expected

## Detail

### Overview

Until the time of writing (October '24), the need for access to information about the data collection pipelines has been
largely satisfied through Datasette, which has been configured to ingest SQLite files stored on EFS volumes.

It is no secret to the team that our use of Datasette stretches beyond the purpose for which it was originally designed. Recent
advances with the Submit tool have further proven the difficulty of relying upon Datasette for OLAP style queries.  We have
effectively been using Datasette as an API for data collection pipeline metadata - a task which it doesn't naturally suit.  Performance
and stability are just two of the problems presented by our attempts to employ Datasette as a drop-in replacement for an API.

An internal API, separate from our existing public platform API is proposed to provide access to the data consumed and produced by the data
collection pipelines.  This metadata includes:

* Logs

* Issues

* Processed & converted files

* Performance aggregations

* Specification

* Configuration

An [example of the potential shape of the API](https://app.swaggerhub.com/apis/CHRISCUNDILL_1/data-collection-pipelines/1.0.0-oas3.1) has been provided in OpenAPI specification format.

> [!NOTE]
> The API will be _publicly_ internal, meaning it will be coded in the open and generally accessible.  The demarcation of "internal"
is important since it communicates the intent that API is primarily for satisfying the needs of internal software tools. 
> Should it become apparent that certain endpoints have wider-appeal, they could be promoted to the public platform API.

### Container diagram

The following container diagram illustrates how the Pipeline API will be able to communicate across a number of different
data sources and formats to provide a single view of pipeline metadata.

![Data Pipelines System Context](/images/proposals/010-data-pipeline-api/containers.drawio.png)

## Implementation considerations

* New code repositories, GitHub pipelines, ECR image repositories and ECS tasks will be needed for:

  * Internal API
    * Service should be able to migrate/mange own database schemas
    * No need for CloudFront distribution not absolutely necessary
    * Public load balancer will be required

* New AWS resources will need to be provisioned for:

  * Internal API
    * Create ECS Service to run on Fargate


## Design Comments/Questions

No feedback yet.
