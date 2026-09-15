# Vibe Analysis — E-Commerce Sales Analytics

An end-to-end data analytics portfolio project that takes messy e-commerce source data through profiling, cleaning, dimensional modeling, and interactive dashboard delivery.

**Live deliverable:** open [`dashboard/vibe_analysis_dashboard.html`](dashboard/vibe_analysis_dashboard.html) in any browser — no server required.

Built end-to-end using **Cursor AI** (Agent mode) for data profiling, ETL scripting, dimensional modeling, and dashboard generation.

---

## Overview

A fictional e-commerce company needs to understand revenue, profit, and performance across products, regions, and time. This project demonstrates the full analyst workflow:

1. **Profile** raw CSV exports and document data quality issues
2. **Clean** and standardize data into a star schema
3. **Analyze** business questions with SQL-ready dimensional tables
4. **Visualize** findings in an interactive HTML dashboard

| Metric | Value |
|--------|------:|
| Total revenue | $29.36M |
| Total profit | $6.73M |
| Profit margin | 22.9% |
| Orders | 24,895 |
| Customers | 2,000 |
| Products | 100 |
| Regions | 5 |
| Date range | Jan 2024 – Dec 2025 |

---

## Data Model

The analytical layer follows a classic **star schema** with one fact table and four dimension tables.

```
                    dim_customer
                         │
                         │
    dim_product ─── fact_sales ─── dim_region
                         │
                         │
                     dim_date
```

### Tables

| Table | Rows | Description |
|-------|-----:|-------------|
| `fact_sales` | 24,895 | Order-level transactions: quantity, discount, sales, cost, profit |
| `dim_customer` | 2,000 | Customer demographics and signup date |
| `dim_product` | 100 | Product catalog with category and sub-category |
| `dim_region` | 20 | State, city, and sales region mapping |
| `dim_date` | 731 | Calendar dimension (2024-01-01 to 2025-12-31) |

### Join keys

| From | To | Key |
|------|----|-----|
| `fact_sales` | `dim_customer` | `customer_id` |
| `fact_sales` | `dim_product` | `product_id` |
| `fact_sales` | `dim_region` | `region_id` |
| `fact_sales` | `dim_date` | `order_date` → `date` |

---

## Raw Data & Quality Issues

Four source files simulate real-world exports with typical problems.

| File | Rows | Issues found |
|------|-----:|--------------|
| `orders_raw.csv` | 25,050 | 50 exact duplicates; 60 blank `customer_id`; 35 blank `product_id`; 10 unparseable dates (`not_a_date`); 15 negative-quantity returns |
| `customers_raw.csv` | 2,010 | 10 duplicate `customer_id` rows |
| `products_raw.csv` | 100 | Inconsistent category casing; trailing spaces; 12 category/sub-category mismatches |
| `regions_raw.csv` | 20 | Clean (placeholder city names only) |

---

## Data Cleaning

Each dimension and the fact table are built by a dedicated Python script. Raw files are left untouched.

| Script | Output | Transformations |
|--------|--------|-----------------|
| `clean_customers.py` | `dim_customer.csv` | Deduplicate on `customer_id` (keep first) |
| `clean_products.py` | `dim_product.csv` | Standardize category labels; recode mismatched category/sub-category pairs |
| `clean_orders.py` | `fact_sales.csv` | Remove duplicates; drop rows with missing IDs; normalize dates; flag returns and invalid dates |
| `clean_regions.py` | `dim_region.csv` | Pass-through (no changes needed) |
| `clean_dates.py` | `dim_date.csv` | Generate one row per calendar day in range |

### `fact_sales` columns

| Column | Description |
|--------|-------------|
| `order_id` | Unique order identifier |
| `order_date` | Normalized date (`YYYY-MM-DD`) or blank if invalid |
| `customer_id` | Foreign key to `dim_customer` |
| `product_id` | Foreign key to `dim_product` |
| `region_id` | Foreign key to `dim_region` |
| `quantity` | Units sold (negative = return) |
| `discount` | Discount applied |
| `sales_amount` | Revenue for the line item |
| `cost_amount` | Cost of goods |
| `profit` | `sales_amount − cost_amount` |
| `is_return` | `1` when `quantity < 0` |
| `is_invalid_date` | `1` when `order_date` could not be parsed |

