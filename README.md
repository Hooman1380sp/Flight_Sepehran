# Flight Management Service — FastAPI

This project implements a backend service for managing flight data, designed as part of a technical assessment for Sepehran Airlines.  
The service follows a layered architecture to ensure scalability, maintainability, and clean separation of concerns.

---

## 🚀 Features

### Core Capabilities
- Create new flight records  
- Retrieve flight list with:
  - Pagination (`skip`, `limit`)
  - Filtering (origin, destination, status, aircraft_type, date ranges)
  - Sorting by selectable column (ASC/DESC)
- Update flight records (partial update with PATCH)
- Delete records (with safe DB-level deletion)
- Change log system that records modifications (diff tracking)
- Layered architecture (API → Service → Repository)
- Direct SQL query usage (for at least two operations)
- Error handling with proper HTTP responses
- Includes one basic unit test

---

## 📂 Project Structure

app/
│
├── api/
│ └── flight_api.py # API endpoints
│
├── service/
│ └── flight_service.py # Business logic layer
│
├── repository/
│ └── flight_repository.py # Database operations (ORM + raw SQL)
│
├── db/
│ ├── connection.py # Database session
│ └── flight_models.py # SQLAlchemy models
│
├── schemas/
│ └── flight_schema.py # Pydantic request/response models
│
└── utils/
└── logger.py # Change logging


---

## 🛠 Technologies Used

- **FastAPI**  
- **SQLAlchemy ORM + Raw SQL**
- **Pydantic**
- **SQLite / PostgreSQL** (configurable)
- **Pytest** for tests

---

## 📦 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Hooman1380sp/Flight_Sepehran.git
cd Flight_Sepehran

2. Create a virtual environment

python3 -m venv venv
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Run database migrations (if using Alembic)

alembic upgrade head

5. Start the server

uvicorn app.main:app --reload

API Docs available at:

    Swagger UI → http://127.0.0.1:8000/docs

Redoc → http://127.0.0.1:8000/redoc
📘 API Endpoints Summary
Flights
Method	Endpoint	Description
POST	/flight/create	Create a flight
GET	/flight/list	List flights (pagination, filtering, sorting)
PATCH	/flight/update/{id}	Update a flight
DELETE	/flight/delete/{id}	Delete a flight
🧪 Testing

Run tests using:

pytest -v

The test suite includes:

    A basic test verifying endpoint functionality.

🏗 Architecture Overview

The system follows a clean layered architecture:
API Layer

Handles HTTP requests/responses. Contains no business logic.
Service Layer

Validates input, computes diffs, manages update logic, and triggers logging.
Repository Layer

Responsible for all database operations using a mix of ORM and raw SQL.

This structure ensures modularity and keeps the project scalable as features grow.
📑 Logging

Every update operation creates a change-log entry with:

    Entity type (flight)

    Previous vs new values

    Actor (system/user)

    Timestamp

This improves transparency and traceability of system changes.
📄 License

This project is provided as part of a technical assessment and is free to review.
✉ Contact

Developer: Hooman Sepehri Rad
GitHub: https://github.com/Hooman1380sp
