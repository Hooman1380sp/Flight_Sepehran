import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.connection import SessionLocal
# from app.db.flight_models import Flight
from app.db.base import Base
from sqlalchemy import create_engine
from app.core.settings import get_settings

settings = get_settings()
engine = create_engine(settings.SQLITE3, connect_args={"check_same_thread": False}, future=True)

# اطمینان از اینکه جدول ساخته شده
Base.metadata.create_all(bind=engine)

# باز کردن session
db: Session = SessionLocal()

# خواندن فایل JSON
with open("flights_sample.json", "r") as f:
    flights_data = json.load(f)

for flight in flights_data:
    # تبدیل رشته به datetime
    flight["departure_time"] = datetime.fromisoformat(flight["departure_time"])
    flight["arrival_time"] = datetime.fromisoformat(flight["arrival_time"])
    flight["created_at"] = datetime.fromisoformat(flight["created_at"])
    flight["updated_at"] = datetime.fromisoformat(flight["updated_at"])

    # تبدیل status به Enum
    from app.db.flight_models import FlightStatus
    flight["status"] = FlightStatus(flight["status"]).value

    # ایجاد آبجکت Flight
    flight_obj = Flight(**flight)
    db.add(flight_obj)

try:
    db.commit()
    print("All flights imported successfully!")
except Exception as e:
    db.rollback()
    print("Error:", e)
finally:
    db.close()
