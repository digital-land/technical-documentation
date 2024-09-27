Author(s) - Owen Eveleigh
## Introduction

![images showing a high level version of our data workflow with two areas highlighted where checkpoints could go](https://github.com/digital-land/digital-land/blob/main/images/high_level_architecture_v2_with_checkpoints.drawio.png)

We currently only record data quality issues during the pipeline section of our data workflow. this is present in the above diagram in the issue log box. While this is powerful as it can fully explain the transformations being applied to a data point it doesn't provide any framework for more checkpoint style validations. I have highlighted two key area above where additional validations have been requested:
- On incoming resources from provider systems further left in the data workflow
- On the dataset sqlite files before it's made available to the public/platform

This ODP outlines how a new python module focussed on data validations called expectations can apply expectations on two specific checkpoints:

- converted resource - to enable us to run expectations on an individual resource to communicate possible errors/warnings back to providers. (we do minimal processing first to establish a common tabular representation)
- Dataset - enables use to run internal expectations to see if anything is wrong at the end of dataset creation and add a layer of protection against adding incorrect data into the public domain.

## Status

 Open 

 * Draft: proposal is still being authored and is not officially open for comment yet
 * Open: proposal is open for comment
 * Closed: proposal is closed for comment with implementation expected
 * On Hold: proposal is on hold due to concerns raised/project changes with implementation not expected

## Detail

### Section 1: Current Data Quality Issues Raised
![our current pipeline setup showing that multiple phases have access to the issue log but not all of them and most of them are row based access to the data](https://github.com/digital-land/digital-land/blob/main/images/current-pipeline.drawio.png)

The above [picture](https://github.com/digital-land/digital-land/blob/main/images/current-pipeline.drawio.png) shows how throughout the current pipeline step of our data workflow we regularly record issues to an issues log. At the time of writing this is primarily focussed on only recording issues when either:

- a value is transformed/changed when we beleive we can fix/improve the quality of the data. E.g. We convert the CRS
- a data point/value is removed because we beleive the data is incorrect e.g. a geometry is outside of an appropriate bounding box

There are a few limitations associated with this and it may not be capable of handling the requirements of the providers and management teams. For example:
- It probably isn't an appropriate place to record problems in the data that aren't fixed or removed. For example missing fields. It could raise this as a warning but it would imply that it is making a transformation.
- If a validation/check needs access to multiple rows (like duplication checks) then right now the pipeline only accesses data row by. row
- what if there is a critical error with the data and no further processing should be done.
- what if you wanted to raise more speculative problems rather than taking an action?

I believe that certain types of validations should have a more formal framework to register what checks should be completed against which data at what stage. For example there should be a checkpoint in the above diagram at the converted resource stage (see the above diagram). this would allow us to communicate problems with a resource back to providers if there are elements missing from their data.

Processing issues should still be recorded but only when changes are being made. Together with both processing issues and these new validation issues we can easily communicate problems back to publishers. 

We have decided to name these new validations expectations. This new framework should be expandable to not just the example in the pipeline stage above but also to the sqlite dataset files we create in the dataset phase

### Section 2: Expectations Module

This is where we need to identify or produce a framework for these additional data validation tests. The word framework here is used as where ever these checks/tests are applied it would be good to have similar meaningful outputs along with commands to make them runnable in multiple environments.

After looking around we need something very specific. The great expectations python package seemed like if would be useful but after looking at the required set-up and how difficult it is to make custom tests it seemed impractical. Hence work has been done to create our own version with similar ideals but much more customisable. We should regularly review this though as it may reduce the maintenance burden to change in the future.

The main aim of the module is that we create checkpoints which take in a set of expected inputs (including data probably through a file path) and run. a set of expectations against that data. The responses to these will be record as expectation responses and if problems are found then they. will be raised as expectation issues. 

We will need to add support for outputting expectation issues and reformat the current expectations responses.


### Section 3: Changes to be made and order

The above is difficult to apply at once and will be of different levels of interest to different parties. I suggest the below:

1. Code up and test expectations work and apply dataset checkpoint
3. Apply converted resource checkpoint

#### 1: Code up and test expectations work

![diagram showing hwo the classes connect to data models](https://github.com/digital-land/digital-land/blob/main/images/Data_Issues.drawio.png)

The changes required of the expectations module:
- implement issue data classes as in the above diagram for each issue scope (It's more of s sketch than every field).
- update response model to link to issues.
- remove suite and just build checkpoints. they could in theory load from yamls but isn't needed at the minute so just use python lists
- update so that dataset checkpoint works and is ran overnight
- Incorporate the dataset data into digital-land-builder so that it's on datasette

Use the dataset checkpoint as a starting point. build a base checkpoint with core functionality then delegate loading of expectations to the checkpoint class.

#### 2: Apply converted resource checkpoint

![diagram with altered flow for additional checkpoint](https://github.com/digital-land/digital-land/blob/main/images/add-converted-resource-check-point.drawio.png)

we will need to run expectations on the csv that is a converted version of the providers data. This will allow us to run checks and raise problems that can be directly connected to the data provided by them. These checks would be ran in both the pipeline and the check tool.

As you can see from the above I think it will be worth altering the pipeline for this checkpoint. Right now the mapping phase takes place after the file is converted and read in row-by-row. First of all this checkpoint needs to take place before the streaming begins so that if checks fail with an error than the pipeline is stopped also so that the checkpoint has access to the entire file. To write consistent checks that take into account the changed column names from the mapping phase it would be best to be able to do it before the checks are ran.

Also the mapping phase it repeated for every row right now, given that it will be the same for every row it makes sense to do it in one step. We can then use the column_field mapping to translate between columns and fields whenever we need to refer to their original data.

## Design Comments
