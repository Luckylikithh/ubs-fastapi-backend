from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import Conversion
from schemas import ConversionCreate
from typing import Optional

def create_conversion(db: Session, conversion: ConversionCreate):

    existing = db.query(Conversion).filter(
        and_(
            Conversion.country == conversion.country,
            Conversion.currency == conversion.currency,
            Conversion.record_date == conversion.record_date
        )
    ).first()
    if existing:
        return existing 

    db_conversion = Conversion(**conversion.dict())
    db.add(db_conversion)
    db.commit()
    db.refresh(db_conversion)
    return db_conversion

def get_conversions(db: Session, threshold: Optional[float] = None, above: bool = True):
    query = db.query(Conversion)
    if threshold is not None:
        if above:
            query = query.filter(Conversion.exchange_rate > threshold)
        else:
            query = query.filter(Conversion.exchange_rate < threshold)
    return query.all()
