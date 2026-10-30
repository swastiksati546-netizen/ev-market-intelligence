-- Works on SQLite, MySQL (change AUTOINCREMENT -> AUTO_INCREMENT) and PostgreSQL (use SERIAL)
CREATE TABLE IF NOT EXISTS ev_data (
  id INTEGER PRIMARY KEY,
  manufacturer VARCHAR(60) NOT NULL,
  model VARCHAR(80),
  vehicle_category VARCHAR(30) NOT NULL,
  year INTEGER NOT NULL,
  annual_sales INTEGER,
  price DECIMAL(10,2),
  battery_type VARCHAR(20),
  battery_capacity_kwh DECIMAL(6,1),
  range_km INTEGER,
  manufacturing_country VARCHAR(40),
  customer_rating DECIMAL(2,1)
);
CREATE INDEX IF NOT EXISTS idx_year ON ev_data(year);
CREATE INDEX IF NOT EXISTS idx_maker ON ev_data(manufacturer);
CREATE INDEX IF NOT EXISTS idx_cat ON ev_data(vehicle_category);
