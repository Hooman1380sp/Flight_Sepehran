from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FlightCreate(BaseModel):
    flight_number: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int
    aircraft_type: str
    seats_total: int
    seats_available: int
    status: str
    process_id: str


class FlightUpdate(BaseModel):
    flight_number: Optional[str] = None
    origin: Optional[str] = None
    destination: Optional[str] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    aircraft_type: Optional[str] = None
    seats_total: Optional[int] = None
    seats_available: Optional[int] = None
    status: Optional[str] = None


class FlightOut(BaseModel):
    flight_id: int
    flight_number: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int
    aircraft_type: str
    seats_total: int
    seats_available: int
    status: str
    created_at: datetime
    updated_at: datetime
    process_id: str

    model_config = {
        "from_attributes": True
    }
