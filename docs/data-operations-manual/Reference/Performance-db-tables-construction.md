## Performance Database Table Construction Documentation

This is documentation that explains the construction of the tables in the [performance database](https://datasette.planning.data.gov.uk/performance/), including details on base tables, sources of columns.

The Performance Database is designed to store and analyze performance-related metrics extracted from the source database [digital_land](https://datasette.planning.data.gov.uk/digital-land). The tables of this DB are:

>1. `endpoint_dataset_issue_type_summary`
>2. `endpoint_dataset_resource_summary`
>3. `endpoint_dataset_summary`
>4. `provision_summary`
>5. `reporting_historic_endpoints`
>6. `reporting_latest_endpoints`

### 1. Table: [endpoint_dataset_issue_type_summary](https://datasette.planning.data.gov.uk/performance/endpoint_dataset_issue_type_summary)

**Purpose**: To summarize issues associated with each dataset and endpoint.

**Base Tables**:
    - `issue`: Contains records of issues related to resources sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `resource`: Holds information about the resources linked to the endpoints sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `issue_type`: Defines types of issues sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).

**Columns**:
- `organisation`: Extracted from the `provision` table.
- `organisation_name`: Extracted from the `provision` table.
- `cohort`: Extracted from the `provision` table.
- `dataset`: Extracted from the `provision` table.
- `collection`: Extracted from the `reporting_historic_endpoints` table.
- `pipeline`: Extracted from the `reporting_historic_endpoints` table.
- `endpoint`: Extracted from the `reporting_historic_endpoints` table.
- `endpoint_url`: Extracted from the `reporting_historic_endpoints` table.
- `resource`: Extracted from the `reporting_historic_endpoints` table.
- `resource_start_date`: Extracted from the `reporting_historic_endpoints` table.
- `resource_end_date`: Extracted from the `reporting_historic_endpoints` table.
- `latest_log_entry_date`: Extracted from the `reporting_historic_endpoints` table.
- `count_issues`: Count of issues from the `issue` table.
- `date`: Current date when the query is executed.
- `issue_type`: Type of issues from the `issue_type` table.
- `severity`: Severity of issues from the `issue_type` table.
- `responsibility`: Responsibility assigned to the issues from the `issue_type` table.
- `fields`: Concatenated fields from `issue` table.


### 2. Table: [endpoint_dataset_resource_summary](https://datasette.planning.data.gov.uk/performance/endpoint_dataset_resource_summary)

**Purpose**: To summarize resources associated with endpoints, including mapping and non-mapping fields.

**Base Tables**:
    - `provision`: Contains information about organizations, cohorts, and datasets sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `reporting_historic_endpoints`: To store historical data on endpoints sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `column_field`: This is a mapping table that connects specific columns from an endpoint to their corresponding fields sourced according to the dataset's specification e.g UID -> reference,  sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).

**Columns**:
- `organisation`: Extracted from the `provision` table.
- `organisation_name`: Extracted from the `provision` table.
- `cohort`: Extracted from the `provision` table.
- `dataset`: Extracted from the `provision` table.
- `collection`: Extracted from the `reporting_historic_endpoints` table.
- `pipeline`: Extracted from the `reporting_historic_endpoints` table.
- `endpoint`: Extracted from the `reporting_historic_endpoints` table.
- `endpoint_url`: Extracted from the `reporting_historic_endpoints` table.
- `resource`: Extracted from the `reporting_historic_endpoints` table.
- `resource_start_date`: Extracted from the `reporting_historic_endpoints` table.
- `resource_end_date`: Extracted from the `reporting_historic_endpoints` table.
- `latest_log_entry_date`: Extracted from the `reporting_historic_endpoints` table.
- `mapping_field`: Generated using conditional aggregation from `column_field` to identify fields that map correctly to columns.
- `non_mapping_field`: Generated using conditional aggregation from `column_field` for fields that do not map correctly.



### 3. Table: [endpoint_dataset_summary](https://datasette.planning.data.gov.uk/performance/endpoint_dataset_summary)

**Purpose**: To summarize endpoint information, including the latest statuses and exceptions.

**Base Tables**:
    - `endpoint`: Contains information about endpoints sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `source`: Provides a link between endpoints and organizations sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `log`: Contains logs related to endpoint performance sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).

**Columns**:
- `endpoint`: Extracted from the `endpoint` table.
- `endpoint_url`: Extracted from the `endpoint` table.
- `organisation`: Extracted from the `source` table.
- `dataset`: Extracted from the resource-dataset mapping.
- `latest_status`: Extracted from the `log` table.
- `latest_exception`: Extracted from the `log` table.
- `entry_date`: Entry date of the endpoint.
- `end_date`: End date of the endpoint.
- `latest_resource_start_date`: Start date of the most recent resource.


### 4. Table: [provision_summary](https://datasette.planning.data.gov.uk/performance/provision_summary)

