import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from urllib.parse import quote_plus



user = os.getenv("DB_USER")
raw_password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST", "127.0.0.1")
database = os.getenv("DB_NAME")
driver=os.getenv("DB_DRIVER")
port=os.getenv("DB_PORT")

if not all([user, raw_password, database]):
    raise RuntimeError("Database environment variables not set")

password = quote_plus(raw_password)

DATABASE_URL = (
    f"{driver}://{user}:{password}@{host}:{port}/{database}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=1800
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()



