# Business Problem | Discovery Worksheet

> **Status:** To be completed by the project owner. Start here **before writing code**.

This document records public-safe, reviewable decisions. In the learning phase, complete the companion Business Problem Canvas in your personal Google Drive. Transfer confirmed, public-safe answers here when ready; do not copy any confidential workplace information or private Google Drive links.

## 1. Situation (business understanding)

- **What is the concrete planning problem?** _To be answered._
- **What happens today without a forecast?** _To be answered._
- **Why is this problem important?** _To be answered._
- **What remains unknown?** _To be answered._

## 2. Stakeholder and decision

- **Who would act on this study?** _To be answered._
- **What decision can realistically change?** _To be answered._
- **When must the decision be made?** _To be answered._
- **Which actions, costs and constraints exist?** _To be answered._

## 3. Analytical question and testable hypothesis

- **Research question:** _Draft: Can item-store future unit sales be predicted better than a simple seasonal rule? Validate scope._
- **Hypothesis:** _To be answered._
- **What observation would contradict the hypothesis?** _To be answered._

## 4. Forecasting contract

- **Target:** _Proposed: daily units sold, not unconstrained demand._
- **Unit of analysis:** _Proposed: item × store × day._
- **Forecast origin / cutoff:** _To be defined._
- **Horizon:** _Proposed: 7 or 28 days. Select based on decision._
- **Available-at-prediction-time features:** _To be inspected._
- **Demand vs sales vs DC throughput:** _Distinct measures. Do not conflate them._

## 5. Data and limitations

- **Proposed public source:** [M5 Forecasting Accuracy](https://www.kaggle.com/competitions/m5-forecasting-accuracy/data).
- **Terms / reuse:** _To be checked before downloading/redistributing._
- **Time coverage, quality and join keys:** _To be inspected from actual files._
- **Stockout/zero-sales ambiguity:** _To be investigated._

## 6. Method and evaluation

- **Baseline:** _Candidate: same weekday of previous week, where valid._
- **Validation:** _Rolling-origin time splits; no random split._
- **Metric / segment cuts:** _To be chosen after inspecting the data._
- **Decision threshold for added model complexity:** _To be decided._

## 7. Results, business impact and disclosure

- **Measured technical results:** _None yet._
- **Business recommendation:** _Pending evidence._
- **What cannot be concluded:** _Prediction accuracy alone does not prove replenishment or cost impact._
- **Disclosure:** _Only independent public analysis. Never publish corporate data or proprietary rules._

## First exercise (Sprint 0)

Answer these four questions **in your own words** in the Canvas:

1. What does a planning team struggle with if it cannot forecast future sales?
2. What business decision could the forecast actually support?
3. Which variable fits the public dataset: orders, units sold or labor hours? Why?
4. How far in advance should the forecast be delivered, and why?

**Definition of done:** four reasoned answers and a provisional forecast target, clearly distinguishing recorded sales from unconstrained demand and warehouse capacity.
