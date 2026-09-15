"""Build dim_region from regions_raw.csv (no recoding required)."""

from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
RAW_PATH = BASE / "regions_raw.csv"
OUT_PATH = BASE / "dim_region.csv"

dim_region = (
    pd.read_csv(RAW_PATH, dtype={"region_id": "string"})
    .drop_duplicates(subset=["region_id"], keep="first")
    .sort_values("region_id")
    .reset_index(drop=True)
)

if dim_region["region_id"].isna().any() or (dim_region["region_id"].str.strip() == "").any():
    raise ValueError("Blank region_id values found")

dim_region.to_csv(OUT_PATH, index=False)
print(f"dim_region rows: {len(dim_region)}")
print(f"Unique region_id: {dim_region['region_id'].nunique()}")
print(f"Wrote {OUT_PATH}")
