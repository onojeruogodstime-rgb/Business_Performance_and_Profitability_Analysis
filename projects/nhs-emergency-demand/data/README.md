# Data directory

Place the permitted aggregate extract as `nhs_emergency_demand.csv`. The reproducible script expects the original extract columns `CALENDAR_MONTH_END_DATE` (labels such as `MAR26`) and `APC_Emergency`.

The uploaded extract used for the current run contained 228 unique consecutive monthly records from April 2007 through March 2026. This repository does not include the raw file because its exact official source URL and reuse terms still need to be recorded.

Before public release, document the official source/table, series definition, geography, units, extraction/revision date, source URL, and licence. Do not add patient-identifiable records or confidential operational data.

## Likely official source and interpretation

The extract appears consistent with NHS England's [Provisional Monthly Hospital Episode Statistics (HES) summary data catalogue](https://www.data.gov.uk/dataset/c914f943-98d1-4dee-aba5-c40a7d08eefa/provisional-monthly-hospital-episode-statistics-for-admitted-patient-care-outpatient-and-accident-and-emergency), which describes monthly summary CSVs from April 2007 and lists the Open Government Licence. Verify the exact file version and extraction date before publishing.

`APC_Emergency` belongs to Admitted Patient Care (APC): interpret it as emergency admissions activity, not total A&E attendances. NHS England states that the historical HES A&E component was replaced by the Emergency Care Data Set from April 2020. Avoid describing this APC variable as a continuous A&E attendance series.
