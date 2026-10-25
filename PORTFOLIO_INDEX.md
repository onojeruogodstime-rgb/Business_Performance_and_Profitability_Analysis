# Godstime Onojeruo | Analytics Portfolio

**MSc Business Analytics** · **BSc Industrial Mathematics (First Class)** · **OND Statistics (Distinction)**

A focused portfolio of work across business performance, statistical forecasting, healthcare analytics, energy markets and systems thinking.

> **Portfolio integrity:** each project distinguishes reported academic findings from results independently reproduced in this repository. Starter templates and concepts are labelled honestly; they are not presented as deployed or validated solutions.

## Featured projects

### 1. Business Performance & Profitability Analysis
**Python · pandas · NumPy · KPI analysis · data visualisation**

Business-oriented analysis of revenue, profit, sales volume and product-category performance. The repository includes the original notebook, supporting dataset and portfolio visuals. The notebook and dataset should still be rerun together in a clean environment before the reported metrics are treated as independently validated.

[View project README](README.md)

### 2. Stochastic Analysis of NHS Emergency Demand
**Healthcare analytics · count-data modelling · stochastic regimes · forecasting**

Analysis chapter reports monthly emergency activity from April 2007 to March 2026, with Poisson versus Negative Binomial modelling, Markov-switching analysis and horizon-specific forecasting evaluation. A key reported result is that regime information did not improve forecasts on the pre-specified test window. The forecasting component has been independently reproduced on the uploaded aggregate extract with a 36-origin rolling evaluation; the count/regime models and exact official source provenance remain outstanding.

[View project](projects/nhs-emergency-demand/README.md)

### 3. Crude Oil Price Forecasting
**R · ARIMA · ETS · stationarity · forecast diagnostics**

Quarterly crude-oil price comparison based on a university analysis of daily prices aggregated from Q4 2009 to Q3 2024. Reported ARIMA and ETS errors are very close, which motivates a careful, baseline-driven evaluation rather than an overconfident winner claim. A provisional workbook reproduction and holdout comparison are now committed. Mixed date storage and low-coverage quarters mean the date convention and exact oil benchmark must be confirmed before the results are considered final.

[View project](projects/crude-oil-price-forecasting/README.md)

### 4. Smart-Home Energy Analysis
**Python · exploratory analysis · interpretable modelling**

A starter project for investigating energy-use patterns and building interpretable baselines. The dataset source, licence, analysis and findings must be completed before this can be described as an empirical case study.

[View project](projects/smart-home-energy-analysis/README.md)

### 5. The Domino Effect: NHS Systems Thinking
**Systems thinking · SSM/CATWOE · causal loops · Vensim PLE**

A systems framework linking waiting lists, workforce pressure, treatment throughput, policy response and delays. The project proposes candidate leverage points while clearly distinguishing a conceptual/simulation model from a calibrated policy model. Check academic publication permissions before sharing assessment artefacts.

[View project](projects/nhs-systems-thinking/README.md)

### 6. CareFlow AI — Care-Demand & Workforce Intelligence
**Concept · healthcare operations · demand planning**

A concept for using aggregate care-demand signals and workforce scenarios to support operational planning. It is not a deployed product, clinical decision tool or validated forecasting system.

[View concept](projects/careflow-ai/README.md)

## Engineering and evidence standards

- Cite the exact dataset, provider, series definition, licence and extraction date.
- Keep raw data out of the repository unless redistribution is explicitly permitted.
- Make data validation, transformations and evaluation windows reproducible.
- Compare forecasting models on chronological holdouts; do not rely on in-sample fit alone.
- Separate measured findings, report-transcribed findings, hypotheses and planned work.
- Record software versions and provide clear setup/run instructions.
- Never publish patient-level data, credentials, confidential employer material or restricted academic content.

## Current priority

The NHS forecasting pipeline now has reproduced metrics and data checks. The oil pipeline now has a provisional model comparison and explicit date-quality audit. Next, verify both datasets' official provenance, resolve the oil date convention/benchmark, recreate the NHS count and regime models from original code, and then rerun both projects in a clean environment.
