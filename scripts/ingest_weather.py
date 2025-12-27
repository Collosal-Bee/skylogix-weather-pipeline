import os
import requests
import pymongo
from datetime import datetime
from dotenv import load_dotenv

# Load secrets from .env file
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
CITIES = ["Nairobi", "Lagos", "Accra", "Johannesburg"]
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_and_upsert():
    # Connect to MongoDB
    client = pymongo.MongoClient(MONGO_URI)
    db = client["skylogix_db"]
    collection = db["weather_raw"]

    print(f"--- Starting Ingestion at {datetime.now()} ---")
    
    for city in CITIES:
        try:
            # Fetch data from API
            url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                # Add 'updatedAt' for incremental processing
                data["updatedAt"] = datetime.utcnow()
                
                # Create a unique ID (City + Time) to prevent duplicates
                # API gives 'dt' (timestamp)
                unique_id = f"{data['name']}_{data['dt']}"
                
                # Upsert (Update if exists, Insert if new)
                collection.update_one(
                    {"_id": unique_id}, 
                    {"$set": data}, 
                    upsert=True
                )
                print(f"✅ Successfully ingested: {city}")
            else:
                print(f"❌ Failed {city}: {data.get('message')}")
                
        except Exception as e:
            print(f"⚠️ Error processing {city}: {e}")

if __name__ == "__main__":
    fetch_and_upsert()