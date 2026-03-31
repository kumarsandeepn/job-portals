from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ✅ DB URL define करना जरूरी है
DATABASE_URL = "sqlite:///./jobportal.db"

# Engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()