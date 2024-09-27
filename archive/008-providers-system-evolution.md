## Status

Open

## Author(s)

[Chris Cundill](mailto:chris.cundill@tpximpact.com)

## Introduction

![Design Sprint Infographic](/digital-land/digital-land/wiki/odp/008/images/design-sprint.png)

During a design sprint held in May 2024, the Providers team of the Planning Data Service programme dreamed about what 
new services could be delivered to enable Data Providers to publish their planning and housing data onto the Planning 
Data Platform.

![Design Sprint journey](/digital-land/digital-land/wiki/odp/008/images/journey.png)

The team built and tested an idea together in 5 days.  That idea was a solution for Providers for problem of understanding
which planning datasets have been provided and the status of each.  The prototyped journey involved providing an overview
of all datasets, a more detailed summary of each dataset along with tasks to guide Providers to take the most appropriate
next step.

![Design Sprint Prototype screenshots](/digital-land/digital-land/wiki/odp/008/images/prototype-screenshots.png)

The clickable prototype is available on Heroku:

[Design Sprint Prototype on Heroku](https://design-sprint-prototype-8e5ca5d98540.herokuapp.com/overview/start)

The Mural board which captures the output of the design sprint is here:

https://app.mural.co/t/mhclg2837/m/mhclg2837/1710195433696/074cb0883565580ec5a3f17063526a3375cdd207?wid=0-1716536957786

## Detail

### Overview

To service the needs of LPAs to manage the publication of their datasets, the following changes are proposed:

 * A new "Providers" web application in the Provider Service system
 * A new "Performance" database and API in the Data Collection Pipeline system

Naming of the new web application might need some refinement, as will the exact user journeys.  Nevertheless, the prototyped
features provide enough information to think about the next architectural evolution of the Providers service.

### Provider Service

The Provider Service will be expanded with a NodeJS/Express frontend web app to fulfil user needs around providing 
datasets.  The existing Check service will be merged into this new frontend app.
The existing Redis session store, currently serving the Check service, will be utilised to enable horizontal scaling 
of the service, while a Postgres database will store tracking data for any dataset tasks that are offered to users.

#### Containers

![Providers System Containers](/digital-land/digital-land/wiki/odp/008/images/containers.drawio.png)

### Data Collection Pipeline

The Data Collection Pipeline system will gain a new Performance database and API to store and provide statistical data 
around the collection pipeline.  Such will include an organisational summary view of datasets.

#### Code - Database

The initial version of the performance database might contain a table which provides summary information for each dataset
and organisation combination.  The fields illustrated here were inspired by the Heroku prototype and are yet to be finalised.

![Data Collection Performance ERD](/digital-land/digital-land/wiki/odp/008/images/code-database-performance.drawio.png)

#### Data Strategy

See the [Decentralised Data ODP](/digital-land/digital-land/wiki/Open-Design-Proposal---007---Decentralised-Data) to understand
the general database strategy along with the roles and responsibilities of each database across the systems 
of the Planning Data Service.


## Implementation considerations

* New AWS resources will need to be provisioned for:

    * Providers Frontend
        * Create ECS Service to run on Fargate
    * Retire Check frontend (lpa-validator-fe)
        * Currently runs on EC2 compute via ECS
    * Performance Database (Postgres on AWS RDS Aurora)
        * Create empty database and app users for Performance API
    * Performance API
        * Create ECS Service to run on Fargate

* New code repositories, GitHub pipelines, ECR image repositories and ECS tasks will be needed for:

    * Performance API
        * Service should be able to migrate/mange own database schema
        * No need for CloudFront distribution
        * Internal load balancer sufficient


## Design Comments/Questions

No feedback yet.