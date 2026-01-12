---
title: Data quality framework
---

## Quality requirements

We have a structured approach to how we identify and fix issues with data quality, which we refer to as our *data quality framework*. The core of this framework is a [list of data quality requirements](https://docs.google.com/spreadsheets/d/1kMAKOAm6Wam-AJb6R0KU-vzdvRCmLVN7PbbTAUh9Sa0/edit#gid=2142834080) built and maintained by the data management team. 

These documented data quality requirements help the team plan and document the tests used to identify whether or not quality requirements are being met, as well as the methods for running the tests. We use the process below to go from identifying a data quality need through to actively monitoring whether or not it is being met, and then raising identified quality issues to the party responsible for fixing them.

The list also acts as a backlog of known data quality requirements. By working through this backlog to build more tests we can expand the coverage of our data quality monitoring and measurement. 

![defining-data-quality-process](/images/data-operations-manual/defining-data-quality-process.png)

1. **Quality requirement**: documenting a need we have of planning data based on its intended uses.

1. **Test definition**: agreeing the methods for systematically identify data which is not meeting a quality requirement.

1. **Test implementation**: productionising the identification of issues in the pipeline, primarily using the issues or expectations testing frameworks, or possibly other pipeline processing artefacts.

1. **Quality monitoring**: surfacing information about data quality issues in a structured way so that action can be taken.

**Example**

Here's an example using a requirement we have based on the expectation that providers of our ODP datasets should only be providing data within their local planning authority boundary. This helps us identify a quality issue like if Bristol City Council were to supply conservation-area data where a polygon was in Newcastle.


> 1. Quality requirement: geometry data should be within the expected boundary of the provider’s administrative area.
> 
> 1. Test definition: An ‘out of expected LPA bounds’ issue for ODP datasets is when the supplied geometry does not intersect at all with the provider’s Local Planning Authority boundary.
> 
> 1. Test implementation: [expectation rules](https://datasette.planning.data.gov.uk/digital-land/expectation?_facet=name&name=Check+no+entities+are+outside+of+the+local+planning+authority+boundary) which test for any of these issues on all ODP datasets.
> 
> 1. Quality monitoring: surfacing information about out of bounds issues in the Submit service so that LPAs can act on this and fix the issues.

## Quality tests

During the development phase, the data management team might use datasette queries or python code in jupyter notebooks to design the methods for a quality test. Once the method has been proven, it is usually more formally implemented in one of two ways:

* **Issues** - issue logs are raised when quality tests fail as the pipeline is processing individual values from a resource.
* **Expectations** - expectations logs are raised when expectation rules fail, these are run after the entire dataset is built into a sqlite database file.

Issue and expectations logs are re-produced each night and provide a detailed record of the results of different data quality tests. For more detail on how they work and where they sit in the pipeline process, see the [data quality needs explainer](../Data-quality-1-needs).

## Quality monitoring

Once data quality requirements are defined, and tests to identify where they're not being met are implemented, we're able to systematically monitor for any occurances of data quality issues. 

Monitoring is carried out in one of two ways, depending on whether the responsibility for fixing the issue is external (i.e. with the data provider) or internal (i.e. with the data management team):

* By the **[Submit service](https://submit.planning.data.gov.uk/)**, to allow LPAs to self-monitor and fix issues at source

* By the **Data Management team**, to resolve data quality issues that can be fixed by a change in configuration

See our [monitoring data quality](../../../Tutorials/Monitoring-Data-Quality) page which gives guidance on the processes we follow to fix quality issues raised by our operational monitoring. These processes go hand-in-hand with our [data quality requirements](https://docs.google.com/spreadsheets/d/1kMAKOAm6Wam-AJb6R0KU-vzdvRCmLVN7PbbTAUh9Sa0/edit#gid=2142834080), which defines our full backlog of requirements, test definitions and monitoring approach.

Note: The Data Management team also has a [defined process](https://docs.google.com/document/d/1YGM8W0E2_qW60k8hlancVWBe0aYPNIfefpctNwQ3MSs/edit) for tackling ad-hoc data quality issues which are raised for data on the platform. This begins with an investigation, followed by one or both of a data fix and root cause resolution. This process may also result in the formal definition of a data quality requirement and test so that it can be handled in future through the data quality management framework.


# Quality measurement

With well defined data quality requirements and tests, it's possible to use them to make useful summaries of data quality at different scales, for example assessing whether the data on an endpoint meets all of the requirements for a particular purpose.

We've created a *data quality measurement framework* to define different data quality levels based on the requirements of ODP software. This measurement framework is used to score data provisions (a dataset from a provider) and create summaries of the number of provisions at each quality level.

The table below visualises the framework:

![quality framework table](/images/data-operations-manual/quality-framework-table.png)

The criteria marked as "true" at each level must be met by a data provision in order for it to be scored at that level. Therefore the framework defines 5 criteria that must be met in order for a data provision to be *good for ODP*. The levels are cumulative, so those same 5 criteria plus 3 more must be met in order for a provision to be scored as *data that is trustworthy*. Where we have data from alternative providers (e.g. Historic England conservation-area data) the first criteria cannot be met so it is scored as the first quality level, *some data*.

Each of the criteria are based around one or more data quality requirements and their respective tests. 

> **Example**   
>
> The "No other types of validity errors" criteria is based on meeting 6 different data quality requirements related to expected data formats. If a provision has failed any of the separate tests for these requirements the criteria is not met.
>
> These requirements and their tests are documented in our [data quality needs tracker](https://docs.google.com/spreadsheets/d/1kMAKOAm6Wam-AJb6R0KU-vzdvRCmLVN7PbbTAUh9Sa0/edit?gid=2142834080#gid=2142834080), and the mapping of requirements to criteria is captured in the  [measurement tab](https://docs.google.com/spreadsheets/d/1kMAKOAm6Wam-AJb6R0KU-vzdvRCmLVN7PbbTAUh9Sa0/edit?gid=1268095085#gid=1268095085).

<br>

The framework is flexible as each data quality test is independent and is carried out by the pipeline automatically each night. To make any changes to the measurement framework we can simply edit the mapping from test results to quality criteria, and quality criteria to quality levels. And to extend the framework we can build new tests and add them into the mapping.

<br>

> **Note**:   
> 
> The scoring process currently a proof of concept which is run in a jupyter-notebook, but we're working on productionising it so scores are output to a `provision-quality` table by the pipeline.

<br>


The chart below is an example of using the framework to measure the quality levels across all ODP dataset provisions (on 2024-11-20):

![quality framework table](/images/data-operations-manual/ODP-data-quality-levels.png)
(see quality reporting in the [jupyter-analysis](https://github.com/digital-land/jupyter-analysis) repo for up to date versions)


[^1]:  The Government Data Quality Framework: https://www.gov.uk/government/publications/the-government-data-quality-framework/the-government-data-quality-framework\#why-do-we-need-a-data-quality-framework
