from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base
import crud, schemas
import requests

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Currency Exchange API", version="2.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://lustrous-pie-54fe17.netlify.app"], #connecting frontend to backend.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def sync_rates():
    url = (
        "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/"
        "accounting/od/rates_of_exchange?fields=country,currency,country_currency_desc,"
        "exchange_rate,record_date&page[size]=10000"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get("data", [])
    except Exception as e:
        print("Sync failed:", e)
        return

    with SessionLocal() as db:
        for rec in data:
            try:
                item = schemas.ConversionCreate(
                    country=rec["country"],
                    currency=rec["currency"],
                    exchange_rate=float(rec["exchange_rate"]),
                    record_date=rec["record_date"]
                )
                crud.create_conversion(db, item)
            except Exception as e:
                print(f"Skipping record due to error: {e}")


@app.get("/")
def root():
    return {"message": "Backend is up and running!"}


@app.get("/api/conversions", response_model=list[schemas.ConversionResponse])
def read_conversions(
    threshold: float = Query(None),
    above: bool = Query(True),
    db: Session = Depends(get_db)
):
    return crud.get_conversions(db, threshold, above)


@app.post("/api/conversions", response_model=schemas.ConversionResponse)
def create_conversion(conversion: schemas.ConversionCreate, db: Session = Depends(get_db)):
    return crud.create_conversion(db, conversion)


sync_rates()