# Technical Report: SkyLogix Weather Pipeline

## Design Decisions
* **Staging Strategy:** MongoDB was chosen for the staging layer to handle the flexible JSON schema from the OpenWeather API without data loss.
* **Upsert Logic:** A composite key (`City_Timestamp`) is used to prevent duplicate records during network retries.
* **Normalization:** The transformation layer flattens nested JSON (e.g., `main.temp`, `wind.speed`) into a relational schema optimized for SQL aggregation.

## Assumptions
* The pipeline assumes the API is available and rate limits are respected (60 calls/min).
* "Real-time" is defined as a 15-minute polling interval, which balances data freshness with API costs.

## Findings
* Data ingestion successfully handles all 4 target cities.
* PostgreSQL indexing on `(city, observed_at)` significantly improves time-series query performance.