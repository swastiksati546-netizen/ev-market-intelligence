-- 1. Total sales by vehicle category (Emily)
SELECT vehicle_category, SUM(annual_sales) AS total_sales
FROM ev_data GROUP BY vehicle_category ORDER BY total_sales DESC;

-- 2. Top 10 manufacturers by sales (Emily / David)
SELECT manufacturer, SUM(annual_sales) AS total_sales
FROM ev_data GROUP BY manufacturer ORDER BY total_sales DESC LIMIT 10;

-- 3. Market share % per manufacturer, using a window function (David)
SELECT manufacturer, SUM(annual_sales) AS sales,
       ROUND(100.0 * SUM(annual_sales) / SUM(SUM(annual_sales)) OVER (), 2) AS share_pct
FROM ev_data GROUP BY manufacturer ORDER BY sales DESC;

-- 4. Battery technology distribution and quality (Sarah / David)
SELECT battery_type, COUNT(*) AS models, ROUND(AVG(range_km),0) AS avg_range_km,
       ROUND(AVG(customer_rating),2) AS avg_rating
FROM ev_data GROUP BY battery_type ORDER BY models DESC;

-- 5. Sales trend by year
SELECT year, SUM(annual_sales) AS total_sales FROM ev_data GROUP BY year ORDER BY year;

-- 6. Year-over-year growth by category using CTE + LAG (Emily: high-growth segments)
WITH yearly AS (
  SELECT vehicle_category, year, SUM(annual_sales) AS sales
  FROM ev_data GROUP BY vehicle_category, year)
SELECT vehicle_category, year, sales,
       ROUND(100.0 * (sales - LAG(sales) OVER (PARTITION BY vehicle_category ORDER BY year))
             / LAG(sales) OVER (PARTITION BY vehicle_category ORDER BY year), 1) AS yoy_growth_pct
FROM yearly ORDER BY vehicle_category, year;

-- 7. Manufacturing country analysis (David / Sarah)
SELECT manufacturing_country, COUNT(DISTINCT manufacturer) AS makers, SUM(annual_sales) AS sales
FROM ev_data GROUP BY manufacturing_country ORDER BY sales DESC;

-- 8. Average range and rating by category
SELECT vehicle_category, ROUND(AVG(range_km),0) AS avg_range, ROUND(AVG(customer_rating),2) AS avg_rating
FROM ev_data GROUP BY vehicle_category ORDER BY avg_rating DESC;

-- 9. HAVING: manufacturers with avg rating >= 4.0 and total sales above 100k
SELECT manufacturer, ROUND(AVG(customer_rating),2) AS avg_rating, SUM(annual_sales) AS sales
FROM ev_data GROUP BY manufacturer
HAVING AVG(customer_rating) >= 4.0 AND SUM(annual_sales) > 100000 ORDER BY sales DESC;

-- 10. Subquery: models whose range beats their category average
SELECT model, vehicle_category, range_km FROM ev_data e
WHERE range_km > (SELECT AVG(range_km) FROM ev_data WHERE vehicle_category = e.vehicle_category)
ORDER BY range_km DESC LIMIT 20;

-- 11. Data cleaning checks
SELECT COUNT(*) AS null_rows FROM ev_data WHERE annual_sales IS NULL OR range_km IS NULL;
SELECT model, COUNT(*) FROM ev_data GROUP BY model HAVING COUNT(*) > 1;

-- 12. Clean view for Tableau (derived columns pre-computed)
CREATE VIEW IF NOT EXISTS v_ev_clean AS
SELECT *, ROUND(price / range_km, 2) AS price_per_km,
       ROUND(range_km * 1.0 / battery_capacity_kwh, 2) AS km_per_kwh,
       CASE WHEN range_km >= 500 THEN 'Long' WHEN range_km >= 300 THEN 'Medium' ELSE 'Short' END AS range_class
FROM ev_data WHERE annual_sales IS NOT NULL AND range_km IS NOT NULL;
