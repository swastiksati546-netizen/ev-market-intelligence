"""Loads the CSV into a SQLite database (ev_market.db) using sql/schema.sql.
For MySQL/PostgreSQL, run schema.sql there and import the CSV with your tool's import wizard."""
import sqlite3, csv, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "ev_market.db")
if os.path.exists(DB): os.remove(DB)
con = sqlite3.connect(DB)
con.executescript(open(os.path.join(ROOT, "sql", "schema.sql")).read())
with open(os.path.join(ROOT, "data", "ev_market_data.csv")) as f:
    r = csv.reader(f); next(r)
    con.executemany("INSERT INTO ev_data VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", r)
con.execute("CREATE VIEW IF NOT EXISTS v_ev_clean AS SELECT *, ROUND(price / range_km, 2) AS price_per_km, "
            "ROUND(range_km * 1.0 / battery_capacity_kwh, 2) AS km_per_kwh, "
            "CASE WHEN range_km >= 500 THEN 'Long' WHEN range_km >= 300 THEN 'Medium' ELSE 'Short' END AS range_class "
            "FROM ev_data WHERE annual_sales IS NOT NULL AND range_km IS NOT NULL")
con.commit()
print("Rows loaded:", con.execute("SELECT COUNT(*) FROM ev_data").fetchone()[0])
con.close()
