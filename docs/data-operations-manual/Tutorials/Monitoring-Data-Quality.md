# Monitoring Data Quality

This section covers situations where we are monitoring the quality of data and fix any issues that have arisen.

## Unknown entities

To keep the datasets up-to-date on the platform, we need to check “unknown entity” issues every week and assign entities.
The unknown entities issue usually occurs when an LPA updates their data on the endpoint we are retrieving and adds new records. These records will have reference values we do not have on the platform, hence when the system realises the new data has been added and the references of those new data are not on the platform, it will trigger an unknown entity issue.

The datasets that require assigning entities are categorised into three main scopes:

ODP Datasets – These datasets are supported by ODP funding. Datasets categorised as ODP can be found here [ODP Data](https://datasette.planning.data.gov.uk/digital-land?sql=select+rowid%2C+dataset%2C+cohort%2C+notes%2C+project%2C+provision_rule%2C+role%2C+specification+from+provision+where+%22project%22+%3D+%3Ap0+group+by+dataset&p0=open-digital-planning)

Mandated Datasets – These are datasets that LPAs are legally required to provide, this includes brownfield-land and developer-contributions datasets.

Single Source Datasets – This category includes data obtained from authoritative sources or seeded data received from the Data Design Team.

The recommended steps to resolve this are as follows:

1. **Setup Config Repo**
    Clone the [Config repository](https://github.com/digital-land/config) if it has not already been done, then create and activate a virtual environment.

2. **Run the Script**
    The script can be run using the command `python3 batch_assign_entities.py`

    Upon execution, the script will download the `issue_summary.csv` file to the root directory of the Config folder.

    The downloaded `issue_summary.csv` includes a column called scope, this column indicates the scope for each dataset. This scope includes the categories specified above, such as ODP, Mandated and Single source.

3. **Analyse Unknown Entity issues**
    Open the `issue_summary.csv` file and apply a filter to the "scope" column to display only entries related to ODP. Begin by analysing all unknown entities issues associated with the ODP scope.

    If the `count_issue` for any dataset is unusually high, verify that the entities are valid and new. `count_issue` may also be high if the LPA has recently their references for existing entities.

    The command will prompt the user to confirm. Type "yes" to assign Unknown entities for ODP.

    The command will prompt the user to enter scope (odp/mandated/single-source). Type "odp" to assign entities. 
    
    It will download all the resources for unknown entities into a resources folder, assign entities, and then delete the downloaded resource files. The affected dataset’s lookup.csv should now have new rows with the assigned entities. The amount of entities that needed to be assigned should be the same amount that have been added in the lookup file.

    Unknown entities will be automatically assigned.

4. **Assign entities for Mandated and single-source datasets**
    Repeat Step 3 for assign entities for Mandated and single-source datasets.

    Enter the scope, either mandated or single-source based on requirement.
    
5. **Merge Changes**
    Raise a PR and merge it after it's reviewed.

    Create a new sheet in [this google docs](https://docs.google.com/spreadsheets/d/1gZ_SIx9jdko_aD3QRZUJh39PdNHISS1N/edit?usp=drive_link&ouid=105995804157199974210&rtpof=true&sd=true) and rename the sheet to have the Sprint start date.
    Paste the row of “unknown entity” issues you have resolved in the google sheet, This will help track the datasets you've updated and ensure they are noted for future review.

6. **Review Changes**
    Once merged, use [endpoint_dataset_issue_type_summary table](https://datasette.planning.data.gov.uk/performance/endpoint_dataset_issue_type_summary?_sort=rowid&issue_type__exact=unknown+entity) and check if the previous unknown entity issues are resolved. 
    
    Note in the sheet if you are not able to assign entities for any LPA.

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

## Retire erroring endpoints

One of our quality measures is to reduce the number of endpoints erroring on our platform so we no longer collecting data from those endpoints. We can retire endpoints in a batch by running a script.

The scope of this task can either be for non-ODP datasets or for ODP datasets, so only retire those that are within scope of this.

The recommended steps to resolve this are as follows:

1. Run [this query](https://datasette.planning.data.gov.uk/digital-land?sql=WITH+unique_endpoints+AS+%28%0D%0A++SELECT%0D%0A++++collection%2C%0D%0A++++pipeline+as+dataset%2C%0D%0A++++endpoint%2C%0D%0A++++organisation%2C%0D%0A++++name%2C%0D%0A++++MIN%28endpoint_entry_date%29+AS+endpoint_entry_date%0D%0A++FROM%0D%0A++++reporting_historic_endpoints%0D%0A++WHERE%0D%0A++++%28%0D%0A++++++%22endpoint_end_date%22+is+null%0D%0A++++++OR+%22endpoint_end_date%22+%3D+%22%22%0D%0A++++%29%0D%0A++++AND+%22endpoint_entry_date%22+%3C+DATE%28%27now%27%2C+%27-1+year%27%29%0D%0A++++AND+%22status%22+NOT+LIKE+%222%25%22%0D%0A++GROUP+BY%0D%0A++++collection%2C%0D%0A++++endpoint%2C%0D%0A++++name%0D%0A%29%2C%0D%0Alatest_log_entry+AS+%28%0D%0A++SELECT%0D%0A++++endpoint%2C%0D%0A++++MAX%28latest_log_entry_date%29+AS+latest_200_log_entry_date%0D%0A++FROM%0D%0A++++reporting_historic_endpoints%0D%0A++WHERE%0D%0A++++status+%3D+%27200%27%0D%0A++GROUP+BY%0D%0A++++endpoint%0D%0A%29%0D%0ASELECT%0D%0Aue.collection%2C%0D%0A++ue.dataset%2C%0D%0A++ue.name%2C%0D%0A++p.project%2C%0D%0A++p.provision_reason%2C%0D%0A++ue.endpoint%2C%0D%0A++strftime%28%27%25d-%25m-%25Y%27%2C+ue.endpoint_entry_date%29+as+endpoint_entry_date%2C%0D%0A++strftime%28%27%25d-%25m-%25Y%27%2C+l.latest_200_log_entry_date%29+as+latest_200_log_entry_date%2C%0D%0A++CAST%28%0D%0A++++julianday%28%27now%27%29+-+julianday%28l.latest_200_log_entry_date%29+AS+int64%0D%0A++%29+as+n_days_since_last_200%2C%0D%0A++s.source%0D%0AFROM%0D%0A++unique_endpoints+ue%0D%0A++LEFT+JOIN+source+s+ON+ue.endpoint+%3D+s.endpoint%0D%0A++LEFT+JOIN+latest_log_entry+l+ON+ue.endpoint+%3D+l.endpoint%0D%0A++LEFT+JOIN+provision+p+on+ue.dataset+%3D+p.dataset%0D%0A++and+ue.organisation+%3D+p.organisation%0D%0AWHERE%0D%0A++%28%0D%0A++++l.latest_200_log_entry_date+%3C+DATE%28%27now%27%2C+%27-5+day%27%29%0D%0A++++OR+l.latest_200_log_entry_date+IS+NULL%0D%0A++%29%0D%0A++AND+%22n_days_since_last_200%22+%3E+90%0D%0AORDER+BY%0D%0A++ue.dataset%2C%0D%0A++julianday%28%27now%27%29+-+julianday%28l.latest_200_log_entry_date%29+desc) which will return all endpoints which have been erroring for more than 90 days (e.g where `n_days_since_last_200 > 90`)
2. Select the data as CSV and copy the contents
3. In VSC, create a `retire.csv` file in the root and paste the content in there
4. Run the command:

```
digital-land retire-endpoints-and-sources retire.csv
```

5. Write down the endpoints you have retired (and note any you have been unable to retire) in [the sheet](https://docs.google.com/spreadsheets/d/1M1Zj_iuYFmd5d29TBUFo6lyaQpeylbnI/edit?gid=1103537962#gid=1103537962)

Success criteria:
No erroring endpoints listed in the query for the scope of the ticket.

## Out of range entities

### Trigger
This is a configuration error where the entity numbers that have been used in a dataset are not within the range defined for that dataset. These issues will be raised in the [issue report](https://config-manager-prototype.herokuapp.com/reporting/download?type=odp-issue) where the `issue_type` = "entity number out of range".

### Task
In order to fix, for each dataset with issues you should:

1. Delete the entries in `lookup.csv` which are using an incorrect entity number.
2. Follow the [assign entities](../../How-To-Guides/Maintaining/Assign-entities) process to assign new entity numbers and replace the deleted lookup entries.

### Test
Once fixed, there should no longer be any issues raised in the issue report.


## Invalid Organisations

One of our monitoring tasks is patching any `invalid organisation` issues that arise. This isually happens if the organisation value provided in the endpoint is wrong or missing e.g it could be a blank field or the wrong organisation name / identifier.

A list of invalid organisation issues can be optained by downloading a csv file from either the [issue summary table](https://config-manager-prototype.herokuapp.com/reporting/odp-summary/issue) or the [overview issue table](https://config-manager-prototype.herokuapp.com/reporting/overview) and filtering for `invalid organisations` under `issue-type`.

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