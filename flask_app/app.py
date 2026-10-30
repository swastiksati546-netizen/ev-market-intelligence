import os, sqlite3
from flask import Flask, render_template, jsonify

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(os.path.dirname(BASE), "ev_market.db")

app = Flask(__name__)

# Paste your published Tableau URLs here (Tableau Public / Cloud / Server).
# Leave as None to show a setup placeholder.
TABLEAU = {
    "emily":  None,   # e.g. "https://public.tableau.com/views/EVMarket/EmilyDashboard"
    "david":  None,
    "sarah":  None,
    "story":  None,
}

PAGES = {
    "emily": ("Executive Market Strategy", "Emily Johnson - Market Strategy Director",
              "Category sales, leading manufacturers, customer satisfaction, battery adoption, high-growth segments."),
    "david": ("Competitive Intelligence", "David Chen - Business Intelligence Manager",
              "Market share, annual sales, battery distribution, manufacturing country, customer ratings."),
    "sarah": ("Technology & Sustainability Research", "Dr. Sarah Williams - Research Analyst",
              "Battery technology comparison, range improvements, global manufacturing, satisfaction by category."),
    "story": ("EV Market Story", "Guided 6-scene narrative",
              "Overview > Categories > Leaders > Battery tech > Global manufacturing > Recommendations."),
}

def q(sql, args=()):
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    rows = [dict(r) for r in con.execute(sql, args).fetchall()]
    con.close()
    return rows

@app.context_processor
def inject():
    return {"pages": PAGES}

@app.route("/")
def home():
    kpi = q("SELECT COUNT(*) models, SUM(annual_sales) sales, ROUND(AVG(range_km)) rng, "
            "ROUND(AVG(customer_rating),2) rating FROM ev_data")[0]
    return render_template("home.html", kpi=kpi)

@app.route("/view/<key>")
def view(key):
    if key not in PAGES: return "Not found", 404
    title, who, desc = PAGES[key]
    return render_template("view.html", key=key, title=title, who=who, desc=desc, url=TABLEAU[key])

# Lightweight JSON endpoints, useful for testing the DB connection and for the report
@app.route("/api/summary")
def summary():
    return jsonify(q("SELECT vehicle_category, SUM(annual_sales) total_sales FROM ev_data "
                     "GROUP BY vehicle_category ORDER BY total_sales DESC"))

@app.route("/api/market-share")
def share():
    return jsonify(q("SELECT manufacturer, SUM(annual_sales) sales, "
                     "ROUND(100.0*SUM(annual_sales)/SUM(SUM(annual_sales)) OVER (),2) share_pct "
                     "FROM ev_data GROUP BY manufacturer ORDER BY sales DESC"))

if __name__ == "__main__":
    app.run(debug=True)
