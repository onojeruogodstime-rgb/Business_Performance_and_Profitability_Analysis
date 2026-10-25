"""Provisional reproduction of quarterly crude-oil forecasting from the supplied workbook.
Date warning: text dates are month-first; ambiguous native Excel dates are month/day-swapped.
This rule is inferred from adjacent records/report coverage and must be confirmed with the source provider.
"""
from pathlib import Path
from datetime import datetime
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing

ROOT=Path(__file__).resolve().parent
INPUT=ROOT/"data"/"BSOM096_CrudeOilPrice.xlsx"
OUT=ROOT/"outputs"

def parse_date(v):
    if pd.isna(v): return pd.NaT
    if isinstance(v,(pd.Timestamp,datetime)):
        if v.month<=12 and v.day<=12 and v.month!=v.day:
            return pd.Timestamp(year=v.year,month=v.day,day=v.month)
        return pd.Timestamp(v.date())
    return pd.to_datetime(str(v).strip(),format="%m/%d/%Y",errors="coerce")

def score(a,p,t):
    a,p,t=np.asarray(a,float),np.asarray(p,float),np.asarray(t,float)
    mae=np.mean(np.abs(a-p)); scale=np.mean(np.abs(t[1:]-t[:-1]))
    return {"MAE":mae,"RMSE":np.sqrt(np.mean((a-p)**2)),
            "MAPE_pct":np.mean(np.abs((a-p)/a))*100,"MASE":mae/scale if scale else np.nan}

def main():
    if not INPUT.exists(): raise FileNotFoundError(f"Place supplied workbook at {INPUT}; do not commit raw data without licence confirmation.")
    raw=pd.read_excel(INPUT,sheet_name="CrudeOilPrice02072024")
    if not {"Date","Crude Oil Price in USD"}.issubset(raw.columns): raise ValueError("Unexpected workbook columns.")
    native=raw["Date"].map(lambda x:isinstance(x,(pd.Timestamp,datetime)))
    raw["date"]=raw["Date"].map(parse_date)
    raw["price_usd"]=pd.to_numeric(raw["Crude Oil Price in USD"],errors="coerce")
    if raw["date"].isna().any(): raise ValueError("Unparseable dates; resolve before modelling.")
    missing_prices=int(raw["price_usd"].isna().sum())
    duplicate_rows=int(raw["date"].duplicated(keep=False).sum())
    daily=raw.dropna(subset=["price_usd"]).groupby("date",as_index=False)["price_usd"].mean().sort_values("date")
    q=daily.set_index("date")["price_usd"].resample("QE").agg(["mean","count"]).loc["2009-10-01":"2024-06-30"].dropna(subset=["mean"])
    q.index.name="quarter_end"; q["quarter"]=q.index.to_period("Q").astype(str); q["low_coverage_flag"]=q["count"]<40
    y=q["mean"].asfreq("QE")
    if y.isna().any(): raise ValueError("Missing quarter detected; no silent imputation.")
    train,test=y.iloc[:-12],y.iloc[-12:]
    pred={"Naive_last_value":np.repeat(train.iloc[-1],len(test))}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ar=ARIMA(train,order=(0,1,0),trend="t").fit()
        et=ExponentialSmoothing(train,trend="add",seasonal=None,initialization_method="estimated").fit(optimized=True)
    pred["ARIMA_0_1_0_drift"]=ar.forecast(len(test)).to_numpy()
    pred["ETS_additive_trend"]=et.forecast(len(test)).to_numpy()
    OUT.mkdir(parents=True,exist_ok=True)
    comparison=pd.DataFrame([{"model":n,**score(test.to_numpy(),p,train.to_numpy())} for n,p in pred.items()]).sort_values("RMSE")
    comparison.to_csv(OUT/"oil_model_comparison.csv",index=False)
    pd.DataFrame({"quarter_end":test.index,"actual_usd":test.to_numpy(),**pred}).to_csv(OUT/"oil_holdout_forecasts.csv",index=False)
    q.reset_index().to_csv(OUT/"oil_quarterly_prices.csv",index=False)
    pd.DataFrame([{"raw_rows":len(raw),"excel_native_date_cells":int(native.sum()),"text_date_cells":int((~native).sum()),
        "missing_prices":missing_prices,"duplicate_date_rows_aggregated":duplicate_rows,
        "unique_daily_dates_after_aggregation":len(daily),"quarters_used":len(q),"first_quarter":q.quarter.iloc[0],
        "last_quarter_used":q.quarter.iloc[-1],"quarters_with_fewer_than_40_daily_observations":int(q.low_coverage_flag.sum()),
        "partial_2024Q3_excluded":True,"date_policy":"month-first text; swap ambiguous native Excel dates",
        "status":"provisional; confirm date policy and oil benchmark/source"}]).to_csv(OUT/"oil_data_quality_audit.csv",index=False)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        final_ar=ARIMA(y,order=(0,1,0),trend="t").fit()
        final_et=ExponentialSmoothing(y,trend="add",seasonal=None,initialization_method="estimated").fit(optimized=True)
    idx=pd.date_range(y.index[-1]+pd.offsets.QuarterEnd(),periods=8,freq="QE")
    pd.DataFrame({"quarter_end":idx,"quarter":idx.to_period("Q").astype(str),
        "ARIMA_forecast_usd":final_ar.forecast(8).to_numpy(),"ETS_forecast_usd":final_et.forecast(8).to_numpy()}).to_csv(OUT/"oil_8_quarter_forecasts.csv",index=False)
    plt.figure(figsize=(10,5)); plt.plot(y.index,y.values,lw=1.4,label="Quarterly mean")
    plt.axvline(test.index[0],color="black",ls="--",label="Holdout start")
    plt.title("Quarterly crude-oil price (provisional date normalisation)"); plt.xlabel("Quarter")
    plt.ylabel("Price (USD; benchmark to confirm)"); plt.legend(); plt.tight_layout()
    plt.savefig(OUT/"oil_quarterly_series.svg"); plt.close()
    plt.figure(figsize=(10,5)); plt.plot(y.index,y.values,label="Observed quarterly mean",lw=1.4)
    for name,values in pred.items(): plt.plot(test.index,values,label=name.replace("_"," "),lw=1.2)
    plt.axvline(test.index[0],color="black",ls="--"); plt.title("Crude-oil prices: 12-quarter chronological holdout")
    plt.xlabel("Quarter"); plt.ylabel("Price (USD; benchmark to confirm)"); plt.legend(fontsize=8); plt.tight_layout()
    plt.savefig(OUT/"oil_holdout_comparison.svg"); plt.close()
    print("Provisional data audit"); print(pd.read_csv(OUT/"oil_data_quality_audit.csv").to_string(index=False))
    print("\n12-quarter holdout comparison"); print(comparison.round(3).to_string(index=False))

if __name__=="__main__": main()
