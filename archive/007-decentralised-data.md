## Status

Draft

## Author(s)

[Chris Cundill](mailto:chris.cundill@tpximpact.com)

## Introduction

We have a lot of data either produced by the pipelines or maintained by us to run the pipelines. We need a strategy to ensure this data is stored in the appropriate way and the ownership is with the appropriate team.

## Detail

### Overview

To avoid building a monolithic database, the following changes are proposed:

 * Decentralise from the Digital Land database into specialised databases
 * Establish Organisation and Configuration databases

More coming soon.

### System Context

#### Data Perspective

![Planning Data Service System Context](/digital-land/digital-land/wiki/odp/007/images/system-context-data-perspective.drawio.png)


## Implementation considerations

More coming soon.


## Design Comments/Questions

### Should organisation be it's own database?

The organisation data is a single table of al our organisations that we have recorded (many of which we collect data from). Does this need to be it's own db or should it just sit in one of the other databases. organisation is a data package which contains all data from the organisation datasets. 

data packages are a concept that has been fully fleshed out yet but they could in theory take any form.

### Should we call the audit database log?

The audit database will contain all of the information produced by the piplines overnight. This includes:

* Collection logs - did we manage to download from the url or not?
* Issue Logs - when normalising and processing data when problems were encountered
* Column field log - which columns of incoming data were mapped to our field names

The above is a starting list but could grow if we need to include more logs for different stages. For example a conversion. log or a dataset build log.

No feedback yet.