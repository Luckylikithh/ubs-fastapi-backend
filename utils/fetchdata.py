import requests
from sqlalchemy.orm import Session
from models import Conversion
from database import SessionLocal
from datetime import datetime

API_URL = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/rates_of_exchange"

def fetch_and_store_data():
    print("🚀 fetch_and_store_data is running...")
    print("Fetching data from API...")
    session: Session = SessionLocal()

    try:
        page = 1
        all_data = []

        while True:
            response = requests.get(API_URL, params={"page[number]": page})
            if response.status_code != 200:
                print("Failed to fetch page", page)
                break

            json_data = response.json()
            records = json_data.get("data", [])

            if not records:
                break

            for item in records:
                # Parse each field
                record = Conversion(
                    country=item.get("country"),
                    currency=item.get("currency"),
                    exchange_rate=float(item.get("exchange_rate")),
                    record_date=datetime.strptime(item.get("record_date"), "%Y-%m-%d").date()
                )
                all_data.append(record)

            print(f"Fetched page {page} with {len(records)} records.")
            page += 1

        # Optional: Clear old data
        session.query(Conversion).delete()

        # Bulk insert
        session.bulk_save_objects(all_data)
        session.commit()
        print(f"Inserted {len(all_data)} records into the database.")

    except Exception as e:
        print("Error occurred:", e)
        session.rollback()
    finally:
        session.close()
