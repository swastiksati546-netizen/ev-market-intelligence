# Tableau Build Guide

Follow this in Tableau Desktop. The workbook itself can't be generated outside Tableau, so this is the exact spec to build it.

## 1. Connect
- **Live DB:** Data > Connect > MySQL / PostgreSQL > table `ev_data` (or view `v_ev_clean`).
- **From SQLite file:** install the SQLite ODBC driver, or simply connect to the CSV `data/ev_market_data.csv` (Text file).
- For Tableau Public publishing, use an **Extract** (Tableau Public cannot hold live DB connections).
- Set `manufacturing_country` > Geographic Role > Country/Region.

## 2. Calculated fields (10)
| # | Name | Formula |
|---|------|---------|
| 1 | Market Share % | `SUM([Annual Sales]) / TOTAL(SUM([Annual Sales]))` |
| 2 | YoY Growth % | `(SUM([Annual Sales]) - LOOKUP(SUM([Annual Sales]),-1)) / ABS(LOOKUP(SUM([Annual Sales]),-1))` |
| 3 | Price per km | `[Price] / [Range Km]` |
| 4 | Range Class | `IF [Range Km]>=500 THEN "Long" ELSEIF [Range Km]>=300 THEN "Medium" ELSE "Short" END` |
| 5 | Satisfaction Tier | `IF [Customer Rating]>=4.5 THEN "Excellent" ELSEIF [Customer Rating]>=4 THEN "Good" ELSEIF [Customer Rating]>=3.5 THEN "Average" ELSE "Poor" END` |
| 6 | Sales Rank | `RANK(SUM([Annual Sales]))` |
| 7 | Energy Efficiency (km/kWh) | `[Range Km] / [Battery Capacity Kwh]` |
| 8 | High Growth Flag | `IF [YoY Growth %] > 0.15 THEN "High Growth" ELSE "Stable" END` |
| 9 | Avg Rating (weighted) | `SUM([Customer Rating]*[Annual Sales]) / SUM([Annual Sales])` |
| 10 | Top N Manufacturer | `IF [Sales Rank] <= [Top N Parameter] THEN [Manufacturer] ELSE "Others" END` (create parameter `Top N Parameter`, integer, default 5) |

## 3. Visualizations (14)
| # | Sheet name | Type | Setup |
|---|-----------|------|-------|
| 1 | KPI Total Sales | Text tile | SUM(Annual Sales) |
| 2 | KPI Avg Range | Text tile | AVG(Range Km) |
| 3 | KPI Avg Rating | Text tile | AVG(Customer Rating) |
| 4 | Sales by Category | Bar | Category x SUM(Sales), sorted desc |
| 5 | Sales Trend | Line | Year x SUM(Sales), color by Category |
| 6 | Top Manufacturers | Bar | Top N Manufacturer x SUM(Sales) |
| 7 | Market Share | Treemap | Manufacturer, size SUM(Sales), label Market Share % |
| 8 | Battery Mix | Donut / Pie | Battery Type, angle COUNT(Model) |
| 9 | Range by Category | Box plot | Category x Range Km |
| 10 | Range vs Capacity | Scatter | Capacity x Range, color Battery Type, size Sales |
| 11 | Rating by Category | Bar | Category x AVG(Rating), color Satisfaction Tier |
| 12 | Manufacturing Map | Filled map | Country, color SUM(Sales) |
| 13 | Battery x Category Heatmap | Highlight table | Battery Type x Category, color AVG(Rating) |
| 14 | Growth by Category | Bar | Category x YoY Growth %, color High Growth Flag |

## 4. Dashboards (3 + story) and filters
| Dashboard | Sheets | Persona |
|-----------|--------|---------|
| **D1 Executive Strategy** | 1,2,3,4,5,11,14,8 | Emily |
| **D2 Competitive Intelligence** | 1,6,7,12,11,13 | David |
| **D3 Tech & Sustainability** | 8,9,10,12,13 | Sarah |

**Filters (show on every dashboard, "Apply to Worksheets > All Using This Data Source"):** Year (range slider), Vehicle Category, Manufacturer, Battery Type, Manufacturing Country, Top N parameter.
**Actions:** Dashboard > Actions > add a *Filter* action (Select, all sheets) and a *Highlight* action.

**Responsive design:** Dashboard pane > Size > *Automatic*, use horizontal/vertical **containers**, then Device Preview > add **Tablet** and **Phone** layouts and remove less important sheets from phone.

## 5. Story - 6 scenes
1. **Market overview:** KPIs + sales trend
2. **Category performance:** sales by category, growth by category
3. **Who leads:** top manufacturers + market share treemap
4. **Battery technology:** battery mix + range vs capacity
5. **Global manufacturing:** map + country sales
6. **Recommendations:** rating heatmap + a text box with 3 takeaways

## 6. Publish
Server > Tableau Public > Save to Tableau Public (extract). Copy each view URL into `TABLEAU = {...}` in `flask_app/app.py`.
