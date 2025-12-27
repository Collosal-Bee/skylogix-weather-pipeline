import os
import pymongo
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def transform_and_load():
    # Connect to Mongo (Source)
    mongo_client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    mongo_coll = mongo_client["skylogix_db"]["weather_raw"]

    # Connect to Postgres (Destination)
    try:
        pg_conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database="postgres", # Default DB name
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        cursor = pg_conn.cursor()
    except Exception as e:
        print(f"Database Connection Failed: {e}")
        return

    # Grab all data from Mongo
    raw_docs = mongo_coll.find({})
    print(f"--- Starting ETL at {datetime.now()} ---")

    insert_query = """
        INSERT INTO weather_readings (
            city, country, observed_at, lat, lon, temp_c, feels_like_c, 
            pressure_hpa, humidity_pct, wind_speed_ms, wind_deg, cloud_pct, 
            visibility_m, rain_1h_mm, snow_1h_mm, condition_main, condition_description
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (city, observed_at) DO NOTHING;
    """

    count = 0
    for doc in raw_docs:
        try:
            # SAFELY extract fields (Handle missing data with .get defaults)
            weather_list = doc.get("weather", [{}])
            weather_first = weather_list[0] if weather_list else {}
            main = doc.get("main", {})
            wind = doc.get("wind", {})
            clouds = doc.get("clouds", {})
            rain = doc.get("rain", {})
            snow = doc.get("snow", {})
            sys = doc.get("sys", {})
            coord = doc.get("coord", {})

            # Map JSON to Table Columns
            row = (
                doc.get("name"),
                sys.get("country"),
                datetime.fromtimestamp(doc.get("dt")),
                coord.get("lat"),
                coord.get("lon"),
                main.get("temp"),
                main.get("feels_like"),
                main.get("pressure"),
                main.get("humidity"),
                wind.get("speed"),
                wind.get("deg"),
                clouds.get("all"),
                doc.get("visibility"),
                rain.get("1h", 0.0), # Default to 0.0 if missing
                snow.get("1h", 0.0),
                weather_first.get("main"),
                weather_first.get("description")
            )
            
            cursor.execute(insert_query, row)
            count += 1
        
        except Exception as e:
            print(f"Error transforming doc {doc.get('_id')}: {e}")

    pg_conn.commit()
    cursor.close()
    pg_conn.close()
    print(f"✅ ETL Complete. Processed {count} records.")

if __name__ == "__main__":
    transform_and_load()