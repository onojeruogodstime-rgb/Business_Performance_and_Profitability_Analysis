# Stochastic Analysis of NHS Emergency Demand

**Project type:** Healthcare analytics research  
**Domain:** NHS operations · count-data modelling · regime analysis · time-series forecasting  
**Tools:** Statistical modelling · time-series diagnostics · out-of-sample evaluation

[← Portfolio index](../../PORTFOLIO_INDEX.md)

## Executive summary

This project studies monthly NHS emergency activity as a time series, with a focus on demand variability, disruption, and the practical limits of forecasting. The supplied results chapter describes **228 monthly observations from April 2007 to March 2026** for a series labelled `APC_Emergency`, with a pre-specified training period of April 2007–March 2023 (192 observations) and evaluation period of April 2023–March 2026 (36 observations).

The analysis compares Poisson and Negative Binomial count models, two-state Markov-switching specifications, and time-series forecasting benchmarks. The results chapter reports that the Poisson model is inadequate after trend, month effects and month length are accounted for; the Negative Binomial improves fit substantially. Regime structure is supported, but its interpretation depends on the specification. Importantly, the regime-informed forecast **did not improve accuracy** over the SARIMA benchmark on the pre-specified evaluation window.

Some findings above are transcribed from the supplied results chapter. The forecasting component has now been independently run against the uploaded 228-row aggregate extract; the Poisson/Negative Binomial and Markov-switching analyses have **not** yet been recreated because their original executable code was not included. The exact official source URL and reuse terms still need to be recorded.

## Research question

Can count-data and stochastic-regime methods better characterise monthly NHS emergency demand, and do regime signals improve forecasts beyond standard time-series benchmarks?

## Data and evaluation design

- **Series label:** `APC_Emergency` (as named in the supplied results chapter).
- **Reported coverage:** April 2007–March 2026; 228 consecutive monthly observations.
- **Reported split:** April 2007–March 2023 training; April 2023–March 2026 test.
- **Calendar adjustment:** the report describes an offset for days per month in count models and a days-adjusted series for forecasting.
- **Data provenance:** exact source table, download location, revision date and reuse licence remain to be recorded.

No patient-level data should be committed. Use only public, permitted aggregate data and retain source metadata.

## Reported findings

| Analysis | Reported result | Interpretation |
|---|---|---|
| Descriptive analysis | Mean monthly activity: 481,909; standard deviation: 51,693 | Long-run trend and disruption contribute to variability |
| Structural disruption | Minimum 330,244 in April 2020; maximum 575,744 in May 2024 | The series includes a sharp 2020 decline and later recovery |
| Count model comparison | Poisson Pearson dispersion reported as 1,330.6; Negative Binomial dispersion 0.98 | Poisson variance assumptions were not adequate for the specified conditional mean |
| Negative Binomial fit | Reported AIC 5,291.5 versus 299,295 for Poisson | Substantially better fit by the reported information criterion; serial correlation remains a limitation |
| Regime modelling | Two-state models preferred by AIC/BIC, but the state interpretation varies by specification | Regimes are plausible, but not uniquely identified |
| Forecast comparison | SARIMA(2,1,1)(0,1,1)[12] was competitive at short horizons; seasonal-naïve was preferable at 12 months | Model complexity should be judged by horizon-specific test performance |
| Regime-informed forecasts | No improvement on the pre-specified test window; slightly weaker performance on the shock-containing sensitivity window | Regime detection did not translate into forecast gains in these reported tests |

*All values above are transcribed from the supplied results chapter and are not independently verified in this repository. They should be rechecked against the source data and executable code before external use.*

## Methods

1. Validate date continuity, missing values, units and series definition.
2. Explore trend, seasonality, calendar effects and the 2020 disruption.
3. Compare Poisson and Negative Binomial models using diagnostics, not AIC alone.
4. Fit alternative two-state Markov-switching specifications and report sensitivity to variance assumptions.
5. Compare naïve, seasonal-naïve and SARIMA benchmarks on the same chronological holdout.
6. Assess errors by forecast horizon, residual autocorrelation and interval coverage.
7. Distinguish statistical coincidence from causal attribution; a detected regime does not establish why it occurred.

## Independently reproduced forecasting results

The uploaded extract was validated and the forecasting comparison was rerun with a 36-origin expanding-window, one-step-ahead evaluation. The script adjusts the SARIMA input for calendar-month length and converts predictions back to the original monthly activity scale.

| Model | MAE | RMSE | MAPE | MASE |
|---|---:|---:|---:|---:|
| SARIMA(2,1,1)(0,1,1)[12] | 10,343.8 | 12,873.0 | 1.88% | 0.412 |
| Seasonal naïve | 22,288.4 | 27,396.0 | 4.07% | 0.888 |
| Last-month naïve | 22,901.1 | 28,010.3 | 4.23% | 0.912 |

On this **one-step-ahead rolling-origin design**, SARIMA has the lowest error. This is not directly comparable with the chapter's separate 12-month-horizon result, where seasonal-naïve was reported as preferable. Forecast accuracy is horizon-dependent.

Data checks found 228 unique consecutive months, April 2007–March 2026, with no missing months or duplicate month labels. Mean monthly APC_Emergency activity is 481,909; the minimum is 330,244 (April 2020) and the maximum is 575,744 (May 2024).

Reproduce the forecasting results with `python reproduce_nhs_emergency.py` after placing the permitted source extract at `data/nhs_emergency_demand.csv`. Generated CSV tables and SVG charts are written to `outputs/`.

## Why this matters operationally

For healthcare planning, a forecast is useful only when its horizon, uncertainty and failure modes are clear. The reported results caution against assuming that a more elaborate regime model will outperform a well-specified baseline. Short-term planning and annual capacity decisions may require different benchmarks.

## Reproducibility status

**Status: forecasting component reproduced; count/regime analysis and source-provenance verification pending.**

The existing Python script is a starter forecasting workflow, not a recreation of every model in the results chapter. To reach a production-quality research repository, add:

- exact official data citation and licence;
- a clean data dictionary and extraction steps;
- versioned environment and runnable scripts/notebook;
- tests for date coverage, missingness and calendar adjustment;
- reproducible model tables and plots generated from code;
- a README update after outputs have been re-run and checked.

## Limitations and responsible use

- Aggregate monthly counts do not capture local variation, patient acuity, staffing, or hospital-level constraints.
- Serial correlation can violate independence assumptions in count regressions.
- Regime labels depend on model specification and should not be interpreted as causal labels.
- Forecasts support planning; they do not demonstrate that any staffing or policy intervention will improve patient outcomes.

See [the reproducible forecasting script](reproduce_nhs_emergency.py). The older generic workflow remains available as [forecast_template.py](forecast_template.py).
