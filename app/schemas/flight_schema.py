from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FlightCreate(BaseModel):
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime


class FlightUpdate(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None


class FlightOut(BaseModel):
    flight_id: int
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime

    model_config = {
        "from_attributes": True
    }
