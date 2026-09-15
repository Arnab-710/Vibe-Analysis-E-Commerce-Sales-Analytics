"""Build dim_date from valid order_date values in fact_sales.csv."""

from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
FACT_PATH = BASE / "fact_sales.csv"
OUT_PATH = BASE / "dim_date.csv"

fact = pd.read_csv(FACT_PATH, usecols=["order_date"])
dates = pd.to_datetime(fact["order_date"], errors="coerce").dropna().drop_duplicates().sort_values()

dim_date = pd.DataFrame({"date": dates.dt.strftime("%Y-%m-%d")})
dim_date["date_key"] = dates.dt.strftime("%Y%m%d").astype(int)
dim_date["day"] = dates.dt.day.astype(int)
dim_date["month"] = dates.dt.month.astype(int)
dim_date["month_name"] = dates.dt.strftime("%B")
dim_date["quarter"] = dates.dt.quarter.astype(int)
dim_date["year"] = dates.dt.year.astype(int)

dim_date = dim_date[
    ["date_key", "date", "day", "month", "month_name", "quarter", "year"]
]

dim_date.to_csv(OUT_PATH, index=False)

print(f"Valid unique dates: {len(dim_date)}")
print(f"date min: {dim_date['date'].min()}")
print(f"date max: {dim_date['date'].max()}")
print(f"years: {sorted(dim_date['year'].unique().tolist())}")
print(f"Wrote {OUT_PATH}")
