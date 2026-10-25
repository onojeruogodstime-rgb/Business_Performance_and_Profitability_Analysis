"""Starter template for smart-home energy analysis.
Document the dataset source and update TARGET to the real target field.
This template is not a completed empirical analysis.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

DATA_PATH = Path("data/smart_home_energy.csv")
TARGET = "energy_consumption"


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError("Add a permitted dataset and cite its source.")
    data = pd.read_csv(DATA_PATH)
    if TARGET not in data.columns:
        raise ValueError(f"Target column {TARGET!r} not found; inspect the data dictionary.")
    data = data.dropna(subset=[TARGET])
    y = pd.to_numeric(data[TARGET], errors="coerce")
    X = data.drop(columns=[TARGET]).select_dtypes(include="number")
    valid = y.notna()
    X, y = X.loc[valid], y.loc[valid]
    if X.empty or len(X) < 20:
        raise ValueError("Not enough usable numeric observations.")
    # Replace random splitting with chronological/group-based splitting when appropriate.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    models = {
        "Mean baseline": make_pipeline(SimpleImputer(strategy="median"),
                                       DummyRegressor(strategy="mean")),
        "Ridge regression": make_pipeline(SimpleImputer(strategy="median"),
                                           StandardScaler(), Ridge(alpha=1.0)),
    }
    rows = []
    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        rows.append({"model": name, "MAE": mean_absolute_error(y_test, pred),
                     "RMSE": mean_squared_error(y_test, pred) ** 0.5})
    print(pd.DataFrame(rows).to_string(index=False))
    y.hist(bins=30, figsize=(8, 5))
    plt.title("Smart-home energy target distribution")
    plt.xlabel(f"{TARGET} (confirm units)")
    plt.ylabel("Observations")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
