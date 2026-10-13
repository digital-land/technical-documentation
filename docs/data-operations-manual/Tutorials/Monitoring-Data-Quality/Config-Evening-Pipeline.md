---
title: Config Evening Pipeline and GitHub Actions
---

The [Config Evening Pipeline](https://github.com/digital-land/config/blob/main/.github/workflows/config-evening-pipeline.yml) is a GitHub Actions workflow in the [Config repository](https://github.com/digital-land/config) that consolidates several nightly data maintenance tasks into a single automated run. It replaces a previous set of separate workflows that were chained together by scheduled times, making the overall process more reliable and easier to reason about.

## Config Evening Pipeline

### Schedule

The pipeline runs automatically at **19:00 UTC, Monday to Friday**. It can also be triggered manually from the [Actions tab](https://github.com/digital-land/config/actions/workflows/config-evening-pipeline.yml) in the Config repository.

Due to delays with GitHub actions, the pipeline will typically run at 19:45 UTC (20:45 BST).

Only one run is active at a time — if the pipeline is triggered manually while a run is already in progress (for example, the scheduled evening run), the new trigger queues and starts once the current run finishes, rather than cancelling it or running alongside it.

### Tasks

The pipeline runs the following jobs in order. Each job waits for the previous one to complete before starting.

1. **Merge** — Checks for an open pull request from the `config-manager-update` branch into `main`. If one exists, it is automatically approved and squash-merged. This ensures `main` is up to date before the remaining steps run. If no PR exists, this step completes without making any changes.

2. **Batch assign** — Runs the [batch entity assignment script](../../How-To-Guides/Maintaining/Assign-entities/) against the platform's live issue data to assign entities for resources with unknown entity issues. Every weeknight run processes **both ODP and mandated datasets** (as two parallel jobs in the same run) — there's no day-of-week rotation between them.

   Single-source datasets are handled separately, by their own weekly pipeline that runs **Sundays only**, processing resources in batches of 10 so a failed run can resume from where it left off rather than restarting from scratch.

   This job commits its changes directly to `main` as soon as it finishes, rather than waiting until the end of the pipeline.

3. **Deduplicate** — Runs four scripts in sequence to deduplicate and retire MHCLG placeholder data:
   - Deduplicates conservation area geographies (`deduplicate-ca-geogs.py`)
   - Retires MHCLG conservation area data (`retire-mhclg-ca-data.py`)
   - Retires MHCLG local plan and plan timetable data (`retire-mhclg-plan-data.py`)
   - Redirects MHCLG plan duplicates (`redirect-mhclg-plan-duplicates.py`)

   If one script fails, the remaining scripts still run. All changes from this step are committed to `main` together in a single commit at the end of the job.

4. **Standardise** — Reorders rows and standardises line endings across all `collection/` and `pipeline/` CSV files. This ensures consistent formatting across the repository regardless of how changes were introduced in earlier steps. Changes are committed to `main` if any are detected.

5. **Upload to S3** — Syncs the `collection/` and `pipeline/` directories to S3 for each deployment environment (development, staging, production). This step runs in parallel across environments and picks up all changes committed in the earlier steps.

### Commits

Each stage that modifies data commits its changes to `main` independently rather than in one combined commit at the end. This approach avoids memory issues that can occur when staging a large number of file changes at once, particularly during batch entity assignment.

### Failure behaviour

If a job fails, the subsequent jobs in the pipeline **still run**. For example, if the deduplicate job fails, the standardise and upload-to-S3 jobs will still execute. This means a failure in one area does not prevent the rest of the pipeline from completing.

At the end of the run, if any job has failed, a single alert is posted to the `#planning-data-alerts` Slack channel. The alert names each stage and its result (batch assign's result covers both `odp` and `mandated` in one line, since they run as parallel jobs within it), so it is immediately clear which part of the pipeline failed without needing to open GitHub.

### Manual trigger

The pipeline can be triggered manually from the [Actions tab](https://github.com/digital-land/config/actions/workflows/config-evening-pipeline.yml), which is useful for testing, diagnosing an issue, or resuming a failed run.

**A manual run writes to `main` and S3 by default**, exactly like the scheduled run — triggering it manually does not make it safe on its own. To run every job against live data without committing or syncing anything, you must explicitly set `dry_run` to `true`.

As well as `dry_run`, the manual trigger accepts these inputs:

- `scope` — runs only `odp` or only `mandated`, instead of both (the scheduled run's default). `single-source` is not a valid choice here - it's handled entirely by its own separate, Sunday-only pipeline; see [Assign Entities](../../How-To-Guides/Maintaining/Assign-entities/#scope-differences) for the scope differences.
- `resources` — a comma-separated list of specific resources to target in batch assign, instead of processing everything in scope.
- `skip_checks` — bypasses every validation check (duplicates, retention, missing fields, `current_resource_empty`, `invalid_uri_issue`) and promotes whatever is assigned unconditionally. Use with caution.
- `commit` — whether batch assign commits its results to `main` (default `true`; set to `false` for a batch-assign-only dry run without using the top-level `dry_run` input).

### Verify

To verify the pipeline has run correctly:

- Check the [Actions tab](https://github.com/digital-land/config/actions/workflows/config-evening-pipeline.yml) to confirm all jobs completed successfully.
- Review the commits made to `main` that evening — there should be up to four commits (batch assign odp, batch assign mandated, deduplicate, standardise) if each stage had changes to make.
- Confirm any unknown entity issues resolved by batch assign are no longer present in the [endpoint dataset issue summary](https://datasette.planning.data.gov.uk/performance/endpoint_dataset_issue_type_summary?_sort=rowid&issue_type__exact=unknown+entity).
- If the deduplicate step ran, verify retired entities appear in `pipeline/local-plan/old-entity.csv` and `pipeline/conservation-area/old-entity.csv` as appropriate.

## Unknown entities

To keep the datasets up-to-date on the platform, we need to check "unknown entity" issues and assign entities. This happens when a provider updates their data and adds records with reference values we don't already have on the platform.

> **This runs automatically each weekday evening as part of the [Config Evening Pipeline](#config-evening-pipeline).** For what the batch assign script actually does, its scopes, how to run it manually, and the full list of validation findings it can raise, see [Assign Entities](../../How-To-Guides/Maintaining/Assign-entities/).

## De-duplication of conservation-area data

The purpose of this process is to ensure that duplicate data is not stored unnecessarily for the conservation-area dataset generated by an organisation which may have also been provided by Historic England(HE).

> **The initial deduplication of conservation area geographies now runs automatically each weekday evening as part of the [Config Evening Pipeline](#config-evening-pipeline).** The manual steps below relate to the subsequent review of duplicate entities in Power BI and preparing corrections to `old-entity.csv` — this part still requires human judgement and is not automated.

The steps required for this process:-

1. Run the add-data tasks for conservation-area dataset (making a note of how many entities were added in the lookup file).

2. Raise the pull-request(PR) and ensure that it has been merged into the main branch so that the duplicate entities are picked up by the expectation report on the following day.

3. `DO NOT` inform the organisation at this stage.

4. On Power BI navigate to the "Digital Planning" workspace then to the "Planning Data Monitoring" report from where you select the "Duplicate Conservation Area" page.(Link\_[0])

5. Click on the reports TITLE in order for the options panel to appear to right hand side

6. Click on the three dots for the more options dropdown menu, from which you select "Export data" to download the output.

7. Open up the exported file to show the HE duplicate entites.

8. Filter on the message column for "complete_match" criteria

9. Filter on the entity_a_organisation.name column for the organisation Historic England and filter on the entity_b_organisation.name column for the organisation for which the data was added on the previous day (re:step 1)

10. Copy the entities in columns entity_a and entity_b

11. Prepare the data to be appended to the old-enity.csv located at Link\_[1] in following format
    where entity_a=old-entity and entity_b=entity
    e.g. 44012512,301,44013703,,redirect Historic England duplicate to LPA entity,2025-08-28,

12. `Also DO NOT forget` to update the entity-organisation file located at Link\_[2]

13. When this change is merged, check the PowerBI report to confirm the duplicate entities have been fixed.

[0]: https://app.powerbi.com/groups/80b5c556-2a94-402f-bd6a-225e9a9b6561/list?experience=power-bi
[1]: <config/pipeline/conservation-area/old-entity.csv at main · digital-land/config>
[2]: <config/pipeline/conservation-area/entity-organisation.csv at main . digital-land/config>

## Retire MHCLG conservation-area data

### Trigger

As with local plans, MHCLG set up conservation-area and conservation-area-document endpoints on behalf of LPAs before those LPAs published their own authoritative data. This is a separate process from the [de-duplication of conservation-area data](#de-duplication-of-conservation-area-data) above, which deals with Historic England duplicates — this script only ever considers MHCLG's own endpoints and explicitly skips Historic England.

Once an LPA has an active authoritative endpoint of their own, the MHCLG endpoint is redundant and should be retired.

### How the script works

The script (`retire-mhclg-ca-data.py`), found in the [Config repository](https://github.com/digital-land/config), processes the `conservation-area` and `conservation-area-document` datasets in turn:

- Fetches all endpoints for the dataset from `reporting_historic_endpoints` in the performance Datasette database, and groups them by LPA (skipping Historic England).
- For each LPA, checks whether it has both an MHCLG-owned endpoint and at least one **active** authoritative endpoint (a non-MHCLG endpoint with no end-date). Only LPAs with both are retired — an LPA with MHCLG data and no active alternative yet is left alone.
- Retires the matching MHCLG endpoints by adding today's date to `collection/conservation-area/endpoint.csv` and `source.csv`.
- Adds any resources previously collected from those endpoints to `collection/conservation-area/old-resource.csv` with status `410`, skipping resources already recorded there from a previous run.
- Finishes with a summary of how many of the retired LPAs are part of the ODP programme.

Unlike `retire-mhclg-plan-data.py` below, this script works at the **endpoint** level rather than the entity level — it retires the whole MHCLG-owned endpoint and its resources for a dataset/LPA, rather than individually flagged entities.

> **This process runs automatically each weekday evening as part of the [Config Evening Pipeline](#config-evening-pipeline).** The steps below are for running it manually, for example to investigate an issue.

### Task

1. Clone the [Config repository](https://github.com/digital-land/config) if you have not already done so, then create and activate a virtual environment.

2. Run the script from the root of the repository: `python3 .github/scripts/retire-mhclg-ca-data.py`

3. Review the output. The script logs, per dataset, how many LPAs had both MHCLG and active authoritative data (and were therefore retired), how many had MHCLG data only, and the ODP coverage of the retired LPAs.

4. Commit and merge the changes to `collection/conservation-area/endpoint.csv`, `source.csv` and `old-resource.csv`.

### Test

Once merged, confirm the retired endpoints no longer appear as active sources for the affected LPAs, and that their resources show status `410` in `old-resource.csv`.

## Retire MHCLG fake template data for local plans and plan timetables

### Trigger

When MHCLG was setting up the local plans system, it pre-seeded placeholder ("fake template") data in the `local-plan` and `plan-timetable` datasets on behalf of LPAs. This was done so that the platform had something to show before LPAs had published their own data.

Once an LPA publishes its own authoritative data, the MHCLG placeholder data is redundant and should be retired. If it is not retired, duplicate or conflicting records exist on the platform.

### How the script works

The script (`retire-mhclg-plan-data.py`), found in the [Config repository](https://github.com/digital-land/config), processes both datasets in sequence:

**plan-timetable:** MHCLG placeholder entities fall within the entity range `5101702–5109686`. For each LPA that has provided new authoritative data outside this range, the script identifies the corresponding MHCLG-owned entity range in `pipeline/local-plan/entity-organisation.csv` and retires those entities.

**local-plan:** MHCLG placeholder entities fall within the entity range `4220656–4220966`. The script generates the expected fake reference for each LPA (in the format `{lpa-slug}-new-local-plan`) and finds the matching MHCLG-owned entity in `pipeline/local-plan/lookup.csv`.

For both datasets, the script appends retired entities to `pipeline/local-plan/old-entity.csv` with status `410` and today's date. It includes several safety checks before writing anything — it verifies there is no overlap between the MHCLG placeholder entities and the LPA's real data, and that every LPA with authoritative data has a corresponding placeholder to retire.

Note: the script skips LPAs that updated MHCLG placeholder data in-place (i.e. their entities fall within the MHCLG range), as those records were overwritten rather than duplicated, so no retirement is needed.

> **This process runs automatically each weekday evening as part of the [Config Evening Pipeline](#config-evening-pipeline).** The steps below are for running it manually, for example to investigate an issue.

### Task

1. Clone the [Config repository](https://github.com/digital-land/config) if you have not already done so, then create and activate a virtual environment.

2. Run the script from the root of the repository: `python3 .github/scripts/retire-mhclg-plan-data.py`

3. Review the output. The script will log which LPAs had MHCLG template data identified for retirement, and print a summary of how many entities were retired per dataset. If no LPAs have newly provided authoritative data since the last run, it will exit cleanly with no changes.

4. If the script raises a `ValueError` naming one or more LPAs, this means those LPAs have provided real data but the script could not find a corresponding MHCLG placeholder to retire. This is a data integrity issue that needs investigating before re-running — check that the relevant rows exist in `pipeline/local-plan/lookup.csv` and `pipeline/local-plan/entity-organisation.csv`.

5. Commit and merge the changes to `pipeline/local-plan/old-entity.csv`.

### Test

Once merged, confirm the retired entities are no longer active on the platform by checking [Datasette](https://datasette.planning.data.gov.uk/) for the relevant `local-plan` or `plan-timetable` entities. The retired entity numbers should now redirect (HTTP 410) rather than return active records.

## Redirect MHCLG plan duplicates

### Trigger

The script above retires MHCLG *fake template* placeholders — rows with no real content, identified structurally by their `{lpa-slug}-new-local-plan` reference. Separately, MHCLG also researched and entered **real** plan data on some LPAs' behalf ahead of the LPA publishing their own version (quality `some`, versus `authoritative` once the LPA has submitted). Once the LPA's own version is published, the MHCLG-seeded version is a duplicate and should redirect to it — but because LPAs often rename or reword plans when they submit, these duplicates can't be found by reference or entity range, so this script compares the published content instead.

### How the script works

The script (`redirect-mhclg-plan-duplicates.py`), found in the [Config repository](https://github.com/digital-land/config), runs in two passes:

1. **`local-plan` / `waste-plan` / `minerals-plan`:** for each MHCLG-seeded row (excluding fake template placeholders), the script looks for authoritative rows from the same LPA with an identical `document-url`, or identical `name`/`description` text (case-insensitive). A seeded row is only redirected when it matches **exactly one** authoritative row — if it matches more than one (for example, an LPA reuses a generic name like "Local Plan" for both an adopted and an emerging plan), it's left alone and flagged for manual review instead of guessed at.

2. **`plan-timetable`:** once a plan reference has been confirmed retired (by pass 1, or by a previous run), the script looks for MHCLG-seeded timetable milestones for that plan with an **exact** match — same organisation-entity, `plan-event`, and date — to an authoritative milestone, and redirects only those. Milestones with the same event but a different or missing date are logged as possible matches for manual review, but never redirected automatically — plan-event labels (`plan-adopted`, `submit-plan-for-examination`, etc.) are a small vocabulary reused across a council's old and new plan cycles, so matching on the event alone risks pairing up unrelated real-world events.

Confirmed redirects are appended to `pipeline/local-plan/old-entity.csv` with status `301` (redirect) and the matching authoritative entity — unlike the `410` (retired, no successor) status used by `retire-mhclg-plan-data.py` above.

> **This process runs automatically each weekday evening as part of the [Config Evening Pipeline](#config-evening-pipeline).** The steps below are for running it manually, for example to investigate an issue.

### Task

1. Clone the [Config repository](https://github.com/digital-land/config) if you have not already done so, then create and activate a virtual environment.

2. Run the script from the root of the repository: `python3 .github/scripts/redirect-mhclg-plan-duplicates.py`

3. Review the output. The script logs, per dataset, how many duplicates were confirmed and redirected, plus any ambiguous matches (multiple candidate authoritative rows) or possible plan-timetable matches (same event, different date) that need manual review.

4. Commit and merge the changes to `pipeline/local-plan/old-entity.csv`. For anything flagged as ambiguous or a possible match, review it manually and add a redirect by hand if appropriate.

### Test

Once merged, confirm the redirected entities return an HTTP 301 to the matching authoritative entity — rather than an active record — by checking [Datasette](https://datasette.planning.data.gov.uk/) for the relevant `local-plan`, `waste-plan`, `minerals-plan` or `plan-timetable` entities.
