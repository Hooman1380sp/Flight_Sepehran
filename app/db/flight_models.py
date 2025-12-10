from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, CheckConstraint, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime
from app.db.base import Base
import enum


class FlightStatus(enum.Enum):
    scheduled = "scheduled"
    delayed = "delayed"
    cancelled = "cancelled"
    departed = "departed"
    arrived = "arrived"

class Flight(Base):
    __tablename__ = "flights"

    flight_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    flight_number: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    origin: Mapped[str] = mapped_column(String(10), nullable=False)
    destination: Mapped[str] = mapped_column(String(10), nullable=False)
    departure_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    arrival_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    aircraft_type: Mapped[str] = mapped_column(String(50), nullable=False)
    seats_total: Mapped[int] = mapped_column(Integer, nullable=False)
    seats_available: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    process_id: Mapped[str] = mapped_column(String(20), nullable=False)

    __table_args__ = (
        CheckConstraint('seats_available >= 0', name='check_seats_positive'),
    )


    def __repr__(self):
        return f"<Flight {self.flight_id}>"

    def __str__(self):
        return str(self.flight_id)
