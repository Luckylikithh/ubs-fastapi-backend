from sqlalchemy import Column, Integer, String, Float, Date
from database import Base

class Conversion(Base):
    __tablename__ = "conversions"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    exchange_rate = Column(Float, nullable=False)
    record_date = Column(Date, nullable=False)
