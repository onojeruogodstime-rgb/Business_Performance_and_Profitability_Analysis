# Data directory

Place a permitted source file here as `crude_oil_prices_daily.csv` with columns:

- `date`: observation date in an unambiguous format such as `YYYY-MM-DD`
- `price`: numeric crude-oil price

Before modelling, document the provider, exact benchmark/series, currency and units, source URL, access date, licence, date range, and how missing observations are treated. The R script aggregates observed daily prices to quarterly arithmetic means and intentionally does not forward-fill weekends or market holidays.

Do not commit raw data unless its licence clearly permits redistribution. The `.gitignore` excludes common data files by default.


## Supplied workbook and date quality

The locally supplied workbook uses the sheet `CrudeOilPrice02072024` with columns `Date` and `Crude Oil Price in USD`. Its date column mixes text dates and native Excel date cells. The workbook reproduction script uses a provisional normalisation rule; confirm it against the original provider before treating results as final. Keep the raw workbook local unless redistribution is explicitly permitted.
