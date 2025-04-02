# Monitoring Data Quality

This page explains the processes we follow to fix data quality issues that we actively monitor for.

Each of these sections covers a different issue, each of which are defined by our [data quality requirements](https://docs.google.com/spreadsheets/d/1kMAKOAm6Wam-AJb6R0KU-vzdvRCmLVN7PbbTAUh9Sa0/edit?gid=2142834080#gid=2142834080&fvid=1368636333).

## Unknown entities

To keep the datasets up-to-date on the platform, we need to check “unknown entity” issues every week and assign entities.
The unknown entities issue usually occurs when an LPA updates their data on the endpoint we are retrieving and adds new records. These records will have reference values we do not have on the platform, hence when the system realises the new data has been added and the references of those new data are not on the platform, it will trigger an unknown entity issue.

The recommended steps to resolve this are as follows:

1. Download the issues report for [ODP datasets](https://config-manager-prototype.herokuapp.com/reporting/odp-summary/issue) or [all datasets](https://config-manager-prototype.herokuapp.com/reporting/download?type=endpoint_dataset_issue_type_summary).
2. Download the CSV file with ‘Download Current Table’ which will download a file called `odp_issues`
3. Analyse the "unknown entity" issues. Look for `issue_type` with `unknown entity`
4. If possible, for each of the issues you have identified, follow the steps in [Assign entities](../../How-To-Guides/Maintaining/Assign-entities). Keep track of the row of the issue.
5. Raise a PR and merge it
6. Once merged, run the issue report again and check if the previous unknown entity is resolved. Paste the row of “unknown entity” issues you have tracked in [this google docs](https://docs.google.com/spreadsheets/d/1gZ_SIx9jdko_aD3QRZUJh39PdNHISS1N/edit?usp=drive_link&ouid=105995804157199974210&rtpof=true&sd=true) after the changes are merged on the platform.
7. Note in the sheet if you are not able to assign entities for any LPA
8. Insert a new workbook with the next sprint date

Success criteria:
Ideally, the number of unknown entity errors should be zero after completing the above steps.

## Check deleted entities

To keep the datasets up-to-date on the platform, we need to check entities that have been deleted from the latest resource every week. This occurs when the LPAs have deleted the entities on their endpoint but not told us. Once we have confirmed which entities have been deleted, we contact the LPAs to make sure. Once we have received confirmation, we can retire the entities.

The recommended steps to resolve this are as follows:

1. Run the [this report](https://colab.research.google.com/github/digital-land/jupyter-analysis/blob/9f29d13f56ba40f476a28947fd03f6c123d7a04f/service_report/Compare_entity_count.ipynb#scrollTo=f8c51819-c013-4473-a08d-140fe69d6bd7)
2. For each dataset, compare the `Latest resource entity count` with the `Platform entity count`. Make note of which dataset has more counts for the platform compared to the latest resource.
3. List those that need to be retired [here](https://docs.google.com/spreadsheets/d/1M1Zj_iuYFmd5d29TBUFo6lyaQpeylbnI/edit?usp=sharing&ouid=118336900984695995103&rtpof=true&sd=true). You will want the collection, endpoint, and source.
4. The LPAs will need to be contacted. Once confirmed that these were deleted, follow the [retire entities process](../../How-To-Guides/Retiring/Retire-entities)
5. Note in the sheet if an entitiy could not be retired

Success criteria:
The count of entities on the platform and on the latest resource should be the same. Run the report to make sure that the counts are matching.

## Retire broken, non-primary endpoints

### Trigger
We define an endpoint as "broken" once it has been logged with a non-200 status for more than 30 consequtive days. We pro-actively end-date broken endpoints and their sources when they are not the primary endpoint for a provision, i.e. the endpoint is not the only or most recently added endpoint for a provision.

> e.g. 
> Wiltshire council has two active `brownfield-land` endpoints, one added in 2025 and one added in 2024. This makes the 2025 endpoint the primary endpoint. The 2024 endpoint has had a 404 status for 62 days, so it should be given an end-date. 

> NOTE
> This applies to all datasets, including ODP, statutory and single-source.

### Task
1. Identify broken, non-primary endpoints through [this datasette query](https://datasette.planning.data.gov.uk/digital-land?sql=--+count+endpoints+and+their+statuses+per+org+and+dataset%0D%0AWITH+endpoint_status_series+as+%28%0D%0A%0D%0A+++SELECT+organisation%2C+name%2C+pipeline%2C+collection%2C+endpoint%2C+status%2C+resource%2C+latest_log_entry_date%2C+endpoint_entry_date%2C+endpoint_end_date%2C%0D%0A++++++dense_rank%28%29+over+%28partition+by+organisation%2C+pipeline+order+by+endpoint_entry_date+desc%2C+endpoint%29+as+endpoint_no%2C%0D%0A++++++dense_rank%28%29+over+%28partition+by+endpoint+order+by+latest_log_entry_date+desc%2C+status%29++as+status_no%0D%0A+++FROM+reporting_historic_endpoints%0D%0A+++ORDER+BY+name%2C+endpoint_entry_date+desc%0D%0A++%0D%0A%29%2C%0D%0A%0D%0A--+get+latest+200+status+for+all+endpoints%0D%0Alatest_log_entry+AS+%28%0D%0A++SELECT%0D%0A++++endpoint%2C%0D%0A++++MAX%28latest_log_entry_date%29+AS+latest_200_log_entry_date%2C%0D%0A++++CAST%28julianday%28%27now%27%29+-+julianday%28MAX%28latest_log_entry_date%29%29+AS+int64%29+as+n_days_since_last_200%0D%0A++FROM%0D%0A++++reporting_historic_endpoints%0D%0A++WHERE%0D%0A++++status+%3D+%27200%27%0D%0A++GROUP+BY%0D%0A++++endpoint%0D%0A%29%0D%0A%0D%0A--+get+all+non-latest%2C+un-end-dated+endpoints+with+a+latest+status+that%27s+not+200+where+it%27s+been+%3C+90+days+since+last+200+status%0D%0ASELECT+%0D%0A+++es.*%2C%0D%0A+++l.latest_200_log_entry_date%2C%0D%0A+++l.n_days_since_last_200%2C%0D%0A+++s.source%0D%0A++%0D%0AFROM+endpoint_status_series+es%0D%0ALEFT+JOIN+latest_log_entry+l+ON+es.endpoint+%3D+l.endpoint%0D%0ALEFT+JOIN+source+s+on+es.endpoint+%3D+s.endpoint%0D%0AWHERE+1%3D1%0D%0AAND+es.endpoint_no+%21%3D+1%0D%0AAND+es.status_no+%3D+1%0D%0AAND+es.status+NOT+LIKE+%222%25%22%0D%0AAND+es.endpoint_end_date+%3D+%22%22%0D%0AAND+l.n_days_since_last_200+%3E+30).
2. Download the query results as a scv file called `retire.csv` in the root of your local `config` directory.
4. Run the following command:

```
digital-land retire-endpoints-and-sources retire.csv
```

### Test
Once the changes have been merged into main, the endpoints and sources you retired should no longer appear in the datasette query results.

## Identify new data sources for broken, primary endpoints
### Trigger
We define an endpoint as "broken" once it has been logged with a non-200 status for more than 30 consequtive days. And we call an endpoint a "primary" endpoint when it is the most recently added, or the only endpoint for a provision.

> e.g. 
> * the `archaeological-priority-area` dataset has one endpoint; this is the primary endpoint
> * the `local-authority-district` dataset has 3 active endpoints; the most recently added one is the primary endpoint

For ODP datasets, endpoint errors are raised back to data providers through the Submit service so we don't need to do anything.

However, when non-ODP datasets have broken, primary endpoints we should search for alternatives.

### Task
1. Identify broken, primary endpoints through [this datasette query](https://datasette.planning.data.gov.uk/digital-land?sql=--+count+endpoints+and+their+statuses+per+org+and+dataset%0D%0AWITH+endpoint_status_series+as+%28%0D%0A%0D%0A+++SELECT+organisation%2C+name%2C+pipeline%2C+collection%2C+endpoint%2C+status%2C+resource%2C+latest_log_entry_date%2C+endpoint_entry_date%2C+endpoint_end_date%2C%0D%0A++++++dense_rank%28%29+over+%28partition+by+organisation%2C+pipeline+order+by+endpoint_entry_date+desc%2C+endpoint%29+as+endpoint_no%2C%0D%0A++++++dense_rank%28%29+over+%28partition+by+endpoint+order+by+latest_log_entry_date+desc%2C+status%29++as+status_no%0D%0A+++FROM+reporting_historic_endpoints%0D%0A+++ORDER+BY+name%2C+endpoint_entry_date+desc%0D%0A++%0D%0A%29%2C%0D%0A%0D%0A--+get+latest+200+status+for+all+endpoints%0D%0Alatest_log_entry+AS+%28%0D%0A++SELECT%0D%0A++++endpoint%2C%0D%0A++++MAX%28latest_log_entry_date%29+AS+latest_200_log_entry_date%2C%0D%0A++++CAST%28julianday%28%27now%27%29+-+julianday%28MAX%28latest_log_entry_date%29%29+AS+int64%29+as+n_days_since_last_200%0D%0A++FROM%0D%0A++++reporting_historic_endpoints%0D%0A++WHERE%0D%0A++++status+%3D+%27200%27%0D%0A++GROUP+BY%0D%0A++++endpoint%0D%0A%29%0D%0A%0D%0A--+get+all+non-latest%2C+un-end-dated+endpoints+with+a+latest+status+that%27s+not+200+where+it%27s+been+%3C+90+days+since+last+200+status%0D%0ASELECT+%0D%0A+++es.*%2C%0D%0A+++l.latest_200_log_entry_date%2C%0D%0A+++l.n_days_since_last_200%2C%0D%0A+++s.source%0D%0A++%0D%0AFROM+endpoint_status_series+es%0D%0ALEFT+JOIN+latest_log_entry+l+ON+es.endpoint+%3D+l.endpoint%0D%0ALEFT+JOIN+source+s+on+es.endpoint+%3D+s.endpoint%0D%0A%0D%0AWHERE+1%3D1%0D%0AAND+es.endpoint_no+%3D+1%0D%0AAND+es.status_no+%3D+1%0D%0AAND+es.status+NOT+LIKE+%222%25%22%0D%0AAND+es.endpoint_end_date+%3D+%22%22%0D%0AAND+l.n_days_since_last_200+%3E+30%0D%0AAND+es.pipeline+in+%28SELECT+DISTINCT+dataset+FROM+provision_rule+WHERE+provision_reason+in+%28%22alternative%22%2C+%22authoritative%22%29%29).
2. For any broken endpoints, search the data provider's website for any newly published endpoint URLs (the source URL for the broken endpoint should take you to the correct site).
3. If you find any newer endpoints, add an end-date for the broken endpoint and source and follow the [adding data process](../Adding-Data) to add the new one.

### Test
Once the changes have been merged into main, the primary endpoint for the provision should no longer appear in the datasette query.


## Identify new data sources for stale endpoints
### Trigger
We define an endpoint as "stale" when it has not been updated with new data within the time period we expect. 

> e.g.   
> the [source](https://environment.data.gov.uk/dataset/04532375-a198-476e-985e-0579a0a11b47) of the latest endpoint we have for `flood-risk-zone` data published by the Environment Agency states that the dataset is updated quarterly. If the start date of the latest resource is 01/01/2024 and today's date is 30/06/24 there hasn't been an update for 6 months so we would say this endpoint is stale.


> NOTE  
> For our **compiled** datasets, local planning authorities are responsible for updating endpoints or publishing new ones for new datasets so we don't monitor for staleness.  
> 
> For our **single source** datasets (i.e. those with national coverage from a single data provider) we need to check whether we have added the most up to date data.

### Task
1. Check for any stale endpoints by running the [monitor frequency of datasets](https://github.com/digital-land/jupyter-analysis/blob/main/reports/monitor_frequency_of_datasets/monitor_frequency_of_datasets.ipynb) report. This will identify any endpoints which have not been updated within the expected time period.
2. For any identified datasets you should check to see whether the data provider has published more up to date data on a new endpoint. You can use the source of existing endpoints to find their website.
3. If you find a new endpoint you will need to add it. Check the [new endpoint for existing provision](../Adding-Data/#new-endpoint-for-existing-provision) scenario on the Adding data page to find the steps to follow in order to retire old endpoints, add the new one and assign any new entities if required.

### Test
Once you've added the new endpoint and merged the changes, re-run the [monitor frequency of datasets](https://github.com/digital-land/jupyter-analysis/blob/main/reports/monitor_frequency_of_datasets/monitor_frequency_of_datasets.ipynb) report; the dataset you've updated should no longer be in the list.

## Out of range entities

### Trigger
This is a configuration error where the entity numbers that have been used in a dataset are not within the range defined for that dataset. These issues will be raised in the issue report for [ODP datasets](https://config-manager-prototype.herokuapp.com/reporting/odp-summary/issue) or [all datasets](https://config-manager-prototype.herokuapp.com/reporting/download?type=endpoint_dataset_issue_type_summary), where the `issue_type` = "entity number out of range".

The entity range for datasets are defined in the [specification repository](https://github.com/digital-land/specification/tree/main/content/dataset), select a dataset to view its entity range, defined by the entity-minimum and entity-maximum fields.

### Task
In order to fix, for each dataset with issues you should:

1. Delete the entries in `lookup.csv` which are using an incorrect entity number, go to [Datasette](https://datasette.planning.data.gov.uk/) and select the relevant dataset. Next, filter the issue table using the `resource` and `issue_type` fields present in the downloaded issue table, then use the value field to identify the incorrect entity number. Now, find the incorrect entity number in lookup.csv and remove the entire row.

2. Follow the [assign entities](../../How-To-Guides/Maintaining/Assign-entities) process to assign new entity numbers and replace the deleted lookup entries.

### Test
Once fixed, there should no longer be any issues raised in the issue report.


## Invalid Organisations

One of our monitoring tasks is patching any `invalid organisation` issues that arise. This isually happens if the organisation value provided in the endpoint is wrong or missing e.g it could be a blank field or the wrong organisation name / identifier.

A list of invalid organisation issues can be optained by downloading the issue report for [ODP datasets](https://config-manager-prototype.herokuapp.com/reporting/odp-summary/issue) or [all datasets](https://config-manager-prototype.herokuapp.com/reporting/download?type=endpoint_dataset_issue_type_summary) and filtering for `invalid organisations` under `issue-type`.

To fix this, we can make use of the `patch.csv` file. More information on how this file works can be found in the pipeline/patch section in [configure an endpoint](../How-To-Guides/Adding/Configure-an-endpoint.md).

For example, if we were given the wrong `organisationURI` in a `brownfield-land` dataset, we can patch it by targetting the endpoint, give the current uri in the `pattern` section, and the desired uri in the `value` section like so:

```
brownfield-land,,OrganisationURI,http://opendatacommunities.org/id/london-borough-council/hammersmith-and-,http://opendatacommunities.org/doc/london-borough-council/hammersmith-and-fulham,,,,,890c3ac73da82610fe1b7d444c8c89c92a7f368316e3c0f8d2e72f0c439b5245
```
To test it, follow the guidance in [building a collection locally](../How-To-Guides/Testing/Building-a-collection-locally) but keep the new patch entry and focus on the desired endpoint.


## Organisational changes

When organisations are created or ended we need to:

* Create new organisation entities for any newly created organisations.
* Make entities for organisations which have been ended have an end-date.
* If appropriate, make sure any entities that any ended organisations were responsible for are moved to the new responsible organisations.

> Note, this guidance relates to local-authority organisation changes, which have the most impact on ODP datasets.

### Trigger

We will know that organisations need to be ended when changes are announced by [governing body]. These may involve multiple existing councils being replaced by a single unitary authority, or other variations of changes.

We may be notified of changes like this by team members, in which case we should act immediately.

Otherwise, the way we should make sure we check for any possible changes in order to be alerted is by monitoring updates to `organisation` typology datasets. If changes to local authority organisations are expected at least once each year, when the time between the latest resource start date and the current day's date is greater than a year we should check for any changes which need to be reflected in the dataset. This test is defined by data-quality need `T-05`.

### Task

1. Use the [dataset editor](https://dataset-editor.development.planning.data.gov.uk/dataset/local-authority) to add new records for new organisations. You may need to cross-reference some other datasets to add all the necessary details, for instance the ONS codes for the local authority and the local planning authority. 

2. Use the [dataset editor](https://dataset-editor.development.planning.data.gov.uk/dataset/local-authority) to add an end-date for any organisations which have been terminated. Use the end date from the official announcement.


The next step will vary depending on how the local authorities transition existing datasets to the new organisation.

#### If there is not a new endpoint from the new organisation

Sometimes it may take a long time for data to be transitioned to a newly created organisation. In which case the existing endpoints from the old organisation should be kept live and maintained until there is a new one for the new organisation, at which point the process below can be followed.


#### If there is a new endpoint from the new organisation

3. Follow the standard process for validating and [adding a new endpoint](../../Adding/Add-an-endpoint.md). During the [validation step](../../Validating/Validate-an-endpoint.md) use the duplicate check step to check for any duplicates with existing data. This should highlight any existing entities that the new records match to. For any matches, existing entity numbers can be used instead of the new ones generated by the `add-data` process. Any new entities from the new organisation which don't match can be given new entity numbers.

4. Any existing entities from the old organisation which haven't been matched to new records from the new organisation should be given an end-date [note: we don't currently have a process for this].

5. The entity-organisation range should be assigned to the new organisation for any of the entity numbers which are now being used for the new organisation's records.

6. [Retire any endpoints](../../How-To-Guides/Retiring/Retire-endpoints.md) for the old organisation's provisions so they are no longer collected.