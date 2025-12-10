from sqlalchemy.orm import Session
from sqlalchemy import select, text
from typing import List, Optional, Dict, Any
from app.db.flight_models import Flight


class FlightRepository:
    def __init__(self, db: Session):
        self.db = db
        self._cols = set(Flight.__table__.columns.keys())
        self.db = db

    def create(self, flight_data: Dict[str, Any], commit: bool = False) -> Flight:
        columns = ", ".join(flight_data.keys())
        values = ", ".join(f":{k}" for k in flight_data.keys())
        stmt = text(f"""
            INSERT INTO Flights ({columns})
            OUTPUT INSERTED.*
            VALUES ({values})
        """)
        result = self.db.execute(stmt, flight_data)
        created_row = result.fetchone()
        if commit:
            try:
                self.db.commit()
            except:
                self.db.rollback()
                raise
        flight = Flight(**created_row)
        return flight

    def list(
            self,
            skip: int = 0,
            limit: int = 100,
            filters: Optional[Dict[str, Any]] = None,
            sort_by: str = "flight_id",
            sort_desc: bool = False
    ) -> List[Flight]:
        stmt = select(Flight)
        if filters:
            for key, value in filters.items():
                if key in self._cols:
                    stmt = stmt.where(getattr(Flight, key) == value)
        if sort_by in self._cols:
            col = getattr(Flight, sort_by)
            stmt = stmt.order_by(col.desc() if sort_desc else col)
        stmt = stmt.offset(skip).limit(limit)
        return self.db.execute(stmt).scalars().all()

    # Update (ORM) بدون تغییر
    def update(self, flight_id: int, update_data: Dict[str, Any], commit: bool = False) -> Optional[Flight]:
        flight = self.db.get(Flight, flight_id)
        if not flight:
            return None
        for key, val in update_data.items():
            if key in self._cols:
                setattr(flight, key, val)
        if commit:
            try:
                self.db.commit()
            except:
                self.db.rollback()
                raise
            self.db.refresh(flight)
        else:
            self.db.flush()
            self.db.refresh(flight)
        return flight

    def delete(self, flight_id: int, commit: bool = False) -> bool:
        stmt = text("""
            DELETE FROM Flights
            OUTPUT DELETED.*
            WHERE flight_id = :flight_id
        """)
        result = self.db.execute(stmt, {"flight_id": flight_id})
        if commit:
            try:
                self.db.commit()
            except:
                self.db.rollback()
                raise
        deleted_row = result.fetchone()
        return deleted_row is not None
