# EV Market Intelligence: SQL + Tableau + Flask

End-to-end analytics project: database, Tableau dashboards and story, Flask web integration. Personas: Emily Johnson, David Chen, Dr. Sarah Williams.

> The dataset is **synthetic** (generated for coursework). The Tableau workbook must be built in Tableau Desktop using `docs/TABLEAU_BUILD_GUIDE.md`.

## Quick start
```bash
pip install -r requirements.txt
python data/generate_dataset.py     # creates data/ev_market_data.csv
python sql/load_db.py               # creates ev_market.db
python flask_app/app.py             # open http://127.0.0.1:5000
```

## Structure
```
data/    dataset + generator
sql/     schema, 13 queries, DB loader
tableau/ put your .twbx here
flask_app/  web app (app.py, templates, static)
docs/    PROJECT_DOCUMENTATION.md, TABLEAU_BUILD_GUIDE.md, VIDEO_SCRIPT.md
```

## After publishing in Tableau
Paste the dashboard URLs into the `TABLEAU` dict in `flask_app/app.py`.

## Demo video
`docs/video/EV_Market_Demo.mp4` is a silent, captioned walkthrough built from real query output and app screenshots (script: `docs/video/make_video.py`). The Tableau segment is a placeholder card; replace it with your own screen recording. For a narrated version, follow `docs/VIDEO_SCRIPT.md`.
