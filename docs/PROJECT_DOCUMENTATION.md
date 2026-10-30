# EV Market Intelligence: Project Documentation

## 1. Problem understanding
The EV industry produces large volumes of sales, battery, manufacturing and customer-satisfaction data. Three stakeholders need different views of it:

| Persona | Role | Needs |
|---|---|---|
| Emily Johnson | Market Strategy Director | Sales by category, leading manufacturers, satisfaction by segment, battery adoption, range by category, high-growth segments |
| David Chen | BI Manager (consulting) | Market share, annual sales, battery distribution, manufacturing-country analysis, ratings, competitive advantages |
| Dr. Sarah Williams | Sustainable Mobility Researcher | Battery technology comparison, range improvements, global manufacturing distribution, satisfaction across categories |

**Solution:** SQL database > Tableau dashboards and story > embedded in a Flask web app.

## 2. Data collection
- **Dataset:** `data/ev_market_data.csv`, 2,200 rows x 12 columns.
- **Source:** synthetic data from `data/generate_dataset.py` (seeded, so it is reproducible). It is **not real market data**; replace it with a Kaggle or other public EV dataset if your instructor requires real data (keep the same column names).
- **Columns:** id, manufacturer, model, vehicle_category, year, annual_sales, price, battery_type, battery_capacity_kwh, range_km, manufacturing_country, customer_rating.
- **Coverage:** 16 manufacturers, 6 categories (Hatchback, Sedan, SUV, Bus, Truck, Two-Wheeler), 5 battery types (LFP, NMC, NCA, Sodium-Ion, Solid-State), 6 countries, years 2019-2025.

## 3. Storing data in the database
1. Run `python data/generate_dataset.py` to create the CSV.
2. Run `python sql/load_db.py` to create `ev_market.db` (SQLite) from `sql/schema.sql` and load the CSV.
3. For MySQL/PostgreSQL: run `sql/schema.sql` in that DB, then import the CSV with the import wizard (MySQL Workbench: Table Data Import; pgAdmin: Import/Export).
Result: `SELECT COUNT(*) FROM ev_data` returns **2200**. Three indexes (year, manufacturer, category) were added for faster filtering.

## 4. SQL operations (`sql/queries.sql`, all 13 statements tested)
Aggregation (`GROUP BY`), sorting and `LIMIT`, window function (`SUM() OVER`) for market share, CTE with `LAG` for YoY growth, `HAVING`, correlated subquery, null/duplicate checks, and a cleaned **view** `v_ev_clean` with derived columns (price_per_km, km_per_kwh, range_class).

## 5. Connect DB to Tableau and prepare the data
See `docs/TABLEAU_BUILD_GUIDE.md` sections 1-2: connect to the table or view, set the country geographic role, create 10 calculated fields, and use an extract for publishing. Data prep already handled in SQL: null filtering and derived columns in the view.

## 6. Visualizations, dashboards, story
- **14 unique visualizations**, **3 dashboards** (one per persona), and a **6-scene story**. Full specs are in the build guide.
- **Filters:** Year, Category, Manufacturer, Battery Type, Country, and a Top-N parameter, plus filter and highlight actions.
- **Responsive:** automatic sizing with containers and Tablet/Phone device layouts.

## 7. Key findings from the dataset (values from the SQL queries; synthetic data)
- **SUV** is the largest category (about 3.05M units, 49% of sales), followed by Sedan (1.35M) and Hatchback (1.06M). Buses and trucks are niche.
- **BYD (27.6%) and Tesla (22.5%)** hold about half the market; the next three (Hyundai, Kia, Volkswagen) each hold 6-7%.
- **Sales grew every year**, from about 0.45M units in 2019 to about 1.36M in 2025 (roughly 3x).
- **LFP is the most common battery** (956 models), then NMC (770). NMC and Solid-State show the highest average ratings (4.14 and 4.15).
- **China (2.25M units) and the USA (1.71M)** lead production by sales, followed by South Korea and Germany.
- Customer ratings are close across categories (4.05-4.07), so satisfaction is driven more by battery type and manufacturer than by body type.
- Sodium-Ion shows a slightly lower average rating (3.90) with fewer models (80), suggesting an early-stage technology.

## 8. Performance testing
| Metric | Value |
|---|---|
| Rows in the database | 2,200 |
| Columns | 12 (+3 derived in view) |
| Calculated fields | 10 |
| Visualizations (sheets) | 14 |
| Dashboards / story scenes | 3 / 6 |
| Filters | 5 filters + 1 parameter |
| SQL query time, aggregate queries (measured on SQLite) | 0.5-0.9 ms each |
| Tableau extract load time | *(fill in from Performance Recorder)* |
| Dashboard render time | *(fill in from Performance Recorder)* |
Optimisations: use extracts, index the filter columns, show only needed columns, and use "Apply to Worksheets" selectively.

## 9. Web integration (Flask)
`flask_app/app.py` serves a home page with live KPIs read from the DB, one page per dashboard and the story using Tableau's Embedding API v3 (`<tableau-viz>`), and JSON endpoints `/api/summary` and `/api/market-share`. Run: `pip install -r requirements.txt && python flask_app/app.py`, then open http://127.0.0.1:5000. All routes were tested and return HTTP 200.

## 10. Conclusion
The solution answers each persona's questions with a SQL-backed, filterable, responsive dashboard set, a guided story, and a web front end.
