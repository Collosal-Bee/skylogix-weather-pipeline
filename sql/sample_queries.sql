-- 1. Check for extreme weather (High Wind > 10m/s)
SELECT city, observed_at, wind_speed_ms, condition_main 
FROM weather_readings 
WHERE wind_speed_ms > 10 
ORDER BY observed_at DESC;

-- 2. Average temperature per city
SELECT city, AVG(temp_c) as avg_temp, MAX(temp_c) as max_temp
FROM weather_readings
GROUP BY city;

-- 3. Rain volume analysis (Potential delay risk)
SELECT city, SUM(rain_1h_mm) as total_rain_last_24h
FROM weather_readings
WHERE observed_at >= NOW() - INTERVAL '24 hours'
GROUP BY city;