from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.connection import get_db
from app.service.flight_service import FlightService
from app.schemas.flight_schema import FlightCreate, FlightUpdate, FlightOut

# router = APIRouter(prefix="/flights", tags=["flights"])
router = APIRouter()


@router.post("/create", response_model=FlightOut)
def create_flight(flight_data: FlightCreate, db: Session = Depends(get_db)):
    service = FlightService(db)
    flight = service.create_flight(flight_data.dict())
    return flight


@router.patch("/update/{flight_id}", response_model=FlightOut)
def update_flight(flight_id: int, flight_data: FlightUpdate, db: Session = Depends(get_db)):
    service = FlightService(db)
    try:
        updated = service.update_flight(flight_id, flight_data.dict(exclude_unset=True))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return updated


@router.delete("/delete/{flight_id}")
def delete_flight(flight_id: int, db: Session = Depends(get_db)):
    service = FlightService(db)
    result = service.delete_flight(flight_id)
    if not result:
        raise HTTPException(status_code=404, detail="Flight not found")
    return {"detail": "Flight deleted successfully"}


@router.get("/list", response_model=List[FlightOut])
def list_flights(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1),
        sort_by: str = "flight_id",
        sort_desc: bool = False,
        origin: Optional[str] = None,
        destination: Optional[str] = None,
        status: Optional[str] = None,
        aircraft_type: Optional[str] = None,
        db: Session = Depends(get_db)
):
    filters = {}
    if origin:
        filters["origin"] = origin
    if destination:
        filters["destination"] = destination
    if status:
        filters["status"] = status
    if aircraft_type:
        filters["aircraft_type"] = aircraft_type

    service = FlightService(db)
    try:
        flights = service.list_flights(
            skip=skip,
            limit=limit,
            filters=filters,
            sort_by=sort_by,
            sort_desc=sort_desc
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return flights
