-- sql/create_table.sql
CREATE TABLE IF NOT EXISTS weather_readings (
    id SERIAL PRIMARY KEY,
    city VARCHAR(50),
    country VARCHAR(10),
    observed_at TIMESTAMP,
    lat NUMERIC,
    lon NUMERIC,
    temp_c NUMERIC,
    feels_like_c NUMERIC,
    pressure_hpa INTEGER,
    humidity_pct INTEGER,
    wind_speed_ms NUMERIC,
    wind_deg INTEGER,
    cloud_pct INTEGER,
    visibility_m INTEGER,
    rain_1h_mm NUMERIC,
    snow_1h_mm NUMERIC,
    condition_main VARCHAR(50),
    condition_description VARCHAR(100),
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(city, observed_at) -- Prevents duplicates
);

-- Create index for fast time-series queries [cite: 82]
CREATE INDEX IF NOT EXISTS idx_city_time ON weather_readings (city, observed_at);