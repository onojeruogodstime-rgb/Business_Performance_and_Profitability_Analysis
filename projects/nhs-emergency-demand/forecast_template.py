"""Starter template for aggregate NHS emergency-demand forecasting.

Not a fitted model. Document the permitted data source, then update column names
and the test horizon to match the chosen series before reporting any results.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.holtwinters import ExponentialSmoothing

DATA_PATH = Path("data/nhs_emergency_demand.csv")
DATE_COLUMN = "date"
TARGET_COLUMN = "activity"
TEST_PERIODS = 12


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"{DATA_PATH} not found. Add a permitted aggregate dataset and cite it."
        )
    data = pd.read_csv(DATA_PATH, parse_dates=[DATE_COLUMN])
    if DATE_COLUMN not in data or TARGET_COLUMN not in data:
        raise ValueError(f"Expected {DATE_COLUMN!r} and {TARGET_COLUMN!r} columns.")
    data = data[[DATE_COLUMN, TARGET_COLUMN]].dropna().sort_values(DATE_COLUMN)
    if data[DATE_COLUMN].duplicated().any():
        raise ValueError("Resolve duplicate dates using the source definitions.")
    series = data.set_index(DATE_COLUMN)[TARGET_COLUMN].astype(float)
    if len(series) <= TEST_PERIODS:
        raise ValueError("Not enough observations for the chosen test horizon.")
    train, test = series.iloc[:-TEST_PERIODS], series.iloc[-TEST_PERIODS:]
    baseline = pd.Series(train.iloc[-1], index=test.index)
    model = ExponentialSmoothing(
        train, trend="add", seasonal=None, initialization_method="estimated"
    ).fit()
    forecast = model.forecast(len(test))
    for label, prediction in [("Naive baseline", baseline), ("Exponential smoothing", forecast)]:
        print(label, "MAE:", round(mean_absolute_error(test, prediction), 3),
              "RMSE:", round(mean_squared_error(test, prediction) ** 0.5, 3))
    ax = train.plot(label="Training data", figsize=(10, 5))
    test.plot(ax=ax, label="Observed test period")
    forecast.plot(ax=ax, label="Forecast")
    ax.set_title("NHS emergency-demand forecast — template output")
    ax.set_ylabel("Activity (confirm selected series units)")
    ax.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
