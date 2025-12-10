from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from fastapi import HTTPException
from app.repositories.flight_repository import FlightRepository
from app.utils.logger import log_change
from app.utils.exception import FlightNotFound


class FlightService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = FlightRepository(db)

    def _get_flight_or_raise(self, flight_id: int):
        flight = self.repo.list(filters={"flight_id": flight_id}, limit=1)
        if not flight:
            raise FlightNotFound(flight_id)
        return flight[0]

    def _compute_diffs(self, flight, update_data: Dict[str, Any]):
        diffs = {}
        for key, new_val in update_data.items():
            if key in self.repo._cols:
                old_val = getattr(flight, key)
                if old_val != new_val:
                    diffs[key] = {"old": old_val, "new": new_val}
        return diffs

    def _commit(self):
        try:
            self.db.commit()
        except:
            self.db.rollback()
            raise

    # Create a new flight
    def create_flight(self, flight_data: Dict[str, Any]):
        flight = self.repo.create(flight_data, commit=False)
        self._commit()
        return flight

    # Update a flight and log changes
    def update_flight(self, flight_id: int, update_data: Dict[str, Any], actor: str = "system"):
        flight = self._get_flight_or_raise(flight_id)
        diffs = self._compute_diffs(flight, update_data)
        if not diffs:
            return flight
        updated = self.repo.update(flight_id, update_data, commit=False)
        self._commit()
        log_change(entity="flight", entity_id=flight_id, diffs=diffs, actor=actor)
        return updated

    # Delete a flight
    def delete_flight(self, flight_id: int) -> bool:
        flight = self._get_flight_or_raise(flight_id)
        result = self.repo.delete(flight.flight_id, commit=False)
        self._commit()
        return result

    # List flights with Pagination, Filtering and Sorting
    def list_flights(
            self,
            skip: int = 0,
            limit: int = 100,
            filters: Optional[Dict[str, Any]] = None,
            sort_by: str = "flight_id",
            sort_desc: bool = False
    ) -> List:
        if sort_by not in self.repo._cols:
            raise HTTPException(status_code=400, detail=f"Invalid sort_by column: {sort_by}")
        return self.repo.list(
            skip=skip,
            limit=limit,
            filters=filters,
            sort_by=sort_by,
            sort_desc=sort_desc
        )
