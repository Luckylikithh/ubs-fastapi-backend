from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://conversion_db_user:cfT1YV89IKhP1UJyAXIzyDI6oxoMV8x0@dpg-d1t74v3uibrs738vu1tg-a.oregon-postgres.render.com/conversion_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
