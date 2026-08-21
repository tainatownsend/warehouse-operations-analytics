# Data Understanding Status

## Purpose

This document separates what has been observed from what the repository can currently reproduce. It prevents provisional findings from being presented as fully validated evidence.

## Business Decision Supported by This Stage

Before defining KPIs or building models, the project must establish whether the relational and temporal structure is trustworthy enough to compare operational performance across routes, loads, trips, customers, facilities, drivers, and assets.

## Evidence Ledger

### Observation 1 — Core identifiers

- **Observation:** The reviewed route, load, and trip key candidates were populated and unique.
- **Hypothesis:** These fields can serve as stable entity identifiers.
- **Test performed:** Local uniqueness and null checks during the PR-0002 review.
- **Conclusion:** Promising, but not yet reproducible from the repository clone because the raw snapshot and generated evidence are absent.

### Observation 2 — Tested referential integrity

- **Observation:** No orphan records were found in the relationships tested so far.
- **Hypothesis:** The tested fact-to-master relationships are internally consistent.
- **Test performed:** Local cross-table validation.
- **Conclusion:** Supported only for the relationships that were actually tested; it does not establish full-model integrity.

### Observation 3 — Loads and trips

- **Observation:** Loads and trips behaved as a one-to-one relationship in the reviewed snapshot.
- **Hypothesis:** A load-level analytical grain may align with trip-level execution for this dataset.
- **Test performed:** Local cardinality comparison.
- **Conclusion:** Useful for model design, but it must be regenerated and checked for duplicate, missing, or many-to-many exceptions.

### Observation 4 — Temporal semantics

- **Observation:** Candidate fields exist for scheduling, dispatch, loading, delivery, purchase, and maintenance.
- **Hypothesis:** The dataset can support both operational-flow analysis and asset-lifecycle analysis.
- **Test required:** Date parsing, coverage, missingness, grain, timezone assumptions, and impossible-sequence checks.
- **Conclusion:** Not yet established.

## Reproducibility Blocker

The repository intentionally excludes raw data, and the reviewed fourteen-file snapshot is not available in this environment. The next evidence run requires the original CSV files to be restored under `data/raw/` while remaining ignored by Git.

## Required Evidence Package

The PR-0002 completion package must generate:

1. A fourteen-table inventory with row counts, column counts, file sizes, and checksums.
2. A column dictionary with inferred types and missingness.
3. Primary-key uniqueness and null tests.
4. Declared foreign-key orphan counts.
5. Relationship cardinality results.
6. Temporal coverage and invalid-sequence results.
7. An ERD with confirmed and provisional relationships visually distinguished.
8. A limitations section connecting data risks to business interpretation.

## Definition of Done for PR-0002

- The raw snapshot can be acquired from documented instructions without being committed.
- Every published observation is backed by a reproducible command and generated artifact.
- The relationship map distinguishes confirmed, rejected, and untested links.
- One authoritative time grain is recommended, with alternatives and limitations documented.
- The next analytical question is selected because the data can support it, not because a model is available.
