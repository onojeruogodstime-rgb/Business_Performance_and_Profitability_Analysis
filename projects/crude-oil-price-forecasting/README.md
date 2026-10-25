# Crude Oil Price Forecasting: ARIMA vs Exponential Smoothing

**Project type:** Statistical forecasting case study  
**Domain:** Energy markets · time-series analysis · forecast evaluation  
**Tools:** R · `forecast` · `tseries` · `ggplot2`

[← Portfolio index](../../PORTFOLIO_INDEX.md)

## Executive summary

This project compares classical time-series approaches for quarterly crude-oil prices. The accompanying academic analysis describes daily prices aggregated to quarterly means from **Q4 2009 to Q3 2024**, with prices expressed in US dollars per barrel. It reports a first-difference ARIMA model and a comparison against exponential smoothing (ETS).

The analysis report identifies **ARIMA(0,1,0)** as its preferred ARIMA specification. It reports a level-series Augmented Dickey–Fuller p-value of 0.5507 and a stable long-horizon point forecast near $88.62 per barrel. Its reported ARIMA and ETS error summaries are very close; ETS has a marginally lower reported RMSE, while the report argues ARIMA better represents the observed movement. These are **results transcribed from the submitted analysis, not independently reproduced results**. The source dataset, model-selection path, evaluation design and code still need to be checked before treating the figures as validated.

## Business question

How do ARIMA and exponential-smoothing methods compare when forecasting quarterly crude-oil prices, and how should decision-makers interpret forecast uncertainty in a market exposed to structural breaks and external shocks?

## Reported comparison

| Reported metric | ARIMA | ETS |
|---|---:|---:|
| RMSE | 9.9943 | 9.9945 |
| MAE | 7.5736 | 7.5727 |
| MAPE | 11.5677% | 11.5665% |
| MASE | 0.4030 | 0.4030 |

*Source: figures reported in the accompanying academic analysis. They have not yet been reproduced from the underlying data and should not be interpreted as a verified independent test-set benchmark.*

The differences are extremely small. A recruiter-facing interpretation should therefore avoid claiming that one method clearly dominates. A stronger evaluation would use a documented chronological holdout or rolling-origin backtest, compare against naïve benchmarks, and report uncertainty around the error differences.

## Analytical workflow

1. Validate the data dictionary, date coverage, price units and source permissions.
2. Aggregate daily prices into quarterly means using an explicitly documented rule.
3. Plot the series and examine missingness, outliers and structural changes.
4. Assess stationarity and differencing needs; use ACF/PACF as diagnostics rather than as the only selection criteria.
5. Fit a naïve benchmark, ARIMA and ETS on training data only.
6. Evaluate forecasts on the same untouched chronological test window.
7. Inspect residual autocorrelation and prediction intervals.
8. Document sensitivity to the evaluation window and major market disruptions.

## Reproducibility and data governance

The underlying dataset was described in the report as material supplied for a university assessment. Its redistribution rights have **not** been confirmed, so raw data and the submitted report are not included here. Before publication, record the original data provider, exact series/benchmark, download URL, licence, units, aggregation method and missing-value policy.

The R script is a reproducible workflow template and requires a permitted input file at `data/crude_oil_prices_daily.csv` with columns `date` and `price`. It must be run against the documented source data before its outputs can be considered verified.

## Limitations

- Classical univariate models do not explicitly include supply disruptions, geopolitical events, inventory levels, exchange rates or macroeconomic drivers.
- Long-horizon intervals can become very wide and do not guarantee coverage under structural breaks.
- AIC-based selection is not a substitute for genuine out-of-sample evaluation.
- Reported metrics are not independently reproduced in this repository.

## Next steps

- Verify and document the original dataset's licence and provenance.
- Re-run the pipeline from a clean R environment.
- Add a forecast-versus-actual chart, residual diagnostics and a baseline comparison.
- Add rolling-origin evaluation and compare results across evaluation windows.
- Publish only verified metrics and appropriately licensed data/figures.

See [the R analysis script](forecast_template.R).
