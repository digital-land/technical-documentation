
This section covers situations where we are monitoring the quality of data and fix any issues that have arisen.


## Unknown entities
To keep the datasets up-to-date on the platform, we need to check “unknown entity” issues every week and assign entities.
The unknown entities issue usually occurs when an LPA updates their data on the endpoint we are retrieving and adds new records. These records will have reference values we do not have on the platform, hence when the system realises the new data has been added and the references of those new data are not on the platform, it will trigger an unknown entity issue.

The recommended steps to resolve this are as follows:

1. Go to the report found [here](https://config-manager-prototype.herokuapp.com/reporting/odp-summary/issue)
2. Download the CSV file with ‘Download Current Table’ which will download a file called `odp_issues`
3. Analyse the "unknown entity" issues. Look for `issue_type` with `unknown entity`
4. If possible, for each of the issues you have identified, follow the steps in [Assign entities](Assign-entities). Keep track of the row of the issue.
5. Raise a PR and merge it
6. Once merged, run the issue report again and check if the previous unknown entity is resolved.  Paste the row of “unknown entity” issues you have tracked in [this google docs](https://docs.google.com/spreadsheets/d/1gZ_SIx9jdko_aD3QRZUJh39PdNHISS1N/edit?usp=drive_link&ouid=105995804157199974210&rtpof=true&sd=true) after the changes are merged on the platform.
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
4. The LPAs will need to be contacted. Once confirmed that these were deleted, follow the [retire entities process](Retire-entities)
5. Note in the sheet if an entitiy could not be retired

Success criteria: 
The count of entities on the platform and on the latest resource should be the same. Run the report to make sure that the counts are matching.

## Retire erroring endpoints

One of our quality measures is to reduce the number of endpoints erroring on our platform so we no longer collecting data from those endpoints. We can retire endpoints in a batch by running a script. 

The scope of this task can either be for non-ODP datasets or for ODP datasets, so only retire those that are within scope of this.

The recommended steps to resolve this are as follows:

1. Run [this query](https://datasette.planning.data.gov.uk/digital-land?sql=WITH+unique_endpoints+AS+%28%0D%0A++SELECT%0D%0A++++collection%2C%0D%0A++++pipeline+as+dataset%2C%0D%0A++++endpoint%2C%0D%0A++++organisation%2C%0D%0A++++name%2C%0D%0A++++MIN%28endpoint_entry_date%29+AS+endpoint_entry_date%0D%0A++FROM%0D%0A++++reporting_historic_endpoints%0D%0A++WHERE%0D%0A++++%28%0D%0A++++++%22endpoint_end_date%22+is+null%0D%0A++++++OR+%22endpoint_end_date%22+%3D+%22%22%0D%0A++++%29%0D%0A++++AND+%22endpoint_entry_date%22+%3C+DATE%28%27now%27%2C+%27-1+year%27%29%0D%0A++++AND+%22status%22+NOT+LIKE+%222%25%22%0D%0A++GROUP+BY%0D%0A++++collection%2C%0D%0A++++endpoint%2C%0D%0A++++name%0D%0A%29%2C%0D%0Alatest_log_entry+AS+%28%0D%0A++SELECT%0D%0A++++endpoint%2C%0D%0A++++MAX%28latest_log_entry_date%29+AS+latest_200_log_entry_date%0D%0A++FROM%0D%0A++++reporting_historic_endpoints%0D%0A++WHERE%0D%0A++++status+%3D+%27200%27%0D%0A++GROUP+BY%0D%0A++++endpoint%0D%0A%29%0D%0ASELECT%0D%0Aue.collection%2C%0D%0A++ue.dataset%2C%0D%0A++ue.name%2C%0D%0A++p.project%2C%0D%0A++p.provision_reason%2C%0D%0A++ue.endpoint%2C%0D%0A++strftime%28%27%25d-%25m-%25Y%27%2C+ue.endpoint_entry_date%29+as+endpoint_entry_date%2C%0D%0A++strftime%28%27%25d-%25m-%25Y%27%2C+l.latest_200_log_entry_date%29+as+latest_200_log_entry_date%2C%0D%0A++CAST%28%0D%0A++++julianday%28%27now%27%29+-+julianday%28l.latest_200_log_entry_date%29+AS+int64%0D%0A++%29+as+n_days_since_last_200%2C%0D%0A++s.source%0D%0AFROM%0D%0A++unique_endpoints+ue%0D%0A++LEFT+JOIN+source+s+ON+ue.endpoint+%3D+s.endpoint%0D%0A++LEFT+JOIN+latest_log_entry+l+ON+ue.endpoint+%3D+l.endpoint%0D%0A++LEFT+JOIN+provision+p+on+ue.dataset+%3D+p.dataset%0D%0A++and+ue.organisation+%3D+p.organisation%0D%0AWHERE%0D%0A++%28%0D%0A++++l.latest_200_log_entry_date+%3C+DATE%28%27now%27%2C+%27-5+day%27%29%0D%0A++++OR+l.latest_200_log_entry_date+IS+NULL%0D%0A++%29%0D%0A++AND+%22n_days_since_last_200%22+%3E+90%0D%0AORDER+BY%0D%0A++ue.dataset%2C%0D%0A++julianday%28%27now%27%29+-+julianday%28l.latest_200_log_entry_date%29+desc) which will return all endpoints which have been erroring for more than 90 days (e.g where `n_days_since_last_200 > 90`)
2. Select the data as CSV and  copy the contents 
3. In VSC, create a `retire.csv` file in the root and paste the content in there
4. Run the command:

```
digital-land retire-endpoints-and-sources retire.csv
```
5. Write down the endpoints you have retired (and note any you have been unable to retire) in [the sheet](https://docs.google.com/spreadsheets/d/1M1Zj_iuYFmd5d29TBUFo6lyaQpeylbnI/edit?gid=1103537962#gid=1103537962)

Success criteria:
No erroring endpoints listed in the query for the scope of the ticket.