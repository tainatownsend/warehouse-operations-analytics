# Retail Demand Forecasting | Walmart M5

> **Status:** Discovery (not started) · **Track:** Independent public-data portfolio · **Last updated:** 2026-10-16

## At a glance

**Goal:** Investigate whether we can estimate near-term retail unit sales more accurately than transparent seasonal baselines, with validation that supports credible planning decisions.

**Business decision:** _To be defined in the Business Problem Canvas._ The future analysis may inform inventory replenishment or merchandise planning, but this project will **not** claim realized cost reductions or distribution-center labor savings.

**Dataset:** [M5 Forecasting Accuracy (Walmart)](https://www.kaggle.com/competitions/m5-forecasting-accuracy/data), subject to the competition's data-use terms.

**Current results:** None. No data have been downloaded for this study, no models trained, and no predictive improvements measured.

## Business problem

Retail planning involves uncertainty about how many units will sell in upcoming days. A credible forecast should help a defined decision-maker choose among feasible planning actions. This project will first clarify the decision, forecast target, horizon, and information available at forecast time.

See [Business Problem](BUSINESS_PROBLEM.md) for the editable, version-controlled question set. The working Canvas in Google Drive is used for guided learning; only independently developed, public-safe conclusions should be promoted here.

## Questions to answer before coding

- Who makes the planning decision, and when?
- What action could the forecast change?
- Are we predicting recorded **unit sales** or underlying demand? Sales may be constrained by inventory availability.
- Do we need a 7-day or 28-day forecast, and at which item/store granularity?
- What simple rule must an advanced method outperform?
- Which data are actually known at each forecast origin?

## Planned approach, not completed work

1. Define the business decision and the forecasting contract.
2. Inspect public M5 files, time coverage, keys, calendar and price information.
3. Choose a small reproducible item/store subset suitable for Google Colab.
4. Examine zeros, intermittency, trend and weekly/holiday effects.
5. Build seasonal-naive baselines.
6. Evaluate using rolling-origin backtests and an untouched later holdout.
7. Consider a more complex model only if it is justified by results and planning needs.
8. Report error, bias, edge cases, limitations and a business interpretation.

**Possible metrics (not yet selected):** MAE, MASE and forecast bias. WRMSSE may be considered if the full hierarchical competition setting is used appropriately.

## Planned portfolio deliverables

- Public-source data dictionary and acquisition instructions
- SQL/Python exploratory analysis and reproducible Colab notebooks
- Seasonal baseline, temporal backtests and model comparisons
- Executive summary with action, uncertainty and limitations

Nothing above is marked complete until independently verified.

## Data rights and confidentiality

This portfolio uses public data and independently authored code only. No lululemon data, proprietary SQL, business rules, facility identifiers, performance metrics, corporate screenshots or company-trained models belong in this repository. The public Walmart M5 study is **not** an anonymized version of a company dataset.

Do not redistribute M5 raw data without verifying the applicable competition terms.

## Reproduction

_Not available yet._ Notebook links, requirements and exact run instructions will be added once the initial public-data experiment exists.

## Learning milestones

- [ ] Business Problem Canvas reviewed
- [ ] Forecast target and decision defined
- [ ] Public data terms checked and files inspected
- [ ] Data dictionary and basic EDA completed
- [ ] Seasonal baseline computed
- [ ] Time-based evaluation validated
- [ ] Advanced model evaluated only if warranted
- [ ] Findings translated into a documented business recommendation

## Roadmap context

This is the **public** track of Project 01 in a four-project Data Science portfolio path. The separate corporate application, if authorized, stays within employer-approved infrastructure and documentation. Both tracks share transferable analytical skills, not proprietary data or code.
