"""Reproduce monthly NHS emergency-activity forecasts from the supplied aggregate HES extract."""
from pathlib import Path
from datetime import datetime
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "data" / "nhs_emergency_demand.csv"
OUT = ROOT / "outputs"
MONTHS = dict(zip(["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"], range(1,13)))
DAYS = 30.4375

def parse_month(value):
    s = str(value).strip().upper()
    if len(s) != 5 or s[:3] not in MONTHS or not s[3:].isdigit():
        raise ValueError(f"Unexpected month label: {value!r}")
    return pd.Timestamp(2000 + int(s[3:]), MONTHS[s[:3]], 1)

def metrics(actual, predicted, train):
    a, p, t = np.asarray(actual, float), np.asarray(predicted, float), np.asarray(train, float)
    mae = np.mean(np.abs(a-p))
    scale = np.mean(np.abs(t[12:]-t[:-12]))
    return {"MAE": mae, "RMSE": np.sqrt(np.mean((a-p)**2)),
            "MAPE_pct": np.mean(np.abs((a-p)/a))*100, "MASE": mae/scale if scale else np.nan}

def main():
    if not INPUT.exists():
        raise FileNotFoundError(f"Add permitted aggregate input at {INPUT}; do not commit patient-identifiable data.")
    raw = pd.read_csv(INPUT)
    required = {"CALENDAR_MONTH_END_DATE", "APC_Emergency"}
    if not required.issubset(raw.columns):
        raise ValueError(f"Expected columns: {sorted(required)}")
    raw["date"] = raw["CALENDAR_MONTH_END_DATE"].map(parse_month)
    raw["APC_Emergency"] = pd.to_numeric(raw["APC_Emergency"], errors="coerce")
    if raw["date"].duplicated().any() or raw["APC_Emergency"].isna().any():
        raise ValueError("Duplicate month labels or missing/non-numeric APC_Emergency values found.")
    y = raw.sort_values("date").set_index("date")["APC_Emergency"].astype(float).asfreq("MS")
    if y.isna().any():
        raise ValueError("Missing calendar months detected; resolve rather than silently imputing.")
    train_end = pd.Timestamp("2023-03-01")
    train, test = y.loc[:train_end], y.loc[train_end + pd.offsets.MonthBegin(1):]
    if len(train) != 192 or len(test) != 36:
        raise ValueError(f"Expected 192 training and 36 test months; got {len(train)} and {len(test)}.")
    preds = {"Naive_last_month": [], "Seasonal_naive": [], "SARIMA_2_1_1_0_1_1_12": []}
    dates, actuals = [], []
    for date in test.index:
        hist = y.loc[:date-pd.offsets.MonthBegin(1)]
        dates.append(date); actuals.append(float(y.loc[date]))
        preds["Naive_last_month"].append(float(hist.iloc[-1]))
        prev_date = date - pd.DateOffset(years=1)
        adj = float(y.loc[prev_date]) / prev_date.days_in_month * DAYS
        preds["Seasonal_naive"].append(adj * date.days_in_month / DAYS)
        adjusted = hist / hist.index.days_in_month * DAYS
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fit = SARIMAX(adjusted, order=(2,1,1), seasonal_order=(0,1,1,12),
                          trend="n", enforce_stationarity=False, enforce_invertibility=False).fit(disp=False, maxiter=200)
            one_step = float(fit.forecast(1).iloc[0])
        preds["SARIMA_2_1_1_0_1_1_12"].append(one_step * date.days_in_month / DAYS)
    OUT.mkdir(parents=True, exist_ok=True)
    forecasts = pd.DataFrame({"date": dates, "actual": actuals, **preds})
    forecasts.to_csv(OUT/"nhs_emergency_rolling_forecasts.csv", index=False)
    comparison = pd.DataFrame([{"model": name, **metrics(actuals, values, train.values)}
                               for name, values in preds.items()]).sort_values("RMSE")
    comparison.to_csv(OUT/"nhs_emergency_model_comparison.csv", index=False)
    summary = pd.DataFrame([{
        "observations": len(y), "start_month": y.index.min().strftime("%Y-%m"),
        "end_month": y.index.max().strftime("%Y-%m"), "missing_months": int(y.isna().sum()),
        "duplicate_month_labels": int(raw["CALENDAR_MONTH_END_DATE"].duplicated().sum()),
        "mean_monthly_emergency_activity": float(y.mean()), "minimum": int(y.min()),
        "minimum_month": y.idxmin().strftime("%Y-%m"), "maximum": int(y.max()),
        "maximum_month": y.idxmax().strftime("%Y-%m"), "train_start": train.index.min().strftime("%Y-%m"),
        "train_end": train.index.max().strftime("%Y-%m"), "test_start": test.index.min().strftime("%Y-%m"),
        "test_end": test.index.max().strftime("%Y-%m"),
        "evaluation": "36 expanding-window one-step-ahead forecasts",
        "calendar_adjustment": "count / days in month * 30.4375 for SARIMA"}])
    summary.to_csv(OUT/"nhs_emergency_data_quality_summary.csv", index=False)
    plt.figure(figsize=(10,5)); plt.plot(y.index,y.values,lw=1.4)
    plt.axvline(train_end,color="black",ls="--",label="Train/test boundary")
    plt.title("Monthly NHS emergency activity (APC_Emergency)")
    plt.xlabel("Month"); plt.ylabel("Recorded activity"); plt.legend(); plt.tight_layout()
    plt.savefig(OUT/"nhs_emergency_time_series.svg"); plt.close()
    plt.figure(figsize=(10,5)); plt.plot(y.index,y.values,label="Observed",lw=1.3)
    for name, values in preds.items(): plt.plot(dates,values,label=name.replace("_"," "),lw=1.2)
    plt.axvline(test.index[0],color="black",ls="--"); plt.title("NHS emergency activity: rolling one-step forecasts")
    plt.xlabel("Month"); plt.ylabel("Recorded activity"); plt.legend(fontsize=8); plt.tight_layout()
    plt.savefig(OUT/"nhs_emergency_forecast_comparison.svg"); plt.close()
    print(summary.to_string(index=False)); print(comparison.round(3).to_string(index=False))

if __name__ == "__main__":
    main()
