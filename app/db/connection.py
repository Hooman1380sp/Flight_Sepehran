from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.settings import get_settings


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
