"""Build fact_sales from orders_raw.csv.

- Remove exact duplicate transactions.
- Normalize valid order_date values to YYYY-MM-DD; blank and flag
  unparseable dates (the literal value not_a_date).
- Drop rows with a blank customer_id or product_id.
- Add is_return for negative quantity.
"""

from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
ORDERS_PATH = BASE / "orders_raw.csv"
OUT_PATH = BASE / "fact_sales.csv"

orders = pd.read_csv(
    ORDERS_PATH,
    dtype={
        "order_id": "string",
        "customer_id": "string",
        "product_id": "string",
        "region_id": "string",
    },
)
raw_rows = len(orders)

for col in ("customer_id", "product_id", "region_id"):
    orders[col] = orders[col].str.strip().mask(lambda s: s.eq(""), pd.NA)

dup_extra = int(orders.duplicated(keep="first").sum())
orders = orders.drop_duplicates(keep="first").reset_index(drop=True)

parsed_dates = pd.to_datetime(orders["order_date"], errors="coerce")
orders["is_invalid_date"] = parsed_dates.isna().astype(int)
orders["order_date"] = parsed_dates.dt.strftime("%Y-%m-%d")
orders.loc[parsed_dates.isna(), "order_date"] = pd.NA

missing_id = orders["customer_id"].isna() | orders["product_id"].isna()
dropped_missing_ids = int(missing_id.sum())
orders = orders.loc[~missing_id].reset_index(drop=True)

orders["quantity"] = pd.to_numeric(orders["quantity"], errors="coerce")
orders["is_return"] = (orders["quantity"] < 0).astype(int)

fact_sales = orders[
    [
        "order_id",
        "order_date",
        "customer_id",
        "product_id",
        "region_id",
        "quantity",
        "discount",
        "sales_amount",
        "cost_amount",
        "profit",
        "is_return",
        "is_invalid_date",
    ]
]

fact_sales.to_csv(OUT_PATH, index=False)

valid_dates = fact_sales["order_date"].dropna()
print(f"Raw rows: {raw_rows}")
print(f"Exact duplicate extra rows removed: {dup_extra}")
print(f"Clean fact_sales rows: {len(fact_sales)}")
print(f"Unique order_id: {fact_sales['order_id'].nunique()}")
print(f"Rows dropped for blank customer_id or product_id: {dropped_missing_ids}")
print(f"is_return=1: {int(fact_sales['is_return'].sum())}")
print(f"is_invalid_date=1: {int(fact_sales['is_invalid_date'].sum())}")
print(f"order_date min: {valid_dates.min()}")
print(f"order_date max: {valid_dates.max()}")
print(f"Wrote {OUT_PATH}")