**Purpose**: To summarize provision metrics across organizations and datasets, counting various types of issues and endpoints.

**Base Tables**:
    - `provision`: Contains information about datasets sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `organisation`: Contains the names and details of organizations sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `issue`: Contains records of issues related to resources sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `resource`: Holds information about the resources linked to the endpoints sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `issue_type`: Defines types of issues sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `column_field`:  This is a mapping table that connects specific columns from an endpoint to their corresponding fields sourced according to the dataset's specification e.g UID -> reference, sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `endpoint`: Contains information about endpoints sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `source`: Provides a link between endpoints and organizations sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `log`: Contains logs related to endpoint performance sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `reporting_historic_endpoints`: To store historical data on endpoints sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).

**Columns**:
- `organisation`: Extracted from the `provision` table.
- `organisation_name`: Extracted from the `organisation` table.
- `dataset`: Extracted from the `provision` table.
- `active_endpoint_count`: Calculated from `endpoint` table.
- `error_endpoint_count`: Calculated from `endpoint` table.
- `count_issue_error_internal`: Count of internal error issues calculated from `issue` and `issue_type`.
- `count_issue_error_external`: Count of external error issues calculated from `issue` and `issue_type`.
- `count_issue_warning_internal`: Count of internal warning issues calculated from `issue` and `issue_type`.
- `count_issue_warning_external`: Count of external warning issues calculated from `issue` and `issue_type`.
- `count_issue_notice_internal`: Count of internal notice issues calculated from `issue` and `issue_type`.
- `count_issue_notice_external`: Count of external notice issues calculated from `issue` and `issue_type`.


### 5. Table: [reporting_historic_endpoints](https://datasette.planning.data.gov.uk/performance/reporting_historic_endpoints)

**Purpose**: To store historical data on endpoints, including their organization, dataset, and status.

**Base Tables**:
    - `endpoint`: Contains information about endpoints sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `source`: Provides a link between endpoints and organizations sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `log`: Contains logs related to endpoint performance sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `organisation`: Contains the names and details of organizations sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `source_pipeline`: Contains information on the pipeline associated with each source sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `resource`: Holds information about the resources linked to the endpoints sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).

**Columns**:
- `organisation`: Extracted from `source` table.
- `name`: Extracted from the `organisation` table.
- `organisation_name`: Extracted from the `organisation` table.
- `dataset`: Extracted from the `source_pipeline` table.
- `collection`: Extracted from the `source` table.
- `pipeline`: Extracted from the `source_pipeline` table.
- `endpoint`: Extracted from the `log` table.
- `endpoint_url`: Extracted from the `endpoint` table.
- `licence`: Extracted from the `source` data.
- `latest_status`: Extracted from the `log` table.
- `latest_exception`: Extracted from the `log` table.
- `resource`: Extracted from the `log` table.
- `latest_log_entry_date`: Extracted using the **max** function on the entry_date from the `log` table.
- `endpoint_entry_date`: Extracted from the `endpoint` table.
- `endpoint_end_date`: Extracted from the `endpoint` table.
- `resource_start_date`: Extracted from the `resource` table.
- `resource_end_date`: Extracted from the `resource` table.


### 6. Table: [reporting_latest_endpoints](https://datasette.planning.data.gov.uk/performance/reporting_latest_endpoints)

**Purpose**: To store the most recent data on endpoints and provides the latest active endpoint data per organization and pipeline.

**Base Tables**:
    - `endpoint`: Contains information about endpoints sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `source`: Provides a link between endpoints and organizations sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `log`: Contains logs related to endpoint performance sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `organisation`: Contains the names and details of organizations sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `source_pipeline`: Contains information on the pipeline associated with each source sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).
    - `resource`: Holds information about the resources linked to the endpoints sourced from the [digital_land](https://datasette.planning.data.gov.uk/digital-land).

**Columns**:
- `organisation`: Extracted from source table.
- `name`: Extracted from the organization table.
- `organisation_name`: Extracted from the organization table.
- `dataset`: Extracted from the dataset table.
- `collection`: Extracted from the source table.
- `pipeline`: Extracted from the source_pipeline table.
- `endpoint`: Extracted from the log table.
- `endpoint_url`: Extracted from the endpoint table.
- `licence`: Extracted from the source data.
- `latest_status`: Extracted from the log table.
- `days_since_200`: Calculated from log as days since last "200 OK" status, from subquery t2.
- `latest_exception`: Extracted from the log table.
- `resource`: Extracted from the log table.
- `latest_log_entry_date`: Extracted using the **max** function on the entry_date from the log table.
- `endpoint_entry_date`: Extracted from the endpoint table.
- `endpoint_end_date`: Extracted from the endpoint table.
- `resource_start_date`: Extracted from the resource table.
- `resource_end_date`: Extracted from the resource table.
- `rn`: Row number for identifying unique records.

