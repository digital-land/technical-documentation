Author(s) -  [Chris Johns](mailto:cjohns@scottlogic.com)

## Introduction

The platform currently removes empty fields from the data during processing. This is usually, but not always, the required behavior. 

A scenario where this isn't the the required behavior is when a later resource has a blank end-date. See [This Ticket](https://trello.com/c/xtDuvX0z/1347-bug-nullable-fields-cannot-be-updated-to-blank)

## Status

Open

 * Draft: proposal is still being authored and is not officially open for comment yet
 * Open: proposal is open for comment
 * Closed: proposal is closed for comment with implementation expected
 * On Hold: proposal is on hold due to concerns raised/project changes with implementation not expected

## Detail

### The difference between blank and missing data

One of the distinctions that needs to be made is between data that is not provided, and data that is provided as blank. An example for a CSV source is not having a column, vs having a column with an empty field.

In addition, we have some fields which can be expected to be empty - such as the end-date in the above example.

### Nullable fields

In order to accommodate fields that must be present, but may be blank the specification needs to extended to reflect this. This can be done by adding an additional 'nullable" attribute to the field. If this is set to true then the field can contain blank values. If set to false (or not present) the field cannot contain blank values.

Blank values in a non-nullable field should be considered an issue.

### Processing empty fields in the pipeline

Currently, the pipeline will remove any empty fields from the facts (done in the `FactPrunePhase`). This phase needs to be keep these fields in. In addition, the dataset builder package excludes empty 'facts' when building the entities.

### Nullable fields in the pipeline

Currently the `HarmonisePhase` will check for mandatory fields in hard-coded list, and generate an issue if they are missing or blank. This would make it a good candidate to also check for nullability. Longer term, the check for mandatory fields should move to be data-driven (and most likely have a better name). The mandatory fields do (currently) vary between collection, which may impact this (or result in a standard set). This aspect is outside the scope of this proposal.

### Updating to blank

The root cause of the above bug would appear to be a later resource is not correctly updating the end-date to be blank. Not stripping the blank facts is a pre-requisite of this, but the dataset generation code will also require updating. This behavior needs to be updated - even in the case where the field is not nullable. If the data we are given is blank, this is what we should reflect. If it SHOULDN'T be blank then an issue should be raised.

## Scenario List

![image](https://github.com/digital-land/digital-land/assets/95475146/abb9b8fa-c714-4bd4-b405-67f76a05c520)