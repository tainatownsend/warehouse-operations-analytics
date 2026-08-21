# Warehouse Operations Analytics

A business-focused data science portfolio project for analyzing logistics and warehouse operations.

## Project Goal

This project investigates how operational data can be transformed into decision-ready insights for logistics leaders. The first version focuses on understanding the data model, establishing trustworthy operational metrics, and identifying opportunities for deeper analysis.

## Business Framing

The project is designed around four questions:

1. Which operational metrics best describe logistics performance?
2. Where do delays, capacity constraints, or inefficient resource use appear?
3. Which patterns deserve investigation by an operations leader?
4. What additional data or modeling would be required to support better decisions?

See the [Project Charter](PROJECT_CHARTER.md) for the initial scope and success criteria.

## Planned Workflow

1. Business understanding
2. Data understanding
3. Data quality assessment
4. Data preparation
5. Exploratory analysis
6. KPI development
7. Insight communication
8. Predictive modeling only if it adds business value

## Repository Structure

```text
warehouse-operations-analytics/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── reports/
│   └── figures/
├── sql/
├── src/
│   └── warehouse_operations_analytics/
├── tests/
├── PROJECT_CHARTER.md
├── requirements.txt
└── README.md
```

## Data

The selected source is the public **Logistics Operations Database** dataset published on Kaggle.

The raw dataset is intentionally not committed during this foundation PR. Data acquisition, licensing notes, file inventory, and integrity checks will be handled in the next data-understanding delivery.

See [`data/README.md`](data/README.md).

## Current Status

**PR-0002 — Data Understanding (in progress)**

- [x] Business problem and analytical scope framed
- [x] Fourteen source tables identified
- [x] Core key candidates for routes, loads, and trips reviewed
- [x] Tested relationships showed no orphan foreign keys
- [x] Loads and trips were observed as one-to-one in the reviewed snapshot
- [ ] Re-run the evidence from a reproducible repository workflow
- [ ] Complete the wider relationship map and temporal coverage review
- [ ] Publish quality limitations and their business implications

See [Data Understanding Status](DATA_UNDERSTANDING_STATUS.md) for the evidence boundary and next validation gate.

### Reproducible Evidence Command

After restoring all fourteen source CSVs under `data/raw/`, run:

```bash
python scripts/build_data_understanding_evidence.py
```

The command is strict by default: an incomplete snapshot stops the build. It
generates checksummed inventory, column/null/uniqueness profiles, temporal
coverage, configured relationship tests, and an evidence-boundary report.
Use `--allow-partial` only for diagnostic profiling; partial output is not a
completion artifact for PR-0002.

Relationships are intentionally empty in the initial config until the source
schema is restored and the exact table/column pairs can be confirmed. This
prevents remembered or guessed links from being published as evidence.

The pull request quality gate runs Ruff and Pytest in GitHub Actions without
requiring the private raw snapshot.

## Principles

- Business questions before algorithms
- Evidence over activity
- Reproducibility by default
- Raw data remains immutable
- Modeling must earn its place
