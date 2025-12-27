from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Ensure Airflow can find your scripts folder
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../scripts'))

from ingest_weather import fetch_and_upsert
from transform_load import transform_and_load

default_args = {
    'owner': 'skylogix',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'skylogix_weather_pipeline',
    default_args=default_args,
    description='End-to-end Weather Pipeline',
    schedule_interval='*/15 * * * *', # Runs every 15 minutes
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id='fetch_and_upsert_raw',
        python_callable=fetch_and_upsert,
    )

    t2 = PythonOperator(
        task_id='transform_and_load_postgres',
        python_callable=transform_and_load,
    )

    t1 >> t2