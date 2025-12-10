from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.settings import get_settings

settings = get_settings()

engine = create_engine(
    url=settings.SQLITE3,
    connect_args={"check_same_thread": False},
    future=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
