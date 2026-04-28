---
title: Solution design - Planning Data Platform
---

### Container Diagram

![Planning Data Platform Container Diagram](/images/planning-data-platform/containers.drawio.png)

### Infrastructure Diagram

![Planning Data Platform Infrastructure Diagram](/images/planning-data-platform-deployment.drawio.png)

### Containers

#### Planning Data Application

This is both the API and website found at [www.planning.data.gov.uk]. This is the main entry point for data consumers as well as aplication built using our data

Key Info:
- Repository: [https://github.com/digital-land/digital-land.info] (the site was originally known as digital-land.info)
- Sentry Project: planning-data-platform
- Terraform System: platform
- Framework: FastAPI

#### Digital Land Database

This is the main postgres/postgis database supporting the platform as is primarily used int he search queries on Planning Data. It's structure is controlled by sqlaclhemy models via alembic found in [https://github.com/digital-land/digital-land.info].

Key Info:
- Repository: [https://github.com/digital-land/digital-land.info] (the code that manages it's shape is defined in here, see the migrations foder and the. appication db folder)
- Terraform System: core (required across multiple software systems so is defined in core)

#### Tiles Bucket

AWS S3 bucket conntaining vector tilles for dispplaying maps on the website, it is behind a publicaly avialable CDN found at [tiles.planning.data.gov.uk].

Key Info:
- Repository: [https://github.com/digital-land/tiles-builder-task] - this belongs to the Data Collection Pipelines system but is the task that creates the tiles
- Terraform System: core - to give access across systems

#### Files Bucket

AWS S3 bucket conntaining all files collected and transformed in the planning data service. The Files bucket contains raw resources colllected from providers, sqlite dataset package files and dataset files. This covers files in bronze,silver and god layers. It is behind a publicaly avialable CDN found at [tiles.planning.data.gov.uk].

Key Info:
- Repositories: 
  - [https://github.com/digital-land/collection-task] - this is the main containner image used for our processing which writes files to this s3 bucket.
- Terraform System: core - to give access across systems

#### Datasette Application

Currently being used as a way to access our silver layer which is a set of sqlite files. These sqlite files are a mixture of dataset packages and reporting packages.

Key Info:
- Repository: [https://github.com/digital-land/datasette-builder] - application code for this, primarily just runs datasette python package with a specific startup script
- Terraform System: platform

#### Datasets Volume

EFS volumne for storing dataset package sqlite files as datasette can't access them directly fom S3

Key Info:
- Repository: [https://github.com/digital-land/digital-land-efs-sync] - task which is triggered via event bridge to load sqlite files from the Files bucket into the Datasets Volume. pat of the data collection pipeline system
- Terraform System: core




