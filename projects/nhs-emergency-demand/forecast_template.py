"""Monthly NHS emergency-demand forecasting workflow.

This is an executable template, not a reproduction of the reported research chapter.
Input CSV: data/nhs_emergency_demand.csv
Required columns: date, activity
Use only aggregate data you are permitted to use; document the exact official source,
series definition, units, revision date and licence before publishing results.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX

DATA_PATH = Path("data/nhs_emergency_demand.csv")
DATE_COLUMN = "date"
TARGET_COLUMN = "activity"
TEST_PERIODS = 36  # aligns with the reported 36-month evaluation window; change only with justification
DAYS_PER_AVERAGE_MONTH = 30.4375


def score(actual: pd.Series, predicted: pd.Series, training: pd.Series) -> dict:
    """Calculate MAE, RMSE and MASE on the same chronological test window."""
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    mae = mean_absolute_error(actual, predicted)
    rmse = mean_squared_error(actual, predicted) ** 0.5
    seasonal_scale = np.mean(np.abs(training[12:].to_numpy() - training[:-12].to_numpy()))
    mase = mae / seasonal_scale if seasonal_scale > 0 else np.nan
    return {"MAE": mae, "RMSE": rmse, "MASE": mase}


def load_monthly_series(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Add a permitted aggregate dataset and document provenance."
        )
    data = pd.read_csv(path)
    missing_columns = {DATE_COLUMN, TARGET_COLUMN} - set(data.columns)
    if missing_columns:
        raise ValueError(f"Missing required column(s): {sorted(missing_columns)}")

    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN], errors="coerce")
    data[TARGET_COLUMN] = pd.to_numeric(data[TARGET_COLUMN], errors="coerce")
    data = data.dropna(subset=[DATE_COLUMN, TARGET_COLUMN]).sort_values(DATE_COLUMN)

    if data.empty:
        raise ValueError("No valid observations remain after date/value validation.")
    if data[DATE_COLUMN].duplicated().any():
        raise ValueError("Duplicate dates found. Resolve using the source definitions.")
    if (data[TARGET_COLUMN] < 0).any():
        raise ValueError("Negative activity counts found; check the source extract.")

    data["month"] = data[DATE_COLUMN].dt.to_period("M")
    if data["month"].duplicated().any():
        raise ValueError("More than one row per month. Aggregate according to the source definition.")
    data = data.set_index("month").sort_index()

    expected = pd.period_range(data.index.min(), data.index.max(), freq="M")
    if not data.index.equals(expected):
        missing = expected.difference(data.index)
        raise ValueError(f"Missing month(s): {list(map(str, missing[:12]))}. Do not silently fill gaps.")

    data.index = data.index.to_timestamp()
    data.index.name = "date"
    data["days_in_month"] = data.index.days_in_month
    data["activity_adjusted"] = (
        data[TARGET_COLUMN] / data["days_in_month"] * DAYS_PER_AVERAGE_MONTH
    )
    return data


def main() -> None:
    data = load_monthly_series(DATA_PATH)
    counts = data[TARGET_COLUMN].astype(float)
    adjusted = data["activity_adjusted"].astype(float)

    if len(data) <= TEST_PERIODS + 24:
        raise ValueError("Not enough observations for the selected training/test windows.")

    train_adjusted, test_adjusted = adjusted.iloc[:-TEST_PERIODS], adjusted.iloc[-TEST_PERIODS:]
    train_counts, test_counts = counts.iloc[:-TEST_PERIODS], counts.iloc[-TEST_PERIODS:]

    # Naive and seasonal-naive benchmarks are essential comparison points.
    naive_adjusted = pd.Series(train_adjusted.iloc[-1], index=test_adjusted.index)
    seasonal_naive_adjusted = pd.Series(
        [train_adjusted.iloc[-12 + (i % 12)] for i in range(TEST_PERIODS)],
        index=test_adjusted.index,
    )

    # SARIMA benchmark. This specification is a candidate, not guaranteed to be optimal.
    model = SARIMAX(
        train_adjusted,
        order=(2, 1, 1),
        seasonal_order=(0, 1, 1, 12),
        trend="n",
        enforce_stationarity=False,
        enforce_invertibility=False,
    )
    fitted = model.fit(disp=False)
    forecast_result = fitted.get_forecast(steps=TEST_PERIODS)
    sarima_adjusted = forecast_result.predicted_mean
    intervals_adjusted = forecast_result.conf_int(alpha=0.05)

    # Convert adjusted forecasts back to calendar-month activity counts.
    test_days = data["days_in_month"].iloc[-TEST_PERIODS:]
    factor = test_days / DAYS_PER_AVERAGE_MONTH
    predictions = {
        "Naive": naive_adjusted * factor,
        "Seasonal naive": seasonal_naive_adjusted * factor,
        "SARIMA": sarima_adjusted * factor,
    }

    # Metrics are computed on original calendar-month counts for comparability.
    metric_rows = []
    for name, prediction in predictions.items():
        values = score(test_counts, prediction, train_counts)
        metric_rows.append({"model": name, **values})
    metrics = pd.DataFrame(metric_rows).set_index("model")
    print("\nHoldout metrics (original calendar-month counts):")
    print(metrics.round(3))

    # Diagnostic output: autocorrelation remains important in healthcare time series.
    print("\nSARIMA model summary:")
    print(fitted.summary())

    output = pd.DataFrame(
        {
            "actual": test_counts,
            "naive_forecast": predictions["Naive"],
            "seasonal_naive_forecast": predictions["Seasonal naive"],
            "sarima_forecast": predictions["SARIMA"],
        }
    )
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    output.to_csv(output_dir / "holdout_forecasts.csv", index_label="date")
    metrics.to_csv(output_dir / "holdout_metrics.csv", index_label="model")

    ax = train_counts.plot(label="Training observations", figsize=(11, 6))
    test_counts.plot(ax=ax, label="Observed holdout")
    predictions["Seasonal naive"].plot(ax=ax, label="Seasonal-naive forecast")
    predictions["SARIMA"].plot(ax=ax, label="SARIMA forecast")
    ax.set_title("Monthly NHS emergency activity: holdout evaluation")
    ax.set_xlabel("Month")
    ax.set_ylabel("Activity (confirm selected series units)")
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "holdout_forecasts.png", dpi=160)
    plt.show()


if __name__ == "__main__":
    main()
