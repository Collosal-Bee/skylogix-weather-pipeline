# 🌤️ SkyLogix Weather Data Pipeline

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)](#)
[![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)](#)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](#)

An automated, end-to-end data engineering pipeline designed to ingest real-time weather data across major African logistics hubs (Nairobi, Lagos, Accra, Johannesburg). This pipeline eliminates manual data handling by orchestrating the extraction, NoSQL staging, and relational transformation of API payloads to support downstream climate and transportation analytics.

## 🧠 Architecture Overview
The pipeline implements a robust **Extract, Load, Transform (ELT)** architecture decoupled across multiple database paradigms:

1. **Extraction:** Python workers ping the OpenWeatherMap REST API on a scheduled cadence.
2. **Staging (Landing Zone):** Raw, nested JSON payloads are upserted into **MongoDB** (`weather_raw` collection) to preserve the immutable system of record.
3. **Transformation & Warehousing:** Data is normalized, flattened, and loaded into a structured **PostgreSQL** warehouse (`weather_readings` table) for high-performance SQL querying.
4. **Orchestration:** The entire workflow is managed, scheduled, and monitored using **Apache Airflow** DAGs.

## ⚙️ Core Engineering Highlights
* **Automated Orchestration:** Utilized Apache Airflow to handle retry logic, dependency management, and cron-based scheduling, ensuring the pipeline runs autonomously and recovers gracefully from API timeouts.
* **NoSQL to SQL Normalization:** Engineered transformation scripts to dynamically flatten nested JSON meteorological data into strict, strongly-typed relational schemas.
* **Idempotent Upserts:** Pipeline is designed to be fully idempotent; rerunning historical DAGs will safely overwrite existing records without creating duplicates.

## 💻 Local Development Setup

**1. Clone and Install Dependencies**
```bash
git clone [https://github.com/Collosal-Bee/skylogix-weather-pipeline.git](https://github.com/Collosal-Bee/skylogix-weather-pipeline.git)
cd skylogix-weather-pipeline
pip install -r requirements.txt
```

**2. Configure Environment**
Copy the sample environment file and inject your specific credentials:
```bash
cp .env.example .env
# Edit .env to include your OpenWeatherMap API Key, MongoDB URI, and Postgres Credentials
```

**3. Initialize & Run**
```bash
# Initialize PostgreSQL schemas
psql -U your_user -d your_db -f sql/create_table.sql

# Execute Ingestion & Transformation manually (or via Airflow UI)
python scripts/ingest_weather.py
python scripts/transform_load.py
```
