from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class FlightNotFound(BaseHTTPException):
    def __init__(self, flight_id: int):
        super().__init__(status_code=404, detail=f"Flight {flight_id} not found")


class FlightUpdateFailed(BaseHTTPException):
    def __init__(self, flight_id: int):
        super().__init__(status_code=400, detail=f"Failed to update Flight {flight_id}")
