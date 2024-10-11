
The [performance database](https://datasette.planning.data.gov.uk/performance/) on datasette contains a number of useful tables designed for reporting and monitoring purposes. 

## [endpoint_dataset_resource_summary](https://datasette.planning.data.gov.uk/performance/endpoint_dataset_resource_summary)
### Table description

### Table columns
| Column name   | Column type   | Column description   |
| :-------- | :--------- | :---------- |
| organisation | TEXT |    |
| organisation_name | TEXT |    |
| cohort | TEXT |    |
| dataset | TEXT |    |
| collection | TEXT |    |
| pipeline | TEXT |    |
| endpoint | TEXT |    |
| endpoint_url | TEXT |    |
| resource | TEXT |    |
| resource_start_date | TEXT |    |
| resource_end_date | TEXT |    |
| latest_log_entry_date | TEXT |    |
| mapping_field | TEXT |    |
| non_mapping_field | TEXT |    |



## [reporting_historic_endpoints](https://datasette.planning.data.gov.uk/performance/reporting_historic_endpoints)
### Table description

### Table columns
| Column name   | Column type   | Column description   |
| :-------- | :--------- | :---------- |
| organisation | TEXT |    |
| name | TEXT |    |
| collection | TEXT |    |
| pipeline | TEXT |    |
| endpoint | TEXT |    |
| endpoint_url | TEXT |    |
| licence | TEXT |    |
| latest_status | TEXT |    |
| latest_exception | TEXT |    |
| resource | TEXT |    |
| latest_log_entry_date | TEXT |    |
| endpoint_entry_date | TEXT |    |
| endpoint_end_date | TEXT |    |
| resource_start_date | TEXT |    |
| resource_end_date | TEXT |    |



## [endpoint_dataset_summary](https://datasette.planning.data.gov.uk/performance/endpoint_dataset_summary)
### Table description

### Table columns
| Column name   | Column type   | Column description   |
| :-------- | :--------- | :---------- |
| endpoint | TEXT |    |
| endpoint_url | TEXT |    |
| organisation | TEXT |    |
| dataset | TEXT |    |
| latest_status | TEXT |    |
| latest_exception | TEXT |    |
| entry_date | TEXT |    |
| end_date | TEXT |    |
| latest_resource_start_date | TEXT |    |



## [provision_summary](https://datasette.planning.data.gov.uk/performance/provision_summary)
### Table description

### Table columns
| Column name   | Column type   | Column description   |
| :-------- | :--------- | :---------- |
| organisation | TEXT |    |
| organisation_name | TEXT |    |
| dataset | TEXT |    |
| active_endpoint_count | INTEGER |    |
| error_endpoint_count | INTEGER |    |
| count_issue_error_internal | INTEGER |    |
| count_issue_error_external | INTEGER |    |
| count_issue_warning_internal | INTEGER |    |
| count_issue_warning_external | INTEGER |    |
| count_issue_notice_internal | INTEGER |    |
| count_issue_notice_external | INTEGER |    |



## [reporting_latest_endpoints](https://datasette.planning.data.gov.uk/performance/reporting_latest_endpoints)
### Table description

### Table columns
| Column name   | Column type   | Column description   |
| :-------- | :--------- | :---------- |
| organisation | TEXT |    |
| name | TEXT |    |
| collection | TEXT |    |
| pipeline | TEXT |    |
| endpoint | TEXT |    |
| endpoint_url | TEXT |    |
| licence | TEXT |    |
| latest_status | TEXT |    |
| days_since_200 | INTEGER |    |
| latest_exception | TEXT |    |
| resource | TEXT |    |
| latest_log_entry_date | TEXT |    |
| endpoint_entry_date | TEXT |    |
| endpoint_end_date | TEXT |    |
| resource_start_date | TEXT |    |
| resource_end_date | TEXT |    |
| rn | INTEGER |    |



## [endpoint_dataset_issue_type_summary](https://datasette.planning.data.gov.uk/performance/endpoint_dataset_issue_type_summary)
### Table description

### Table columns
| Column name   | Column type   | Column description   |
| :-------- | :--------- | :---------- |
| organisation | TEXT |    |
| organisation_name | TEXT |    |
| cohort | TEXT |    |
| dataset | TEXT |    |
| collection | TEXT |    |
| pipeline | TEXT |    |
| endpoint | TEXT |    |
| endpoint_url | TEXT |    |
| resource | TEXT |    |
| resource_start_date | TEXT |    |
| resource_end_date | TEXT |    |
| latest_log_entry_date | TEXT |    |
| count_issues | INTEGER |    |
| date | TEXT |    |
| issue_type | TEXT |    |
| severity | TEXT |    |
| responsibility | TEXT |    |
| fields | TEXT |    |



