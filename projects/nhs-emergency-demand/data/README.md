# Data directory

Place a permitted monthly aggregate extract here as `nhs_emergency_demand.csv` with columns:

- `date`: one date per month, parseable by pandas
- `activity`: non-negative monthly activity count for one consistently defined series

The workflow expects one row per month and will stop if it detects missing months or duplicate monthly records. If the source has multiple rows per month, aggregate only after documenting the meaning of each row and the appropriate aggregation rule.

Document the exact official source/table, series label, geography, units, extraction and revision dates, source URL, and reuse terms. Do not place identifiable patient records or confidential operational data here. Raw data and generated outputs are excluded from version control by default.
