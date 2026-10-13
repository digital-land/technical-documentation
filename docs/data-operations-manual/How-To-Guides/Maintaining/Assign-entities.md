---
title: Assign Entities
---

## Purpose

When a provider updates their data on an endpoint we are collecting from and adds records with reference values we do not already have on the platform, the pipeline raises an `unknown entity` issue — it cannot resolve those records to a stable Planning Data entity number on its own.

The `.github/scripts/batch_assign_entities.py` script in the [Config repository](https://github.com/digital-land/config) automatically assigns entity numbers for resources flagged this way, across three scopes:

- **ODP** — datasets supported by [Open Digital Planning funding](https://datasette.planning.data.gov.uk/digital-land?sql=select+rowid%2C+dataset%2C+cohort%2C+notes%2C+project%2C+provision_rule%2C+role%2C+specification+from+provision+where+%22project%22+%3D+%3Ap0+group+by+dataset&p0=open-digital-planning).
- **Mandated** — datasets LPAs are legally required to provide, including `brownfield-land` and `developer-contributions`.
- **Single-source** — data from authoritative sources or seeded data received from the Data Design Team.

> **This runs automatically every weekday evening for `odp` and `mandated`, as part of the [Config Evening Pipeline](../../Tutorials/Monitoring-Data-Quality/Config-Evening-Pipeline/#config-evening-pipeline). `single-source` runs separately, Sundays only.** The sections below cover what the script actually does and how to run it manually — for example to investigate an issue, resume a failed single-source batch run, or process specific resources.

## How it works

For each resource with an `unknown entity` issue, the script:

1. **Fetches** the resource (downloading it if it isn't already cached locally).
2. **Assigns** — runs digital-land-python's `check_and_assign_entities`, which transforms the resource and writes any newly-assigned entities into a *scratch* copy of `lookup.csv` (`var/cache/assign_entities/<collection>/pipeline/lookup.csv`), not the real one.
3. **Validates** the result against the checks in the [table below](#validation-findings). This is where it decides whether the assignment looks safe.
4. **Promotes** — only if nothing blocking was found, the scratch `lookup.csv` is copied over the real `pipeline/<collection>/lookup.csv`, and new entity-number ranges are appended to `entity-organisation.csv`.

A resource that fails validation was still fully assigned in step 2 — that work is simply never promoted in step 4, so it leaves no trace in the real `lookup.csv`. This is intentional, not a bug: it's why a blocked resource shows no `lookup.csv` diff even though entity assignment ran to completion for it.

### Outcome and severity

Every row written to the output summary (see [Interpreting the output](#interpreting-the-output) below) has a `status`:

| Status | Meaning |
| --- | --- |
| `assigned` | The resource was promoted; its new entities are in the real `lookup.csv`. |
| `skipped` | A no-op, not a failure — there was nothing to promote either way. |
| `blocked` | A data-quality finding stopped promotion. Needs a reviewer's decision. |
| `failed` | A pipeline or engineering problem, not a data-quality one. Needs an engineer, not a data reviewer. |
| `warn` | A separate, non-blocking severity tier: logged for visibility, but the resource is still promoted. |

### Scope differences

`odp` and `mandated` process whatever Datasette currently reports as outstanding for that scope, in one pass.

`single-source` additionally supports `--batch-size`/`--start-batch`: it self-commits after each batch and is resumable if a run fails partway through — useful because a full single-source run can take hours. It's also the only scope where the organisation is passed as blank to `check_and_assign_entities`, and only for the `listed-building` dataset specifically — that dataset's per-entity organisation isn't reliable enough on single-source to assume everything in a resource belongs to the endpoint's registered organisation. Every other single-source dataset gets its real organisation. That same combination (single-source + `listed-building`) is also the only case where a blank `organisation` is never backfilled and never gets an `entity-organisation.csv` range — both deliberate, since the right organisation genuinely isn't known.

### `--skip-checks`

Bypasses *all* validation in step 3 above — not just the duplicate/retention/missing-field checks, but also the `current_resource_empty` guard and the `invalid_uri_issue` lookup. With it set, anything `check_and_assign_entities` assigns gets promoted unconditionally. Use with caution.

## Running it manually

Clone the [Config repository](https://github.com/digital-land/config) if you haven't already, create and activate a virtual environment, then run:

```bash
python3 .github/scripts/batch_assign_entities.py --scope [SCOPE]
```

Available options:

| Option | Default | Purpose |
| --- | --- | --- |
| `--scope` | `odp` | `odp`, `mandated` or `single-source`. |
| `--resources` | all outstanding | Comma-separated resource hashes, to target specific resources instead of everything in scope. |
| `--skip-checks` | off | Bypasses all validation — see above. Use with caution. |
| `--commit` / `--no-commit` | `--commit` | Whether to commit and push successful assignments to `main`. Use `--no-commit` for a dry run. |
| `--batch-size` | `0` (process all) | Resources per run, for `single-source`. |
| `--start-batch` | `1` | 1-indexed batch to resume from after a failed run, with `--batch-size`. |
| `--triggered-by` | none | Identifier for the actor/system that triggered the run, recorded in the commit message. |

On first run, the script downloads `issue_summary.csv` (the current `unknown entity` backlog for every scope) to the repository root, downloads each resource it needs into a local `resource/` folder, and deletes them again once successfully processed.

## Interpreting the output

The script writes one row per finding (plus one summary row per resource) to `batch_assign_summary_[scope].csv`. This file is also what the [Manage service](https://manage.planning.data.gov.uk/) reads from for the manual assign-entities review flow, so users can see exactly which resources the script could not safely assign automatically.

The summary includes these columns:

- `dataset` - the dataset or pipeline being processed
- `resource` - the current resource hash
- `organisation` - the organisation associated with the resource or flagged row
- `reference` - the provider reference where the finding relates to a specific entity
- `status` - see the [outcome and severity](#outcome-and-severity) table above
- `entities_created` - how many new entities this resource's row produced (`0` unless `status` is `assigned`)
- `error_code` - the validation finding or Python exception type; blank for the `assigned` row itself
- `message` - extra context from the script

Failed resource downloads are printed in the terminal summary as `Failed Downloads`; they are not written as normal validation rows because the resource was never processed.

### Terms used below

The script compares the latest ("current") resource for an endpoint with the previous ("old") resource it collected for the same endpoint, to decide whether the entities it just assigned look safe.

- **current resource** - the latest resource being processed. This is the file linked from the `unknown entity` issue.
- **previous resource** - the older transformed resource for the same endpoint, found from historic endpoint data and downloaded from `files.planning.data.gov.uk` for comparison.
- **current entity** / **previous entity** - an entity number found in the current / previous transformed resource.
- **new entity** - a current entity that was not present in the previous resource - the ones the script is trying to validate.

For example, if the previous resource contained entities `44000001`, `44000002` and `44000003`, and the current resource contains those three plus `44000004`, then `44000004` is the new entity. If the current resource contains no entity numbers that were missing from the previous one, the script records `current_resource_no_new_entities`.

### Validation findings

| Error code | Status | What it means | Why it is flagged | Example |
| --- | --- | --- | --- | --- |
| `previous_resource_not_found` | `blocked` | The script could not fetch or read the previous transformed resource for that endpoint, despite real history existing for it. | Without the previous resource, the script cannot tell which entities are genuinely new or whether current rows duplicate existing platform entities. | Datasette returns no previous resource hash for the endpoint, or `https://files.planning.data.gov.uk/[collection]-collection/transformed/[dataset]/[old-resource].csv` cannot be downloaded. |
| `new_endpoint_no_history` | `warn` | The endpoint has never had an earlier, superseded resource - this is genuinely its first ever resource. | There is nothing to compare against by definition, which is different from a fetch failure (`previous_resource_not_found`) - every entity is new, so this doesn't block the first assignment. | A brand-new endpoint is added for an LPA that has never provided this dataset before. |
| `previous_resource_empty` | `blocked` | The previous transformed resource exists but has no entity rows. | If the old resource has no entities, every current entity appears new and the comparison is not reliable. | The previous transformed CSV downloads successfully but only contains headers, or contains no rows with an `entity` value. |
| `current_resource_empty` | `failed` | The current transformed resource produced by assignment has no rows. | Signals an upstream/pipeline problem, not a data-quality issue with any actual rows - it needs an engineer to check source/pipeline health, not a reviewer to make a data decision. | The file in `var/cache/assign_entities/transformed/[resource].csv` is empty after `check_and_assign_entities` runs. |
| `current_resource_no_new_entities` | `skipped` | The current resource does not contain any entity numbers that were not already present in the previous resource. | A pure no-op, not a failure - there is nothing to promote either way. If this wasn't expected, the issue may already be resolved, the wrong resource may have been processed, or the data may have changed since the issue summary was generated. | The previous and current resources both contain entities `44000001` to `44000010`, with no additional entity numbers. |
| `low_entity_retention` | `blocked` | Fewer than the retention threshold's percentage (90% by default) of the previous resource's entities are still present in the current one. | Replaces an earlier growth-only check entirely - genuine growth (a source adding records) is safe on its own, but old entities disappearing at roughly the rate new ones appear is the fingerprint of a reference-format change (churn), which this catches instead. | The previous resource had 100 entities; only 80 of them are still present in the current resource (80% retention, below the 90% threshold) - even if the current resource also gained new entities. |
| `duplicate_entity_all_fields` | `blocked` | A new entity matches an old entity when comparing all fact fields except `reference` and `entry-date`. The script builds a fingerprint from the remaining fact field and value pairs. | If all the compared facts match an existing entity, the provider may have changed the reference for the same real-world thing. Creating a new entity number could create a duplicate. If the previous entity has any compared fact field that the current entity does not have, or the current entity has any extra compared fact field, the fingerprints will not match and this check will not flag it as a duplicate. | A conservation area has the same name, organisation and geometry as an existing entity, but the provider changed the reference from `CA-001` to `CON-001`. If any compared fact field is present on the previous entity but absent from the current entity, this check will pass it as not being a duplicate. |
| `possible_reference_churn_fuzzy_match` | `warn` | A new entity is a *likely* match for an existing one - either a geometry overlap of 90%+ or a name similarity of 90+/100 with an old entity - but not an exact fingerprint match. | Companion to `duplicate_entity_all_fields`: that check requires every other field to be byte-identical, so it misses a new entity that's probably the same real-world feature but with a slightly adjusted boundary or a lightly-edited name alongside the reference change. Lower confidence than an exact match by design, so this doesn't block - it's a prompt to review, not a rejection. | A listed building's boundary shifts slightly and its reference changes, but the name is unchanged - the geometry overlap is 95%, below an exact-match fingerprint but above the similarity threshold. |
| `duplicate_reference_organisation` | `blocked` | A new entity has the same `reference` and `organisation` as an old entity, regardless of prefix. (This absorbed what used to be a separate `duplicate_prefix_reference_organisation` check - within one dataset's output, prefix is always the dataset itself, so the two checks were provably identical.) | This catches duplicate provider identifiers even when another field has changed. It is broader than an exact-fingerprint match. | A provider republishes reference `TPO-99` for the same organisation and the script tries to create a new tree preservation order entity for it. |
| `duplicate_reference_organisation_in_new_resource` | `blocked` | Two or more entities inside the current resource have the same `reference` and `entry-date` (matching the pipeline's own "reference values are not unique" issue scope, rather than reference + organisation). | The script cannot know whether these rows are duplicate records for the same thing or separate things with duplicated identifiers. | The current transformed resource contains two entities with the same `reference` and `entry-date`. |
| `missing_organisation` | `warn` | A current entity is missing its `organisation` value. | digital-land-python's own lookup phase only requires `prefix` and `reference` to assign an entity, so this doesn't block assignment the way a missing reference would. The script backfills the real `lookup.csv` row with the endpoint's registered organisation afterwards, so this is visibility, not a rejection. | The transformed rows for entity `44001234` include a `reference` field but no `organisation` field. |
| `missing_reference` | `blocked` | A current entity is missing its `reference` value. | The lookup maps provider references to entity numbers. Without the reference, digital-land-python's lookup phase can never resolve this entity, so it can never actually be assigned - future collections cannot reliably resolve the same record either. | The transformed rows for entity `44001234` include `organisation` but the `reference` field is blank. |
| `invalid_uri_issue` | `warn` or `blocked` | The same resource also appears in the current invalid URI issue summary. `warn` when the specific affected entities could be identified from the local issue log (those entities alone are excluded from promotion, pending the URI being fixed upstream); `blocked` for the whole resource only if the issue log couldn't resolve it to specific entities. | Entity assignment may have worked for the rest of the resource, but an invalid URI is a separate, known quality issue that needs manual review before that specific entity is accepted. Excluding only the affected entities (rather than the whole resource) avoids wrongly discarding valid, already-matched existing entities in a multi-authority resource. | A brownfield land resource has unknown entities and also invalid document URI values in the issue summary; the affected entities are identified and excluded, the rest of the resource is still promoted. |
| Python exception name, for example `RuntimeError`, `FileNotFoundError`, `KeyError` or another exception type | `failed` | The script raised an exception outside the validation checks. | An unhandled exception is a pipeline/engineering problem, not a data-quality finding a reviewer can action. The `message` column and terminal output should be used to diagnose the failure. | `RuntimeError` can be raised if a required command such as `git` or `gh` fails. `FileNotFoundError` can be raised if an expected local file is missing. |

## Validating conservation area entities

If the entities belong to the `conservation-area` dataset, check for duplicates using the endpoint checker (see step 3 in [Validating an endpoint](../Validating/Validate-an-endpoint/)). Once new `lookup.csv` entries have been generated, use the `Duplicates with different entity numbers` output from the endpoint checker to replace any newly-generated entity numbers that are actually duplicates with the existing entity number they match.
