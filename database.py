from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

# Get database URL from environment or use SQLite by default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///habits.db")

# Create database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()

class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    habit_name = Column(String, unique=True, index=True)
    created_date = Column(Date, default=datetime.now().date())
    target_frequency = Column(String)
    check_ins = Column(String, default="")

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
