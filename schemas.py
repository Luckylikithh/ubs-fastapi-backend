from pydantic import BaseModel
from datetime import date

class ConversionCreate(BaseModel):
    country: str
    currency: str
    exchange_rate: float
    record_date: date

class ConversionResponse(ConversionCreate):
    id: int

    class Config:
        orm_mode = True
