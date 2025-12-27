# SkyLogix Transportation - Weather Data Pipeline

## Project Overview
This project implements a real-time data pipeline for SkyLogix Transportation. It ingests weather data from OpenWeatherMap for Nairobi, Lagos, Accra, and Johannesburg, stages it in MongoDB, and transforms it into a structured PostgreSQL warehouse for analytics.

## Architecture
1. **Ingestion:** Python script fetches JSON data from OpenWeatherMap API.
2. **Staging:** Raw data is upserted into MongoDB (Collection: `weather_raw`).
3. **Orchestration:** Apache Airflow DAG schedules the process.
4. **Warehousing:** Data is normalized and loaded into PostgreSQL (Table: `weather_readings`).

## Prerequisites
* Python 3.10+
* MongoDB Community Server
* PostgreSQL 14+

## Setup & Run
1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Configure Environment:**
    Copy `.env.example` to `.env` and add your API Key and DB credentials.
3.  **Initialize Database:**
    Run the SQL script in `sql/create_table.sql`.
4.  **Run Pipeline:**
    * Ingest: `python scripts/ingest_weather.py`
    * Transform: `python scripts/transform_load.py`

## Project Structure
* `dags/`: Airflow DAGs
* `scripts/`: Python ETL scripts
* `sql/`: Database DDL and sample queries
* `config/`: Configuration files