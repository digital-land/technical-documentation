
The [performance database](https://datasette.planning.data.gov.uk/performance/) on datasette contains a number of useful tables designed for reporting and monitoring purposes. 

## [endpoint_dataset_resource_summary](https://datasette.planning.data.gov.uk/performance/endpoint_dataset_resource_summary)
### Table description

### Table columns
| Column name   | Column type   | Column description   |
| :-------- | :--------- | :---------- |
| organisation | TEXT |  Unique code that identifies organization  |
| organisation_name | TEXT |  Name of the Organisation  |
| cohort | TEXT |    |
| dataset | TEXT |  Name of Dataset, representing the type of data collected  |
| collection | TEXT | Name of Collection, within which the dataset belongs  |
| pipeline | TEXT | Name of Pipeline, process the dataset   |
| endpoint | TEXT | Unique hash for accessing the data   |
| endpoint_url | TEXT | URL linking to the dataset’s csv file or API endpoint   |
| resource | TEXT |  Unique hash for the resource  |
| resource_start_date | TEXT |  Start date of the resource  |
| resource_end_date | TEXT |  End date of the resource  |
| latest_log_entry_date | TEXT |    |
| mapping_field | TEXT |    |
| non_mapping_field | TEXT |    |



## [reporting_historic_endpoints](https://datasette.planning.data.gov.uk/performance/reporting_historic_endpoints)
### Table description

### Table columns
| Column name   | Column type   | Column description   |
| :-------- | :--------- | :---------- |
| organisation | TEXT |  Unique code that identifies organization  |
| name | TEXT |    |
| organisation_name  | TEXT | Name of the Organisation |
| dataset  |  TEXT | Name of Dataset, representing the type of data collected |
| collection | TEXT | Name of Collection, within which the dataset belongs  |
| pipeline | TEXT | Name of Pipeline, process the dataset   |
| endpoint | TEXT |  Unique hash for accessing the data  |
| endpoint_url | TEXT |  URL linking to the dataset’s csv file or API endpoint   |
| licence | TEXT |    |
| latest_status | TEXT |    |
| latest_exception | TEXT |    |
| resource | TEXT |  Unique hash for the resource  |
| latest_log_entry_date | TEXT |    |
| endpoint_entry_date | TEXT |  Entry date of the endpoint  |
| endpoint_end_date | TEXT |  End date of the endpoint  |
| resource_start_date | TEXT | Start date of the resource   |
| resource_end_date | TEXT |  End date of the resource  |



## [endpoint_dataset_summary](https://datasette.planning.data.gov.uk/performance/endpoint_dataset_summary)
### Table description

### Table columns
| Column name   | Column type   | Column description   |
| :-------- | :--------- | :---------- |
| endpoint | TEXT |  Unique hash for accessing the data  |
| endpoint_url | TEXT |  URL linking to the dataset’s csv file or API endpoint  |
| organisation | TEXT |  Unique code that identifies organization  |
| dataset | TEXT |  Name of Dataset, representing the type of data collected  |
| latest_status | TEXT |    |
| latest_exception | TEXT |    |
| entry_date | TEXT | Entry date of endpoint  |
| end_date | TEXT |  End date of endpoint  |
| latest_resource_start_date | TEXT |    |



## [provision_summary](https://datasette.planning.data.gov.uk/performance/provision_summary)
### Table description

### Table columns
| Column name   | Column type   | Column description   |
| :-------- | :--------- | :---------- |
| organisation | TEXT | Unique code that identifies organization   |
| organisation_name | TEXT | Name of Organisation   |
| dataset | TEXT |  Name of Dataset, representing the type of data collected  |
| active_endpoint_count | INTEGER | Count for the active endpoint   |
| error_endpoint_count | INTEGER |  Count of endpoints with errors  |
| count_issue_error_internal | INTEGER |  Count of internal issues  |
| count_issue_error_external | INTEGER |  Count of external issues  |
| count_issue_warning_internal | INTEGER |  Count of internal warnings  |
| count_issue_warning_external | INTEGER | Count of external warnings   |
| count_issue_notice_internal | INTEGER | Count of internal notice   |
| count_issue_notice_external | INTEGER |  Count of external notice  |



## [reporting_latest_endpoints](https://datasette.planning.data.gov.uk/performance/reporting_latest_endpoints)
### Table description

### Table columns
| Column name   | Column type   | Column description   |
| :-------- | :--------- | :---------- |
| organisation | TEXT |  Unique code that identifies organization  |
| name | TEXT |    |
| organisation_name  |  TEXT | Name of Organisation |
| dataset | TEXT | Name of Dataset, representing the type of data collected  |
| collection | TEXT |  Name of Collection, within which the dataset belongs  |
| pipeline | TEXT | Name of Pipeline, process the dataset   |
| endpoint | TEXT |  Unique hash for accessing the data  |
| endpoint_url | TEXT |  URL linking to the dataset’s csv file or API endpoint  |
| licence | TEXT |    |
| latest_status | TEXT |    |
| days_since_200 | INTEGER |    |
| latest_exception | TEXT |    |
| resource | TEXT |  Unique hash for the resource  |
| latest_log_entry_date | TEXT |    |
| endpoint_entry_date | TEXT |  Entry date of endpoint  |
| endpoint_end_date | TEXT |  End date of endpoint  |
| resource_start_date | TEXT |  Start date of the resource   |
| resource_end_date | TEXT | End date of the resource    |
| rn | INTEGER |    |



## [endpoint_dataset_issue_type_summary](https://datasette.planning.data.gov.uk/performance/endpoint_dataset_issue_type_summary)
### Table description

### Table columns
| Column name   | Column type   | Column description   |
| :-------- | :--------- | :---------- |
| organisation | TEXT |  Unique code that identifies organization  |
| organisation_name | TEXT | Name of Organisation   |
| cohort | TEXT |    |
| dataset | TEXT | Name of Dataset, representing the type of data collected   |
| collection | TEXT |  Name of Collection, within which the dataset belongs  |
| pipeline | TEXT |  Name of Pipeline, process the dataset  |
| endpoint | TEXT | Unique hash for accessing the data   |
| endpoint_url | TEXT |  URL linking to the dataset’s csv file or API endpoint   |
| resource | TEXT | Unique hash for the resource    |
| resource_start_date | TEXT | Start date of the resource   |
| resource_end_date | TEXT |  End date of the resource  |
| latest_log_entry_date | TEXT |    |
| count_issues | INTEGER |  The total number of issues recorded  |
| date | TEXT |    |
| issue_type | TEXT | The type of issue noted   |
| severity | TEXT |  The level of importance of the issue  |
| responsibility | TEXT |  Who is accountable for addressing or resolving the issue   |
| fields | TEXT |    |



