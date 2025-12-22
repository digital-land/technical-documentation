---
title: Solution design
---

The solution architecture for the Planning Data Service has been modelled using the [C4 approach](https://c4model.com/).

## System Context

![Planning Data Service System Context](/images/system-context.drawio.png)


## Systems

* [Data Pipelines](/architecture-and-infrastructure/solution-design/data-pipelines/) - This system is where both the batch data proccessing and the dynamic data pocessing is done to support the othe systemms.
* [Planning Data Platform](/architecture-and-infrastructure/solution-design/planning-data-platform/) - the system for the [platform](www.plannig.data.gov.uk)
* [Provide](/architecture-and-infrastructure/solution-design/check-service/) - the systemm to support tools and feedback for data providers

> 🔜 Need to build a ayatem page for the data management service 

### Others

 * [DNS Setup](/architecture-and-infrastructure/dns/)