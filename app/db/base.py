from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models here so Alembic can detect them
from app.db.flight_models import Flight
