# Decision Log

This log records modeling and business decisions, their rationale, and the evidence needed to revisit them. It does not claim models were trained.

| Date | Status | Decision | Rationale | Revisit when |
| --- | --- | --- | --- | --- |
| 2026-10-16 | Proposed | Start with the public Walmart M5 dataset for an independent forecasting study | Reproducible public learning; distinct from employer work | Dataset terms and grain have been inspected |
| 2026-10-16 | Open | Forecast horizon: 7 or 28 days | Depends on decision timing | Business Problem Canvas answers are reviewed |
| 2026-10-16 | Open | Target: daily recorded unit sales | Candidate target supported by M5 format; verify once files are available | Raw data have been inspected |
| 2026-10-16 | Proposed | Baseline before advanced ML, using temporal backtests | Transparent, leakage-aware evaluation | Data cadence and zero-sales behaviour are checked |

## New decision template

**Date:** YYYY-MM-DD  
**Status:** Proposed / Accepted / Rejected / Superseded  
**Decision:**  
**Alternatives considered:**  
**Reasoning and evidence:**  
**Risks / trade-offs:**  
**Revisit trigger:**  
