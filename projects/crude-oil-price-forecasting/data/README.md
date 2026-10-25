# Data directory

Place a permitted source file here as `crude_oil_prices_daily.csv` with columns:

- `date`: observation date in an unambiguous format such as `YYYY-MM-DD`
- `price`: numeric crude-oil price

Before modelling, document the provider, exact benchmark/series, currency and units, source URL, access date, licence, date range, and how missing observations are treated. The R script aggregates observed daily prices to quarterly arithmetic means and intentionally does not forward-fill weekends or market holidays.

Do not commit raw data unless its licence clearly permits redistribution. The `.gitignore` excludes common data files by default.
