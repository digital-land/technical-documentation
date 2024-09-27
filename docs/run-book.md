# Run Book

This document contains some basic instructions for fixing common issues encountered operating the service.

## Outage Procedure

When an outage occurs the following process should be followed.

* Post a message into the team chat in slack
  * Replace **AFFECTED_APPLICATIONS** with a list of services that are down
  * Replace **MEET_LINK** with a google meet link [create a new one here](https://meet.new)
  * Replace **INCIDENT_RESPONSE_DOCUMENT** with a google doc link [create a new one here](https://doc.new)

```
@here *Service Outage*

AFFECTED_APPLICATIONS

MEET_LINK

INCIDENT_RESPONSE_DOCUMENT
```

* All team members must join the google meet link and begin documenting the outage.

Resolving an outage is an iterative process that should be improved with the lessons learnt from the previous outages.
It is suggested that the outage document contain the following headers to direct work appropriately. This is provided in Markdown to allow for easier updating of this Run Book.

```
### Outage - APPLICATION - DATE (YYYY-MM-DD)

#### In attendance

* A list of people who have responded to the outage and the roles they have taken

#### Description

A brief description of the outage, including affected services

#### Running log

Put timestamped entries under here including actions, observations, etc.
    * Action **TIME We did x.**
    * Observation **TIME We observed that x happened.**

#### Postmortem

A few paragraphs explaining the root cause of the issue and what measures have been taken to mitigate
further instances.

```

Outage Roles:

* **Scribe** The role of scribe is to maintain the incident report document during diagnosis and resolution of the outage.
  * Requires edit access to the google document tracking the incident.
  * Requires read-write access to the technical documentation repository.
* **Observer** The role of observer is to keep track of changes made to application and infrastructure code, approving
    any pull requests where needed.
  * Requires read-only access to the AWS account hosting the applications that are experiencing an outage.
  * Requires read-write access to any GitHub repositories hosting code for the applications that are experiencing an outage.
* **Actor** The role of actor is to be the only person who makes changes to application code and deployed infrastructure.
  * Requires read-write access to the AWS account hosting the applications that are experiencing an outage.
  * Requires read-write access to any GitHub repositories hosting code for the applications that are experiencing an outage.

It is worth checking the [incident response history](#incident-response-history)

Once the outage has been resolved it is a good idea to take a break before reflecting on the outage and completing the
postmortem section of the document. Once the document is complete, the contents must be copied under the section
[Incident Response History](#incident-response-history) for future reference, taking care to remove any secret
information from the document.

## Common Issues

 TBA 

## Incident Response History

### Outage - Datasette - 2024-08-23

#### In attendance

Async on Slack:

* Infrastructure Team
* Providers Team

#### Description

Over night we had requests on the providers site which used datasette to access data. the url used is
datasette.planning.data.gov.uk. The datasette application was reporting 502 errors implying  that the serve was down.

#### Running log

**On (2024-08-23)**

* At around 03:00 AM and 07:00AM the requests were made and sentry reported the events to the notification channel
* At 08:00AM the infrastructure team reacted to and investigates these errors. It was found that the application had automatically reset itself and the site was back up and operational.

#### Postmortem

Under further investigation it was identified that the traffic was mostly due to crawlers on the providers site. The providers team will
be adding a robots.txt file to the service to stop this traffic in the future.

The datasette outage was due to datasets being updated overnight. when data is added to the source it can cause the application to
restart especially when requests are being made at the same time. we will investigate further to identify if this can be solved
in the current set up but there are already plans to replace datasette to support the providers service which will remove these errors.

We will continue to monitor the impact of these errors after the robots.txt is implemented. 

The smoke tests did not trigger an alarm implying that the service was never down for ten minutes and had fixed itself. 

### Outage - Check Service - 2024-07-17

#### In attendance

Async on Slack:

* Owen Eveleigh
* Ben Hodgkiss
* Ernest Man
* Chris Cundill
* George Goodall

#### Description

The [Planning Data Check Service](https://check.planning.data.gov.uk/) is not available - and is returning an error page.

#### Running log

**On (2024-07-17)**

* Ben Hodgkiss noticed a canary alarm in Slack that the Check service canaries had failed twice at 9:17 and 9:27 am (BST).
* Once noticing, Owen Eveleigh was informed. After an initial investigation, an incident was declared.
* Ernest Man and Chris Cundill began to perform the full investigation of the issue, working alongside George Goodall for any identified application problems.
* The issue was identified as an intermittent front-end application issue. As a short-term fix, the app was restarted.
* At 11:46am, the Check service was back online.
* Further investigations and fixes will be carried out to do a long-term fix to the identified issue.

#### Postmortem

To be completed once incident completed.

### Outage - Title boundaries not displayed on Map

#### In attendance

Async on Slack:

* Paul Downey
* Chris Cundill

#### Description

Paul Downey reported that he couldn’t find any title boundaries on our map and observed from the browser console that it
appears as though the titles requested are not found (return 404 errors).

![Title boundary map issue - screenshot](/images/psd-title-boundary-issue.png)

#### Running log

**On (2024-07-12)**

* Paul Downey reported the issue on Slack, asking for it to be investigated after the weekend, on Monday.

**On (2024-07-15)**

* Chris Cundill began investigating. Following discussion with Owen Eveleigh, it appears that the job to populate
datasette tiles with title boundaries may not be functioning normally and therefore has resulted in no map tile data
for title boundaries.
* After investigating the system containers responsible for populating datasette tiles, an ECS task was identified as
the system container responsible for building map tile data for datasette tiles.  The ECS task is triggered by a
Cloudtrail event (originating from S3) via EventBridge.
  * The source code for the ECS task is at [Tiles Builder GitHub repo](https://github.com/digital-land/tiles-builder)
  * The EventBridge rule is named production-datasette-tile-builder-entity-uploaded-trigger
  * The ECS task definition is named production-datasette-tile-builder-task
* Having not found any logging from the ECS task, the AWS S3 CLI was used to re-upload the .sqlite3 file for the
title-boundary dataset to thus trigger an invocation of the ECS Task
 * The upload did not result in an invocation of the ECS Task so the Cloudtrail event log was consulted
 * It was observed that the requestParameters were truncated in the Cloudtrail event which means the event pattern in
 the EventBridge rule would not have matched
   * Examples of (CompleteMultipartUpload) events for other datasets were found from previous logs which did include
   the full requestParameters and would therefore match the EventBridge rule pattern

**On (2024-07-16)**

 * After reviewing these findings, the following change to the event pattern was proposed...

 Current

 ```json
 {
   "detail": {
     "eventName": ["PutObject", "CompleteMultipartUpload"],
     "eventSource": ["s3.amazonaws.com"],
     "requestParameters": {
       "bucketName": ["production-collection-data"],
       "key": [{
         "suffix": ".sqlite3"
       }]
     }
   },
   "detail-type": ["AWS API Call via CloudTrail"],
   "source": ["aws.s3"]
 }
 ```

 Proposed:

 ```json
 {
   "detail": {
     "eventName": ["PutObject", "CompleteMultipartUpload"],
     "resources": {
       "type": ["AWS::S3::Object"],
       "ARN": [{"wildcard": "arn:aws:s3:::production-collection-data/*.sqlite3"}]
     }
   },
   "source": ["aws.s3"]
 }
 ```
 * We agreed to go ahead with the proposed changes but also noted that the input parameters used by these jobs would
 need to be changed since the bucket name and key are no longer available separately but only as part of the overall S3
 Object ARN.  The knock-on effect is that the ECS tasks using these EventBridge triggers also need to be adapted to
 work with an ARN instead of a separate bucket name and bucket key.

 * The following changes have been made:
   * [digital-land/tiles-builder/pull/15](https://github.com/digital-land/tiles-builder/pull/15)
 * The EventBridge trigger for tiles-builder was changed manually in the development environment and tested by updating
 one of the dataset sqlite files.

**On (2024-07-17)**

 * Next, the Terraform changes for the EventBridge rule must be made.  Since all EventBridge rules are managed as a collection by the same module, it became apparent that it would also be necessary to adapt the other ECS tasks for the ARN parameter:
    * [digital-land/digital-land-postgres/pull/16](https://github.com/digital-land/digital-land-postgres/pull/16)
    * [digital-land/digital-land-efs-sync/pull/4](https://github.com/digital-land/digital-land-efs-sync/pull/4)
 * The Terraform change was applied to the development environment and tested before proceeding to production.
   * Staging environment was skipped since it was occupied with an ongoing development change which wasn't quite ready for production yet
 * The Terraform change was applied to production, and the following ECS task images were published to ECR in production:
   * tiles-builder
   * digital-land-postgres (ECS task named sqlite-ingestion)
   * digital-land-efs-sync (usually just referred to as efs-sync)
 * The S3 upload event was tested first on a smaller dataset: agricultural-land-classification-collection
   * All three ECS tasks were triggered normally and succeeded
 * Unfortunately the first few attempts to upload the title-boundary dataset (15 GiB) (to trigger an S3 upload event) failed due to authentication session timeouts

**On (2024-07-18)**

 * 7:30 - First upload failed (about 75% the way through) due to authentication session timeouts again
 * 9:30 - Thankfully the second upload of the day succeeded (14.9 GiB)
 * All ECS tasks were fired after the S3 upload event, including the critical datasette-tiles-builder task.  However, it seems hashing has prevented it from proceeding to write data…

```
2024-07-18T09:56:21.658+01:00	890a0155-8d5e-4d64-a4ba-9b1b70b68dbb: running with settings: S3_BUCKET=production-collection-data, S3_KEY=title-boundary-collection/dataset/title-boundary.sqlite3, DATABASE=title-boundary.sqlite3, DATABASE_NAME=title-boundary
2024-07-18T09:56:21.658+01:00	890a0155-8d5e-4d64-a4ba-9b1b70b68dbb: checking lock
2024-07-18T09:56:21.661+01:00	890a0155-8d5e-4d64-a4ba-9b1b70b68dbb: no current lock-title-boundary
2024-07-18T09:56:21.674+01:00	890a0155-8d5e-4d64-a4ba-9b1b70b68dbb: removing existing temporary tiles
2024-07-18T09:56:21.679+01:00	890a0155-8d5e-4d64-a4ba-9b1b70b68dbb: attempting download from s3://production-collection-data/title-boundary-collection/dataset/title-boundary.sqlite3
2024-07-18T09:59:02.788+01:00	890a0155-8d5e-4d64-a4ba-9b1b70b68dbb: finished downloading from s3://production-collection-data/title-boundary-collection/dataset/title-boundary.sqlite3
2024-07-18T09:59:02.799+01:00	890a0155-8d5e-4d64-a4ba-9b1b70b68dbb: building tiles
```

 * Added a new flag parameter to the datasette-tiles-builder task to control whether a hash check should be performed.
    * Disabling the check can be useful in the scenario where a rebuild of tile data is required even when SQLite data has not changed.
 * After deploying the new version of datasette-tiles-builder task, it was triggered manually by creating an ECS task.
    * The manual trigger included the new flag to disable the hash check
 * Unfortunately, despite skipping the hash check, a new problem materialised with generating a hash of the SQLite file
   * The root cause of this problem is not known.  Low disk space might be one issue.  No error materialised in logs.
   * Instead of addressing the root cause, it was decided that an option would be introduced to disable hash generation.
 * Another new flag parameter was added to the datasette-tiles-builder task to control whether hash generation should be performed.
    * Disabling the check can be useful in the scenario where a rebuild of tile data is required even when SQLite data has not changed.
 * After deploying the new version of datasette-tiles-builder task, it was triggered manually by creating an ECS task.
    * Thankfully, this time the task succeeded.
    * Map tile data for title boundaries was written to EFS for Datasette Tiles and, ultimately, the Map website to use

#### Postmortem

Coming soon.  Postmortem session to be arranged by Gordon Matchett.

In the meantime, here are few thoughts from Chris C relating to some questions received via Slack:

*How long has this been happening?*

Unsure.  The problem occurred because AWS truncated event data, which was actually a knock on effect from the size
of the title boundary dataset.

*What was the impact on users?*

Title boundary data was not displayed on the Map search feature of the Planning Data website.

*How can we recognise this in the future?*

Get notified when an event-based ECS task fails to fire/execute.

*What steps are we taking to ensure it doesn't happen again, or we can respond more quickly?*

We could do the following:

 * add better error handling in the main shell scripts
 * setup an alarm and alert for when an event-based ECS task fails to fire/execute
 * setup another alarm and alert for when an event-based ECS task encounters an error
 * have smoke tests in production which check for the presence of expected datasets, e.g. ensure the map has some title boundaries

### Outage - Config data missing in datasette - 2024-07-08

#### In attendance

Async on Slack:

* Paul Downey
* Owen Eveleigh
* Chris Johns

#### Description

Paul Downey reported that the [datasette column table](https://datasette.planning.data.gov.uk/digital-land/column) only had three entries. There was a concern that this data may affect pipeline data, such as [brownfield land](https://github.com/digital-land/config/blob/main/pipeline/brownfield-land/column.csv).

#### Running log

**On (2024-07-08)**

* Paul Downey reported the issue on Slack.
* Owen Eveligh and Chris Johns began investigating. Owen began to look specifically at the brownfield land data to confirm the issue.

#### Postmortem

To be completed once incident closed.

### Outage - digital-land tables down on Datasette - 2024-07-04

#### In attendance

Async on Slack:

* Greg Slater
* Paul Downey
* Owen Eveleigh
* Ernest Man

#### Description

Greg Slater noticed that some of the digital-land tables were showing an "Invalid SQL" error when attempting to load on datasette. In particular, digital-land.organisation was noted as being down. The error page shown notes a "disk I/O error".

#### Running log

**On (2024-07-04)**

* Greg Slater reported the issue as a query on the Planning Data Slack channel.
* Multiple users confirmed that this was a widespread issue.
* Ernest Man and Owen Eveleigh were deployed to fix the issue.
* Four containers hosting datasette were restarted. Upon restart, the webpages were available.
* Owen Eveleigh reported that this was due to a glitch found as `digital_land.sqlite3` had caused very high CPU and memory usage on the containers, causing the SQL error to show
* At this stage, the incident was closed, although there will be additional monitoring over the subsequent days to confirm no repeat of the issue.

#### Postmortem

* This incident was unexpected and deemed to be of a low risk of reoccurence.
* The primary concern was that the incident was not known until anecdotally discovered by the team.
* A [ticket](https://trello.com/c/Y6VWQ3E1/3341-create-canaries-and-alerting-for-digital-land-key-tables) has been raised in the backlog to introduce canaries and other alerts to some of the key digital-land database tables. Once completed, these should alert the relevant teams that they are returning an error.

### Organisation-collection is not updating local authority data  - 2024-06-24

#### In attendance

Async on slack:

* Paul Downey
* Owen Eveleigh
* Chris Johns

#### Description

Paul Downey made some changes to the local-authority.csv to update the regions of local authorities. After the pipeline process ran for two days, the data was not being updated on Datasette or planning.data.gov.uk.

#### Running log

**On (2024-06-25)**

* Paul Downey encountered the issue the previous day and reported it on the Slack channel.
* Chris Johns investigate the issue and believed it was connected to a prior piece of work.
* Owen Eveleigh and Chris Johns identified the ikely cause of the issue was due to update to the data being incorrect. Entry-date field had been included previously where it should not have been.
* Owen Eveleigh made the decision that to fix this issue, we would remove entry-date from all organisation csv files (including local-authority.csv) and we will retire all the resources that contain the entry-date column, as these contain the error.

**On (2024-06-26)**

* Chris Johns removed the entry-date from the files. 
* A second issue was discovered relating to how the organisation.csv file is generated. The recent change downloads the files used to generate it from AWS. However caching of the files meant that this could download outdated copies rather than the ones just generated. 
* This step was then modified to get files directly from the S3 bucket.

**On (2024-06-27)**

* Chris Johns reported that the overnight process had worked correctly and as expected. 
* The incident was closed at this time, however enhanced monitoring will continue for the next few days, especially when we are notified that a data change is being made.
* A RCA and postmortem will be led by Gordon Matchett, and updated below.

#### Postmortem

* To be completed by Gordon Matchett.

### Planning.data.gov.uk 502 encountered when loading entity  - 2024-06-07

#### In attendance

* Paul Downey
* Samriti Sadhu

#### Description
An issue was reported via Slack concerning a 502 error encountered when accessing specific entities on the platform. 
Upon investigation, it was observed that the error occurred due to the excessively large data size of certain entities, 
particularly Flood Risk Zone entities.


#### Running log

* On June 7, 2024, Paul Downey encountered the issue and reported it on the Slack channel, specifically for the 
entity: https://www.planning.data.gov.uk/entity/65135927.
* Samriti Sadhu investigated the issue and observed that it occurred specifically for Flood Risk Zone entities 
where the data volume was excessively large. This was confirmed by accessing the entity data in
JSON format: https://www.planning.data.gov.uk/entity/65135927.json.
* A ticket is created in Trello to address and optimize the loading of large data sets.
* Implemented self-contained HTML error pages that will be served by CloudFront. This ensures the page fails graciously
* To optimize the page, it was decided that the GeoJSON tab content will be loaded only when the GeoJSON tab is clicked


### Planning.data.gov.uk Data Replaced With Empty Fields - 2024-05-03

#### In attendance

* Kena Vyas
* Owen Eveleigh

#### Description

Reports in slack of data no longer being available on the platform. It became clear that a change to the python library
had resulted in all of the information except the entity number being removed from the entities. 

#### Running log

* Owen and Kena investigated the issue identifying the cause.
* Owen and Kena reverted the change and reprocessed the data.
* 2024-05-07 issue still present for the title boundary data. This was due to another underlying issue
caused by how events trigger in AWS. 
* Owen manually triggered the re-processing of title boundary data in all three environments leading to the
data being present on the site.

#### Postmortem
* Review of the changes made will take place including improving acceptance and unit tests which did not pick up on the fault.
* Ticket to be made regarding improving the triggers in AWS for large files which do not contian the right meta data.


### Planning.data.gov.uk Maps Down - 2024-04-12

#### In attendance

* George Goodall
* Ernest Man
* Owen Eveleigh

#### Description
Failed canaries was first reported in the planning-data-platform slack channel on the morning of 12 April 2024. The maps were down and the alarms were triggered.
 
#### Running log

* Ernest noticed the triggered alarms and found that the error was due to maplibre not being found in the client side javascript. he then contacted Owen and George. around 9.55 
* George started investigating the issue at 10.00. shortly after he found the issue was to do with https://unpkg, where we were fetching the maplibre library from.
* George then developed a hotfix involving obtaining maplibre via npm and using rollup.js to bundle the library into the client side javascript.
* The hotfix was deployed around 11.30am and the maps were back online.

#### Postmortem
* This issue arose due to importing the javascript directly from the CDN, bundling the library into the client side javascript resolved the issue.
* Going forward we need to address other imports from CDNs to prevent similar issues. both for javascript and css.


### Datasette Tiles outage - 2024-04-08

#### In attendance

* Ernest Man
* Owen Eveleigh

#### Description
Failed canaries was first reported in the planning-data-platform slack channel on 08 April 2024 around 9:20am. It then resolved and raise 
new alarm again at 10:10am.
 
#### Running log

* Ernest started investigation around 9:50am. RDS & EFS resources seems all fine. However, the ECS tasks keep failing in healthcheck
which causes the task to restart.

Main symptoms:

* Slowness and error 504 for datasette tiles 
* ECS tasks healthcheck keep failing which causes the tasks to restarts

Summary of the issue: The datasette tile outage was caused by the Memory utilization reached close to 100%. And we can see the following sqlite3 error
in logs.

```
ERROR: conn=<sqlite3.Connection object at 0x7f916c753120>, sql = ‘\n    select\n      columns.database_name,\n      
columns.table_name,\n      group_concat(columns.name) as columns\n    from\n      columns\n    where\n      
columns.table_name = “tiles”\n    group by\n      columns.database_name,\n      columns.table_name\n    
order by\n      columns.table_name\n    ’, params = None: database table is locked: columns
```

```
sqlite3.OperationalError: database table is locked: columns
```

#### Postmortem
* Seems something happened which cause the sqlite table locked
* ECS task have now upgrade to additonal 3 instance of .098 vCPU & 1GB. There should not be any additonal cost implications 
as we are using the cluster spare resources, but a long term plan should consider for vertical scaling. 
* Ernest will continous monitoring any issue.

**On (2024-04-09)**

* Datasette tiles are running fine in Production



### Datasette & Datasette Tiles outage - 2024-02-06

#### In attendance

* Ernest Man
* Chris Cundill

#### Description
Failed canaries was first reported in the planning-data-platform slack channel on 06 Feb 2024 around 1am when the Collection ran. 
Users also reported error 502 around 9am. in the morning.

#### Running log

* Ernest started investigation around 9am. I think this is related to the EFS throguhtput mode changes on 05 Feb 2024 [ticket](https://trello.com/c/HcQDkZf4) as we have previously downgraded 
the throguhtput mode from "Elastic" to "Bursting".

Main symptoms:

* Slowness and error 502 for datasette and datasette tiles 
* EFS Throughput utilization reached 100%

Summary of the issue: The datasette outage was caused by the EFS throughtput reached 100% threshold. We have roll back the throguhtput
mode changes and both datasette servcies are back online at 9.20am.

#### Postmortem

* Discussion between Owen, Chris and Ernest already started last week on a long term solution for this EFS issue.

**On (2024-02-07)**

* Both datasette services are running fine in Production. In additon, the EFS throughtput is now running about 20%.


### Planning.data.gov.uk outage - 2023-10-05

#### In attendance

Async on slack:

* Ernest Man
* Owen Eveleigh

#### Description

During the Bug Party on the morning of 05th October 2023, the Development and Design teams (around 11 people) were carried out some testing for the planning data site 
with different browser/device. Slowness of the site first reported around 15mins in and the first aws canary test failed at 11:27am. The outage was 
around 10-15 mins.

#### Running log

* Ernest and Owen started investigation at around 11:30am. We getting time out error for the site. The issue seems related to the aws rds database.
* Ernest and Owen have look at varies area in the production platform, inclued ECS, RDS postgres database etc.

Main symptoms:

* Slowness of the planning data site
* time out error on the site
* Search doesn't work


Summary of the issue: The aws rds reader instance is running out of local storage. With the current DB instance class "db.t4g.large" which 
has 16GB maximum temporary storage available. More info [here](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.Managing.html#AuroraPostgreSQL.Managing.TempStorage)

ERROR: could not write to file "base/pgsql_tmp/pgsql_tmp13706.0": No space left on device

#### Postmortem

* [Bug ticket](https://trello.com/c/chJL4wsR) have been created.
* Additional reader instance have been temporary added to production cluster.
* Dev team is looking at optimize the search query
* Ernest will continous monitoring any databse issue.


### National map url 'dataset' parameter key changed to 'layer' - 2023-10-02

#### In attendance

Async on slack:

* George Goodall
* Paul Downey

#### Description

At 5.09 on Friday the 29th of September, Paul Downey posted in the main Slack channel that the url param key for the dataset has changed from dataset to layer. He advised that this needed reverting, and any urls pointing to the old key needed to be redirected.

Example of original format:

`https://www.planning.data.gov.uk/map/?dataset=infrastructure-project`

Example of new, unexpected format:

`https://www.planning.data.gov.uk/map/?layer=infrastructure-project`


#### Running log

* George started investigations at 9.11am on the 2nd October, finding that the specified key for the dataset param had
been overwritten as part of the refactor/map component update here: https://github.com/digital-land/digital-land.info/pull/133

* An initial fix was deployed at 10.35am that reverted the key back to dataset, and added a function to change any urls with the old key to the new key. 

* A second PR was deployed at 11.08am that added a test to check that the url param key was correct and that the old key was correctly changed to the new key.

* These changes were reviewed, approved and merged by Mark at 11:08 and available on the live site a few minutes later.

#### Impact

Links with the now non-functioning format had gone out as a part of the weeknote shared by senior management, including to a minister-level audience. Matt Lucht identified a quick workaround, to make a new URL that included both sets of data:

`https://www.planning.data.gov.uk/map/?dataset=infrastructure-project&layer=infrastructure-project`

#### Analysis

We did not appreciate that people were using and sharing the direct link off the browser to access the map.

When applying updates to the map code, we overwrote the section that specified the `dataset` url param key and replaced it with `layer`. This change was not picked up in manual testing or code reviews. There were no automated tests covering this case, and as the change was inadvertent, we did not write any new ones.

### Post incident actions

We are implementing a better set of automated tests to reduce the likelihood of this happening again. 

#### Lessons to be learned

The original change came in as part of a much largeer set of code changes. It was not noticed in code review. Code reviews are not as effective when dealing with extensive changes. Next time, let us find ways to not create large pull-requests with hundreds of lines of changes. 

### maptiler started returning 403 errors - 2023-08-16

#### In attendance

Async on slack:

* George Goodall
* Martin Grey

#### Description

Early afternoon on 16th October 2023, Martin noted that the national map was not loading correctly. George then investigated further and found that the maptiler service was returning 403 errors.

#### Running log

**on (2023-08-16)**

* George started investigations around 3pm. He found that the maptiler service was returning 403 errors. with attached body ```Invalid key - Get your FREE key at https://cloud.maptiler.com/account/keys/```

* Paul Smith is the only person with access to the maptiler account. As he is on leave we can not investigate further to discover the cause of this issue.

* A [temporary fix](https://github.com/digital-land/digital-land.info/pull/140) was merged  by George that swapped out the paid map for an open one and replaced the key with his own personal one. 

### aws alarms raised for datasette and datasette-tiles canaries - 2023-08-14

#### In attendance

Async on slack:

* Ernest Man
* Owen Eveleigh

#### Description

On the morning of 14th August 2023 when Ernest logged on around 9am in the morning and noticed the aws alarms was raised in our 
slcak channel for datasette and datasette-tiles. Getting 502 error for both endpoints and diagnostic procedures started at that point.

#### Running log

* Ernest and Owen started investigation at around 9am. We getting 502 when we hit those endpoints directly. The issue seems only 
affecting Production environment as we cannot see the same in the lower environments (Dev and staging). So we suspect this is more of 
a platform related issue.

* Ernest and Owen have look at varies area in the production platform, inclued ECS, collection pipeline, RDS postgres database etc.

Main symptoms:

* both datasette and datasette-tiles applications crashed in prod leading to a 502 bad gateway
* ECS task is unable to launch any new instances as they do not pass health checks
* National map may not be able to access our tiles
* Fact pages on the site will be unavailable
* Reporting may be affected as cannot access production datasette

Summary of the issue: The EFS throughput is too high during the nightly data update. This caused by the 
pipeline dumped files and datasette applications restarting.

#### Postmortem

* [Live incident ticket](https://trello.com/c/KNB7k4ee) have been created.
* EFS have now upgraded to use "Elastic" throughput mode.
* Ernest will continous monitoring any cost implications in aws Cost Explorer

**On (2023-08-14)**

* a temporary fix have been implemented by reducing the 2 ECS services which uses the EFS storage to 0, allow EFS to 
move to a normal throughput, an then reinstate the applications. Both datasette and datasette-tiles seems to back online
in the evening and canaries also reported positive test results.

**On (2023-08-15)**

* The datasette alarms was also rasied around 1:05am and it seems the EFS throughput still very high in Production when the 
collection pipleine run, so we start looking for a more permanant solution.

The current EFS file system is using “Bursting“ throughput mode. It means the application is throughput-constrained 
(i.e. if it uses more than 80% of the permitted throughput or we have used up all burst credits). 
The burst credits was used up (near 0) when the collection pipeline runs.

We decided to upgrade the EFS to use “Elastic” throughput mode instead. In contrasts to the burst credits way of Bursting 
throughput mode, Elastic throughput mode of EFS automatically scales throughput performance up or down to meet the needs 
of the workload activity. Elastic throughput can drive up to 3 GiBps for read operations and 1 GiBps for write operations 
per file system.

We upgraded the EFS to use “Elastic” throughput mode in the afternoon.

**On (2023-08-16)**

* No alarms have been raised this morning and all canaries seems running fine.
* The EFS throughput are healthy too
* ECS tasks are all running fine
* We will continous monitoring the platform and the additional cost implications if any.

**On (2023-08-17)**

* No alarms have been raised and all canaries seems running fine.
* The EFS throughput are healthy as yesterday
* We noticed the EFS cost increased by around $8 per day, so decided to re-enable “Bursting“ mode 
for (Dev and Staging) environments to save cost.



### Documentation section on planning.data.gov.uk showing error - 2023-06-12

#### In attendance

Async on slack:

* Swati Dash
* Owen Eveleigh
* Ernest Man
* Mark Smith

#### Description

On the morning of 12th June 2023 at 09:55a.m. Swati reported the planning data site Documentation section is showing error. 

#### Running log

* Ernest and Mark started investigation at around 10am. We cannot see any issue from the infrastructure side and the error 
seems to have appear in the lower environments (Dev and staging) too. So we suspect this is a coding issue and Mark have started 
to investigate this matter further. 

Summary of the issue: The robots.txt server route did not explicitly tell Fast API to exclude it from application API schema.
Mark have rasied a PR to address the issue.

#### Postmortem

* Mark PR [hotfix](https://github.com/digital-land/digital-land.info/pull/119)
* [Live incident ticket](https://trello.com/c/63K0MDi3) have been created.
* Ernest now included "/docs" in the canary test, [ticket](https://trello.com/c/mNoSqt17) also created.

**On (2023-06-14)**

* The Documentation section is showing without any error, we have also implemented canary test for checking the /doc endpoint.


### Slowness reported on planning.data.gov.uk - 2023-06-01

#### In attendance

Async on slack:

* Warren Hobden
* Ernest Man
* Mark Smith
* Adam Shimali

#### Description

On the morning of 1st June 2023 at 10:15a.m. User reported the planning data site slowness and the Entity & Dataset API endpoints are also affected 
by intermittent 500 error and diagnostic procedures started at that point. In addition, PlanX also seems impacted by the same issue and they reported
on Friday 2nd June 2023.

#### Running log

* Ernest, Mark and Adam have done some detailed investigation as we are seeing this similiar issue second time. The first incident happened in April 2023
when we initially thought it was due to an auto minor databse version upgrade by aws as it happen around the same time when we have the outage.

The postgres RDS database (Reader instance) was maxed-out on CPU due to the following error and query. 

```
ERROR:  could not write to file “base/pgsql_tmp/pgsql_tmp31290.8”: No space left on device
2023-06-01 11:51:47 UTC:10.0.24.253(34156):root@planning:[31290]:ERROR: could not write to file 
“base/pgsql_tmp/pgsql_tmp31290.8": No space left on device
```

```
2023-06-01 11:51:47 UTC:10.0.24.253(34156):root@planning:[31290]:STATEMENT:  
SELECT ST_AsGeoJSON(entity.geometry) AS “ST_AsGeoJSON_1”, ST_AsGeoJSON(entity.point) AS “ST_AsGeoJSON_2", 
entity.entity AS entity_entity, entity.name AS entity_name, entity.entry_date AS entity_entry_date, 
entity.start_date AS entity_start_date, entity.end_date AS entity_end_date, entity.dataset AS entity_dataset, 
entity.json AS entity_json, entity.organisation_entity AS entity_organisation_entity, entity.prefix AS entity_prefix, 
entity.reference AS entity_reference, entity.typology AS entity_typology, ST_AsEWKB(entity.geometry) AS entity_geometry, 
ST_AsEWKB(entity.point) AS entity_point, count(entity.entity) OVER () AS count
FROM entity ORDER BY entity.entity
LIMIT 10 OFFSET 536990
```

Summary of the issue: We use a limit/offset query to provide paginated access to the data. 
We're seeing very large offsets (greater than 500,000) which looks like a search engine or similar 
is crawling through the entity pages. Large offsets cause inefficiencies for the database, 
which is we believe the cause of the problem you are seeing with the site being down.

#### Postmortem

* We have temporary increased the number of database reader nodes in Production, which seems to have addressed the issue in the short term.
* Adam has re-write the [entity query](https://github.com/digital-land/digital-land.info/pull/114/files) so it does not use limit/offset.
* Mark has also added a [robots.txt](https://github.com/digital-land/digital-land.info/pull/116/files) file which can be used to ask search engine crawlers to exclude certain parts of the web site.
* [ticket](https://trello.com/c/QEGoMUqk) have been created to enabled database auto scaling in production.
* [Live incident ticket](https://trello.com/c/qmoKooTm) also created.

**NEXT DAY (2023-06-02)**

* After we have increased the number of reader nodes in the morning and it seems the site is running fine.
* The team continuous monitoring the production database server/logs and the planning site.
* We also deployed the robots.txt PR into Development for further testing.

**On (2023-06-05)**

* The planning data site seems back to normal
* Testing [database auto scaling](https://github.com/digital-land/digital-land-infrastructure/pull/65/files) in development environemt and ready for deploy into production.
* Testing robots.txt in development environment
* Paul Downey rasied a point about malicious usage, he mentioned datasette has similar restrictions on the size of a result set got returned. 
we will look at this and put some restrictions around it.

**On (2023-06-06)**

* The RDS database auto scaling is now deployed to production and the planning data site seems running fine.
* New [Synthetics Canaries ticket](https://trello.com/c/mNoSqt17) created to included the following backend API endpoints. https://www.planning.data.gov.uk/entity.json?limit=10 
and https://www.planning.data.gov.uk/dataset.json

**On (2023-06-08)**

* The planning site continous to run fine with averaging around 20% database CPU utilization and we have also included the robots.txt changes.


### Getting error 500 on planning.data.gov.uk - 2023-04-11

#### Description

On the morning of 11th April 2023 at 7:34a.m. Paul Downey noted that the site getting intermittent 500 error and diagnostic
procedures started at that point. 

#### Running log

* Ernest and Owen have done a number of checks across the platform and noticed the postgres RDS database (Reader instance) was 
maxed-out on CPU due to the following query. This may caused by someone trying to download lots of data. 

```
2023-04-11 06:04:02 UTC:10.0.43.141(45314):root@planning:[22027]:STATEMENT: SELECT ST_AsGeoJSON(entity.geometry) AS “ST_AsGeoJSON_1", 
ST_AsGeoJSON(entity.point) AS “ST_AsGeoJSON_2”, entity.entity AS entity_entity, entity.name AS entity_name, 
entity.entry_date AS entity_entry_date, entity.start_date AS entity_start_date, entity.end_date AS entity_end_date, 
entity.dataset AS entity_dataset, entity.json AS entity_json, entity.organisation_entity AS entity_organisation_entity, 
entity.prefix AS entity_prefix, entity.reference AS entity_reference, entity.typology AS entity_typology, 
ST_AsEWKB(entity.geometry) AS entity_geometry, ST_AsEWKB(entity.point) AS entity_point, count(entity.entity) OVER () AS count
FROM entity ORDER BY entity.entity
LIMIT 10 OFFSET 569100
```

#### Postmortem

* Ernest implemented an [aws alarm](https://eu-west-2.console.aws.amazon.com/cloudwatch/home?region=eu-west-2#alarmsV2:alarm/production-rds-alarm?) for the postgres database's CPU when it reached above 60% threshold.
* A new [ticket](https://trello.com/c/DaXtE5v0) have been created to look into this issue in more details. 


### All applications on planning.data.gov.uk - 2022-11-22

#### In attendance

Async on slack:

* Paul Downey
* Lawrence Goldstien
* Paul Smith

#### Description

On the morning of the 22nd the decision was taken to switch over to the new infrastructure setup in the production
account. We made preparations by adding a service outage banner to the application as we were aware that some downtime
would be experienced while DNS updated globally. After the switchover Lawrence was able to access the new infrastructure
so assumed everything was going to plan. At 2:45pm Paul Downey noted that the site was not accessible and diagnostic
procedures started at that point.

#### Running log

* GDS contact confirmed the DNS change had been actioned at 2:15pm
* Lawrence observed that the datasette and datasette tiles applications were available on the new domain at 2:20pm
* Lawrence observed that the main application was available at 2:35pm
* Paul Downey observed that the site was still not accessible for him and posted the results of a dig on the main
    application domain at 2:50pm
* Lawrence used the site https://www.whatsmydns.net/#NS/planning.data.gov.uk to check for propagation and noted that
    most DNS servers had updated to the new environment at 3pm
* Paul Downey observed that the website worked for him at 4pm
* Lawrence and Paul Downey observed that the site was working intermittently from 4pm to 6pm.

**NEXT DAY (2022-11-23)**
* Paul Downey observed that the site worked for him when tethered to his phone but saw that one in three runs of dig
    against the domain returned empty results at 9am
* Paul Downey posted into the digital planning slack to advise that we thought the change went through and to let the
    team know of any issues at 9am
* Lawrence observed that some DNS servers had longer TTLs for the domain compared to the current and old DNS records
    TTLs of 24 hours at 1pm
* The decision was made to wait out the full 48 hours of TTL and continue work to solve the issues afterwards at 1:30pm

**NEXT DAY (2022-11-24)**
* Paul Downey noted that the DNS responses where still not returned consistently when running a dig command at 8:30am
* Lawrence ran some diagnostics against a selection of public DNS servers and noted that the data.gov.uk domain has two
    sets of DNS servers: AWS and Google Cloud. Lawrence found that running a dig against AWS servers for the domain
    returned details for the new domain whereas running a dig against the Google Cloud returned no results at 10am
* Lawrence drafted a message to be sent to GDS detailing the issues with the Google Cloud nameservers at 10am
* GDS confirmed the issue and confirmed they had synced AWS and Google Cloud nameservers at 11:50am
* Paul Downey observed that the site was up and running for him at 11:55am
* Lawrence completed further checks and noted that most global DNS servers had updated to the new infrastructure at 12pm

#### Postmortem

We felt the team reacted well to this outage and stakeholders were understanding of the downtime.

Paul Smith developed a pattern for service status messages to users and added feedback to the
[GOV.UK Design system](https://github.com/alphagov/govuk-design-system-backlog/issues/266).

In reflection the team could have recognised the issues sooner and checked more details of the DNS configuration.

We could have offered the old address https://digital-land.info to OSL and other groups as a fallback while the system
was down.