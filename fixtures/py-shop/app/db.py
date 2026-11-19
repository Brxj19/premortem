"""Database session and engine."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.settings import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
