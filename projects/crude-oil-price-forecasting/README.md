# Crude Oil Price Forecasting

**Domain:** energy markets · statistical time series · forecast evaluation

## Project question
How well do classical time-series methods forecast a documented crude-oil price series, and how does uncertainty change with forecast horizon?

Earlier project notes describe R analysis of daily oil prices over 2009–2024 aggregated quarterly, including stationarity checks, information criteria, residual diagnostics and forecasts. Verify those details against the actual source file and executed analysis before publishing numerical findings.

## Objectives
- Record the benchmark, currency, units, frequency, source and data licence.
- Visualise the series and assess transformations, trend and seasonality.
- Compare a naïve baseline with ARIMA and exponential smoothing.
- Inspect residuals and evaluate out-of-sample forecast errors.
- Present prediction intervals and discuss structural breaks and market shocks.

## Methods
R, forecast, tseries and ggplot2. Use chronological holdout or rolling-origin evaluation and suitable metrics such as MAE, RMSE and MASE. Information criteria support model comparison but do not replace out-of-sample forecast evaluation.

## Data requirements
Record the exact source and download URL, series definition, date range, price units, frequency, aggregation rule, missing-value treatment and terms of use.

## Status
Project page and starter script are provided. **Do not report a forecast or accuracy metric as verified until the data and model outputs have been rerun and checked.**

See [portfolio index](../../PORTFOLIO_INDEX.md).
