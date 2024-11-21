## Organisation

We maintain a list of organisations that supply data to our platform. These organisations are categorised into various types, such as development corporations, government organisations, local authorities, and more. Each data source added to our platform must be linked to the organisation that provided the data.

The [organisation](https://datasette.planning.data.gov.uk/digital-land/organisation) table includes key details for each organisation, such as the organisation name, website, start date, end date, etc.

## Provision

The [Provision](https://datasette.planning.data.gov.uk/digital-land/provision?_sort=rowid) table is created to identify the organisations from which we expect data for a given dataset. This table helps in identifying the expected publishers for a specific dataset.

It contains key information such as:

* provision_reason: Specifies the reason why an organisation is expected to provide a particular dataset.
* provision_rule: Defines the rules governing the data we expect each organisation to supply. These rules are used to generate the final provision dataset. 

## Provision Rule

The [Provision Rule](https://datasette.planning.data.gov.uk/digital-land/provision_rule) table contains two key fields, **project** and **role**, which are used to identify the organisations expected to provide data.

For example, in the case of the Article 4 Direction dataset:

* The role is set to local-planning-authority. Organisations linked to this role are stored in the [Role Organisation](https://datasette.planning.data.gov.uk/digital-land/role_organisation?role=local-planning-authority) Table, and all organisations associated with this role are added for the dataset.
* Additionally, the dataset is associated with the project Open Digital Planning. Organisations linked to this project, found in the [Project Organisation](https://datasette.planning.data.gov.uk/digital-land/project_organisation?project=open-digital-planning) Table, are also added for this dataset.

To modify the Project Organisation list, navigate to the [project](https://github.com/digital-land/specification/tree/main/content/project) folder within the specification repository and select the file depending on the project you wish to update.

**Note:** Avoid making changes to any files in the [specification](https://github.com/digital-land/specification/tree/main/specification) folder. The specification files are automatically built from the content files after every commit. Any changes made here will be automatically reverted.

This process ensures that all relevant organisations, based on their roles and project affiliations, are accurately associated with each dataset.