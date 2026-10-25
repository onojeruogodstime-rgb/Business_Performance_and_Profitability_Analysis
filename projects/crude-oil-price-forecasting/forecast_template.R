# Crude oil price forecasting starter template
# Prepare data/crude_oil_prices.csv with columns date,price.
# Cite the source, benchmark, units, frequency and licence before publishing results.

required <- c("forecast", "tseries", "ggplot2", "readr")
missing <- required[!vapply(required, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing) > 0) stop("Install packages: ", paste(missing, collapse = ", "))
library(forecast)
library(tseries)
library(ggplot2)
library(readr)

file_path <- "data/crude_oil_prices.csv"
if (!file.exists(file_path)) stop("Add a permitted source dataset and document provenance.")
raw <- read_csv(file_path, show_col_types = FALSE)
if (!all(c("date", "price") %in% names(raw))) stop("Expected columns date and price.")
raw$date <- as.Date(raw$date)
raw <- raw[order(raw$date), ]
raw <- raw[complete.cases(raw[, c("date", "price")]), ]
if (anyDuplicated(raw$date)) stop("Resolve duplicate dates before modelling.")

# Confirm the actual frequency first. This example assumes quarterly observations.
price_ts <- ts(raw$price, frequency = 4)
plot(price_ts, main = "Crude oil price series", ylab = "Price (confirm units)")
print(adf.test(price_ts))
print(ndiffs(price_ts))

n_test <- max(4, floor(length(price_ts) * 0.2))
if (length(price_ts) <= n_test + 8) stop("Insufficient observations for this split.")
train <- head(price_ts, length(price_ts) - n_test)
test <- tail(price_ts, n_test)
fit_arima <- auto.arima(train, seasonal = TRUE, stepwise = FALSE, approximation = FALSE)
fit_ets <- ets(train)
fc_arima <- forecast(fit_arima, h = n_test)
fc_ets <- forecast(fit_ets, h = n_test)
print(accuracy(fc_arima, test))
print(accuracy(fc_ets, test))
checkresiduals(fit_arima)
checkresiduals(fit_ets)

# Refit only after model selection and evaluation. Intervals do not capture every market shock.
final_fit <- auto.arima(price_ts, seasonal = TRUE)
future <- forecast(final_fit, h = 8, level = c(80, 95))
autoplot(future) +
  labs(title = "Crude oil price forecast — template",
       x = "Time", y = "Price (confirm units)") +
  theme_minimal()