**Cleaning result:** 25,050 raw orders → **24,895** clean fact rows (155 rows removed or flagged).

---

## Key Business Insights

Analysis is performed on `fact_sales` joined to `dim_product` and `dim_region`.

### Top 10 products by revenue

| Product | Revenue |
|---------|--------:|
| Kids Product 98 | $823K |
| Tables Product 97 | $731K |
| Storage Product 83 | $701K |
| Appliances Product 99 | $691K |
| Appliances Product 50 | $663K |
| Cookware Product 59 | $652K |
| Kids Product 80 | $642K |
| Women Product 67 | $632K |
| Chairs Product 12 | $572K |
| Paper Product 94 | $521K |

### Profit by region

| Region | Profit |
|--------|-------:|
| North | $1.71M |
| East | $1.69M |
| South | $1.69M |
| West | $1.32M |
| Central | $315K |

### Other findings

- **Monthly trend:** Revenue and profit tracked from Jan 2024 through Dec 2025; weakest month Feb 2025, strongest Dec 2025.
- **High revenue, low margin:** Cookware Product 89 (9.6% margin) and Mobiles Product 66 (12.1% margin) generate strong sales but thin margins — candidates for pricing or cost review.

---

## Interactive Dashboard

The dashboard is a self-contained HTML file powered by Chart.js. Data is embedded at build time from the star schema CSVs.

### Features

- **KPI cards** — Revenue, Profit, Orders, Customers
- **Monthly sales trend** — Revenue and profit over time
- **Revenue by category** — Donut chart (Clothing, Home & Kitchen, Furniture, Office Supplies, Electronics)
- **Profit by region** — Bar chart across five regions
- **Top 10 products** — Horizontal bar chart by revenue
- **Filters** — Year, Region, and Category update all visuals instantly

### View the dashboard

Double-click `dashboard/vibe_analysis_dashboard.html` or open it in Chrome, Edge, or Firefox.

### Rebuild after data changes

```
pip install pandas
python build_dashboard.py
```

This reads `fact_sales.csv`, `dim_product.csv`, and `dim_region.csv`, embeds 24,895 valid-dated rows as JSON, and writes `vibe_analysis_dashboard.html` from `dashboard_template.html`.

---

## Project Structure

```
Vibe-Analysis/
├── README.md
├── LICENSE
│
├── data/
│   ├── data_raw/
│   │   ├── orders_raw.csv
│   │   ├── customers_raw.csv
│   │   ├── products_raw.csv
│   │   └── regions_raw.csv
│   └── data_processed/
│       ├── fact_sales.csv
│       ├── dim_customer.csv
│       ├── dim_product.csv
│       ├── dim_region.csv
│       └── dim_date.csv
│
├── Scripts/
│   ├── clean_orders.py
│   ├── clean_customers.py
│   ├── clean_products.py
│   ├── clean_regions.py
│   └── clean_dates.py
│
├── dashboard/
│   ├── dashboard_template.html
│   ├── build_dashboard.py
│   └── vibe_analysis_dashboard.html
│
└── images/
    └── star_schema.svg
```

---

## Tech Stack

| Layer | Tools |
|-------|-------|
| Data processing | Python 3, pandas |
| Storage | CSV (star schema) |
| Visualization | HTML, CSS, JavaScript, Chart.js |
| Modeling | Star schema (dimensional model) |
| AI-assisted development | Cursor AI |

---

## Skills Demonstrated

- Data profiling and quality assessment
- ETL pipeline design with reproducible scripts
- Dimensional modeling (star schema)
- Business metrics definition (revenue, profit, margin, returns)
- Exploratory analysis and insight communication
- Interactive dashboard development for stakeholders

---

## Author

**Arnab Kar** — Data Analyst portfolio project
[GitHub](https://github.com/Arnab-710) · [LinkedIn](https://linkedin.com/in/arnab-kar10)

If you use or reference this work, please link back to the repository.
