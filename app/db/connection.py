import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from urllib.parse import quote_plus
from dotenv import load_dotenv
load_dotenv(override=True)


user = os.getenv("DB_USER")
raw_password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")
driver=os.getenv("DB_DRIVER")
port=os.getenv("DB_PORT")

print("HOST =", host)
print("PORT =", port)
print("DB =", database)
print("USER =", user)

if not all([user, raw_password, database, driver, port]):
    raise RuntimeError("Database environment variables not set")

password = quote_plus(raw_password)

DATABASE_URL = (
    f"{driver}://{user}:{password}@{host}:{port}/{database}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=1800,
    connect_args={
        "ssl": {
            "ca": "certs/isrgrootx1.pem"
        }
    }
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



