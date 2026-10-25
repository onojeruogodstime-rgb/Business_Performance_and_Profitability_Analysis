# Stochastic Analysis of NHS Emergency Demand

**Domain:** healthcare analytics · time-series forecasting · uncertainty

## Research question
How can historical aggregate NHS emergency-care activity be analysed to characterise demand variability and evaluate forecasts that may support operational planning?

## Objectives
- Describe trend, seasonality, calendar effects and unusually high-demand periods.
- Compare simple baselines with suitable statistical forecasting models.
- Evaluate forecasts using chronological holdout or rolling-origin testing.
- Report uncertainty and discuss implications for planning.
- Document changes in reporting, service definitions and external shocks that can limit model reliability.

## Data plan
Prefer an official, openly accessible aggregate source such as NHS England A&E Attendances and Emergency Admissions statistics. Record the exact table, series, geography, frequency, units, publication date, download URL and permitted-use terms. Do not upload patient-level or confidential records.

**Exact data source and period:** to be recorded after selection and verification.

## Proposed methods
Python, pandas, statsmodels, scikit-learn and Matplotlib. Begin with naïve and seasonal-naïve baselines; compare moving-average or exponential-smoothing methods and SARIMA where the series supports them. Use MAE, RMSE and MASE where appropriate, plus prediction-interval coverage and width. Do not assume a more complex AI model is better without evaluation evidence.

## Workflow
1. Acquire permitted aggregate data and preserve metadata.
2. Validate dates, missing periods, revisions and definitions.
3. Explore the series and seasonal structure.
4. Split chronologically into training and test periods.
5. Fit baselines and candidate models using training data only.
6. Compare errors, inspect residuals and assess uncertainty.
7. Present forecasts with limitations and operational interpretation.

## Status
This is a research plan and starter project, **not a claim that a final forecast has been fitted or validated**. Add a cited dataset, executed notebook, charts, model-comparison table and verified findings after completing the workflow.

## Ethics and limitations
Forecast accuracy does not prove that a staffing or capacity intervention will improve patient outcomes. Use aggregate public statistics unless explicit approvals authorise another source.

See [portfolio index](../../PORTFOLIO_INDEX.md).
