# Quarterly crude-oil forecasting: ARIMA versus ETS
#
# Input: data/crude_oil_prices_daily.csv with columns date,price.
# Confirm source, benchmark, units, licence and missing-data policy before use.
# The source academic report's results are not reproduced automatically by this script.

required <- c("forecast", "tseries", "ggplot2", "readr", "dplyr", "zoo")
missing <- required[!vapply(required, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing) > 0) stop("Install packages: ", paste(missing, collapse = ", "))

library(forecast)
library(tseries)
library(ggplot2)
library(readr)
library(dplyr)
library(zoo)

input_file <- "data/crude_oil_prices_daily.csv"
if (!file.exists(input_file)) {
  stop("Missing ", input_file,
       ". Add only data you are permitted to redistribute and document its provenance.")
}

daily <- read_csv(input_file, show_col_types = FALSE)
if (!all(c("date", "price") %in% names(daily))) {
  stop("Expected columns named date and price.")
}

daily <- daily |>
  mutate(date = as.Date(date), price = suppressWarnings(as.numeric(price))) |>
  filter(!is.na(date), !is.na(price)) |>
  arrange(date)

if (nrow(daily) == 0) stop("No valid observations after date/price validation.")
if (anyDuplicated(daily$date)) stop("Duplicate dates found; resolve them using source documentation.")
if (any(daily$price <= 0, na.rm = TRUE)) {
  warning("Non-positive prices found; check the benchmark and source before proceeding.")
}

# Aggregate observed daily prices to arithmetic quarterly means.
# Do not forward-fill weekends or market holidays unless the source methodology justifies it.
quarterly <- daily |>
  mutate(quarter = as.yearqtr(date)) |>
  group_by(quarter) |>
  summarise(price = mean(price, na.rm = TRUE), daily_observations = n(), .groups = "drop") |>
  arrange(quarter)

if (nrow(quarterly) < 24) stop("Too few quarterly observations for a useful comparison.")
if (anyDuplicated(quarterly$quarter)) stop("Quarterly aggregation produced duplicate quarters.")

# Check for missing quarters. Do not silently impute them.
all_quarters <- seq(min(quarterly$quarter), max(quarterly$quarter), by = 0.25)
missing_quarters <- setdiff(as.character(all_quarters), as.character(quarterly$quarter))
if (length(missing_quarters) > 0) {
  stop("Missing quarter(s) detected: ", paste(missing_quarters, collapse = ", "),
       ". Resolve/document gaps before fitting models.")
}

start_year <- as.integer(format(min(quarterly$quarter), "%Y"))
start_quarter <- as.integer(format(min(quarterly$quarter), "%q"))
price_ts <- ts(quarterly$price, start = c(start_year, start_quarter), frequency = 4)

print(summary(quarterly$price))
print(adf.test(price_ts))
autoplot(price_ts) +
  labs(title = "Quarterly crude-oil price", x = "Quarter",
       y = "Price (confirm currency and units)") +
  theme_minimal()

# Chronological holdout: final 20% of quarters, with a minimum of four quarters.
n_test <- max(4, floor(length(price_ts) * 0.20))
if (length(price_ts) <= n_test + 12) stop("Insufficient training observations.")
train <- head(price_ts, length(price_ts) - n_test)
test <- tail(price_ts, n_test)

# Benchmarks and candidate methods are fit on training observations only.
arima_fit <- auto.arima(train, seasonal = TRUE, stepwise = FALSE, approximation = FALSE)
ets_fit <- ets(train)

fc_naive <- naive(train, h = n_test)
fc_arima <- forecast(arima_fit, h = n_test, level = c(80, 95))
fc_ets <- forecast(ets_fit, h = n_test, level = c(80, 95))

metrics <- function(actual, predicted) {
  c(MAE = mean(abs(actual - predicted)),
    RMSE = sqrt(mean((actual - predicted)^2)),
    MAPE_percent = mean(abs((actual - predicted) / actual)) * 100)
}

comparison <- rbind(
  Naive = metrics(as.numeric(test), as.numeric(fc_naive$mean)),
  ARIMA = metrics(as.numeric(test), as.numeric(fc_arima$mean)),
  ETS = metrics(as.numeric(test), as.numeric(fc_ets$mean))
)
print(round(comparison, 4))

# Plot test-period forecasts against observed values.
test_plot <- data.frame(
  quarter = as.character(time(test)),
  actual = as.numeric(test),
  naive = as.numeric(fc_naive$mean),
  arima = as.numeric(fc_arima$mean),
  ets = as.numeric(fc_ets$mean)
)
print(test_plot)

# Diagnostics must be reviewed, not merely generated.
checkresiduals(arima_fit)
checkresiduals(ets_fit)

# Final forecasts are fitted to the full series only after the holdout comparison.
final_arima <- auto.arima(price_ts, seasonal = TRUE, stepwise = FALSE, approximation = FALSE)
final_ets <- ets(price_ts)
horizon <- 8
future_arima <- forecast(final_arima, h = horizon, level = c(80, 95))
future_ets <- forecast(final_ets, h = horizon, level = c(80, 95))

autoplot(future_arima) +
  labs(title = "ARIMA forecast — quarterly crude-oil prices",
       x = "Quarter", y = "Price (confirm currency and units)") +
  theme_minimal()
autoplot(future_ets) +
  labs(title = "ETS forecast — quarterly crude-oil prices",
       x = "Quarter", y = "Price (confirm currency and units)") +
  theme_minimal()

# Save outputs for review and versioning; do not publish until source provenance is documented.
dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
write.csv(as.data.frame(comparison), "outputs/holdout_model_comparison.csv", row.names = TRUE)
write.csv(quarterly, "outputs/quarterly_prices_used.csv", row.names = FALSE)
