from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from typing import List, Optional, Dict, Any
from app.db.flight_models import Flight

class FlightRepository:
    def __init__(self, db: Session):
        self.db = db
        self._cols = set(Flight.__table__.columns.keys())

    # Create: repository only adds and flushes; commit handled by service/endpoint
    def create(self, flight_data: Dict[str, Any], commit: bool = False) -> Flight:
        flight = Flight(**flight_data)
        self.db.add(flight)
        if commit:
            try:
                self.db.commit()
            except:
                self.db.rollback()
                raise
            self.db.refresh(flight)
        else:
            # ensure PK/defaults are available
            self.db.flush()
            self.db.refresh(flight)
        return flight

    # Get by ID - use session.get
    # def get_by_id(self, flight_id: int) -> Optional[Flight]:
    #     return self.db.get(Flight, flight_id)

    # List with pagination/filter/sort - validate keys
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

    # Update (ORM way)
    def update(self, flight_id: int, update_data: Dict[str, Any], commit: bool = False) -> Optional[Flight]:
        flight = self.get_by_id(flight_id)
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

    # Bulk update (no object loading) - good for performance on many rows
    # def bulk_update_where(self, where_clause, values: Dict[str, Any], commit: bool = True):
    #     # where_clause is a SQLAlchemy boolean expression (e.g., Flight.origin == 'IKA')
    #     stmt = update(Flight).where(where_clause).values(**{k:v for k,v in values.items() if k in self._cols})
    #     result = self.db.execute(stmt)
    #     if commit:
    #         try:
    #             self.db.commit()
    #         except:
    #             self.db.rollback()
    #             raise
    #     return result.rowcount

    # Delete
    def delete(self, flight_id: int, commit: bool = False) -> bool:
        flight = self.get_by_id(flight_id)
        if not flight:
            return False
        self.db.delete(flight)
        if commit:
            try:
                self.db.commit()
            except:
                self.db.rollback()
                raise
        return True
