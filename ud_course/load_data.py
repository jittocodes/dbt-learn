import pandas as pd
from sqlalchemy import create_engine, text
import requests
import os

# Postgres connection from profiles.yml
DB_URL = "postgresql://admin:secret@localhost:5432/mydb"
SCHEMA = "raw_thelook"

BASE_URL = "https://raw.githubusercontent.com/dqops/dqo/develop/dqops/sampledata/files/csv/thelook-ecommerce/"
TABLES = {
    "distribution_centers": BASE_URL + "distribution_centers.csv",
    "events": BASE_URL + "events.csv",
    "inventory_items": BASE_URL + "inventory_items.csv",
    "order_items": BASE_URL + "order_items.csv",
    "orders": BASE_URL + "orders.csv",
    "products": BASE_URL + "products.csv",
    "users": BASE_URL + "users.csv"
}

def load_data():
    engine = create_engine(DB_URL)
    
    # Create schema if not exists
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA};"))
        conn.commit()
    
    for table_name, url in TABLES.items():
        print(f"Loading {table_name} from {url}...")
        try:
            # Download and load
            df = pd.read_csv(url)
            
            # Write to Postgres
            df.to_sql(
                table_name, 
                engine, 
                schema=SCHEMA, 
                if_exists='replace', 
                index=False,
                chunksize=10000 # Good for big tables like events
            )
            print(f"Successfully loaded {len(df)} rows into {SCHEMA}.{table_name}")
        except Exception as e:
            print(f"Error loading {table_name}: {e}")

if __name__ == "__main__":
    load_data()
