# Crude Oil Price Forecasting: ARIMA vs Exponential Smoothing

**Project type:** Statistical forecasting case study  
**Domain:** Energy markets · time-series analysis · forecast evaluation  
**Tools:** R · `forecast` · `tseries` · `ggplot2`

[← Portfolio index](../../PORTFOLIO_INDEX.md)

## Executive summary

This project compares classical time-series approaches for quarterly crude-oil prices. The accompanying academic analysis describes daily prices aggregated to quarterly means from **Q4 2009 to Q3 2024**, with prices expressed in US dollars per barrel. It reports a first-difference ARIMA model and a comparison against exponential smoothing (ETS).

The analysis report identifies **ARIMA(0,1,0)** as its preferred ARIMA specification and reports a forecast near $88.62 per barrel. The uploaded workbook is now available and has been run through a provisional reproduction pipeline. Because it mixes text dates with native Excel date cells, the date normalisation remains an explicit assumption and the reproduced metrics below must be treated as provisional until the original provider/date convention and exact oil benchmark are confirmed.

## Provisional reproduction from the uploaded workbook

The workbook contains 3,404 rows, 2 missing prices, and 1,329 native Excel date cells mixed with 2,075 text date cells. A provisional rule parses text dates as month-first and swaps month/day in ambiguous native date cells. This rule is consistent with the report's stated broad date coverage, but it must be checked against the original source before the analysis is treated as final. Duplicate dates are averaged; the one-observation 2024 Q3 is excluded from model fitting and evaluation.

The current comparison uses 59 quarterly means from Q4 2009 to Q2 2024 and the last 12 complete quarters as a chronological holdout:

| Model | MAE | RMSE | MAPE | MASE |
|---|---:|---:|---:|---:|
| Last-quarter naïve | 21.741 | 24.953 | 22.75% | 2.783 |
| ARIMA(0,1,0) with drift | 22.856 | 25.893 | 24.01% | 2.926 |
| ETS additive trend | 22.856 | 25.893 | 24.01% | 2.926 |

These results differ materially from the report's error summaries because the current comparison uses an explicit 12-quarter holdout and a naïve benchmark. Four quarters have fewer than 40 daily observations, including Q2 2010 (17 observations), so coverage and date parsing require further source-level validation. Do not claim that the report's original results have been reproduced yet.

Run `python reproduce_oil_workbook.py` after placing the workbook locally at `data/BSOM096_CrudeOilPrice.xlsx`. The script writes the quarterly series, holdout forecasts, metrics, audit summary and SVG charts to `outputs/`. The workbook itself is not committed to the public repository.

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

The R script remains a generic CSV-based workflow. The new Python workbook pipeline reproduces a provisional comparison directly from the supplied workbook, with the date policy and coverage issues disclosed. Neither workflow should be described as fully source-verified until the benchmark, provider, date convention and reuse terms are confirmed.

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

See the [provisional workbook reproduction script](reproduce_oil_workbook.py) and the [R CSV workflow](forecast_template.R).
