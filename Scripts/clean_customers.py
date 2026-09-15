"""Build dim_customer from customers_raw.csv: one row per customer_id."""

from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
RAW_PATH = BASE / "customers_raw.csv"
OUT_PATH = BASE / "dim_customer.csv"

raw = pd.read_csv(RAW_PATH, dtype={"customer_id": "string"})

duplicate_mask = raw.duplicated(subset=["customer_id"], keep=False)
duplicate_rows = raw.loc[duplicate_mask].copy()
duplicate_ids = (
    duplicate_rows["customer_id"].drop_duplicates().sort_values().tolist()
)

dim_customer = (
    raw.drop_duplicates(subset=["customer_id"], keep="first")
    .sort_values("customer_id")
    .reset_index(drop=True)
)

dim_customer.to_csv(OUT_PATH, index=False)

print(f"Raw rows: {len(raw)}")
print(f"Duplicate customer_id values: {len(duplicate_ids)}")
print("Duplicate customer IDs:")
for cid in duplicate_ids:
    count = int((raw["customer_id"] == cid).sum())
    print(f"  {cid} (appears {count} times)")
print(f"Clean dim_customer rows: {len(dim_customer)}")
print(f"Unique customer_id in dim_customer: {dim_customer['customer_id'].nunique()}")
print(f"Wrote {OUT_PATH}")
