# Demo Video Script (about 9 minutes)
Record with OBS Studio, Zoom (share screen + record), or Windows Game Bar (Win+G). Speak slowly. Keep the DB tool, Tableau, and the browser open before starting.

| Time | Screen | Say |
|------|--------|-----|
| 0:00-0:40 | Title slide / README | "This project is an EV Market Intelligence solution. It supports three users: Emily, a strategy director; David, a BI manager; and Dr. Sarah, a researcher. It uses SQL, Tableau and Flask." |
| 0:40-1:30 | docs/PROJECT_DOCUMENTATION.md, problem section | Explain the three scenarios and the questions each one needs answered. |
| 1:30-2:30 | `data/ev_market_data.csv` + `generate_dataset.py` | "The dataset has 2,200 records across 16 manufacturers, 6 vehicle categories and 7 years. It is synthetic, built to mirror real EV attributes." |
| 2:30-3:40 | DB tool running schema.sql and load_db.py | Create table, load data, show `SELECT COUNT(*)` = 2200. |
| 3:40-4:40 | Run 3-4 queries from `sql/queries.sql` | Show market share (window function), YoY growth (CTE + LAG), HAVING query. Explain results. |
| 4:40-5:30 | Tableau: connect + data prep | Show connection, geographic role, calculated fields list. |
| 5:30-6:40 | Tableau: dashboards | Click filters and highlight actions on D1, D2, D3. Show phone layout in Device Preview. |
| 6:40-7:20 | Tableau: story | Walk through the 6 scenes. |
| 7:20-8:30 | Browser: Flask app at localhost:5000 | Show home KPIs, each embedded dashboard, and the story page. |
| 8:30-9:00 | Documentation + GitHub repo | Summarise findings, mention performance table and repo link. Thank the viewer. |
