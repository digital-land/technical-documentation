---
title: Setting up and working on the Submit Service
---

### Architecture
- Runs on [Datasette](datasette.planning.data.gov.uk) currently for all data queries,with an interest to move all queries to pipeline API / platform API for speed and cost savings.
- All requests are made to the async service, can be run locally or with the docker file.

### Important Links
-   [Architecture Diagrams](/architecture-and-infrastructure/solution-design/check-service/)
-   [Debugging Async Service](/development/live-service/debugging-live-services/)