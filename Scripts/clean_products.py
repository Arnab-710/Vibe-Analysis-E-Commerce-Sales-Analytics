"""Build dim_product from products_raw.csv.

- Standardize category labels (trim + consistent casing).
- Recode inconsistent category/sub-category pairs to the majority parent
  for that sub_category so the dimension is internally consistent.
"""

from collections import Counter
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
RAW_PATH = BASE / "products_raw.csv"
OUT_PATH = BASE / "dim_product.csv"

CANONICAL_CATEGORIES = {
    "electronics": "Electronics",
    "office supplies": "Office Supplies",
    "furniture": "Furniture",
    "clothing": "Clothing",
    "home & kitchen": "Home & Kitchen",
}


def standardize_category(value: str) -> str:
    key = str(value).strip().lower()
    if key not in CANONICAL_CATEGORIES:
        raise ValueError(f"Unexpected category value: {value!r}")
    return CANONICAL_CATEGORIES[key]


raw = pd.read_csv(RAW_PATH, dtype={"product_id": "string"})
raw["category_standardized"] = raw["category"].map(standardize_category)

majority_parent = {}
for sub_category, group in raw.groupby("sub_category"):
    counts = Counter(group["category_standardized"])
    majority_parent[sub_category] = counts.most_common(1)[0][0]

raw["category"] = raw["sub_category"].map(majority_parent)
corrected = raw[raw["category"] != raw["category_standardized"]]

dim_product = raw[
    ["product_id", "product_name", "category", "sub_category", "cost", "selling_price"]
].sort_values("product_id").reset_index(drop=True)

dim_product.to_csv(OUT_PATH, index=False)

print(f"Raw rows: {len(raw)}")
print(f"Clean dim_product rows: {len(dim_product)}")
print("Canonical categories:", sorted(dim_product["category"].unique()))
print(f"Category/sub-category pairs recoded: {len(corrected)}")
for row in corrected.itertuples(index=False):
    print(
        f"  {row.product_id}: {row.sub_category} | "
        f"{row.category_standardized!r} -> {row.category}"
    )
print(f"Wrote {OUT_PATH}")
