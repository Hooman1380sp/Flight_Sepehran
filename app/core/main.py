from fastapi import FastAPI
import uvicorn
from app.api.flight_router import router as flight_router

app = FastAPI(
    title="Sepehran Air company",
    description="sepehran Project task",
    version="1.0.0"
)

app.include_router(flight_router, tags=["flight"], prefix="/api/flights")

# if __name__ == "__main__":
#     uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)

if __name__ == "__main__":
    uvicorn.run("app.core.main:app", host="0.0.0.0", port=8000, reload=True)
