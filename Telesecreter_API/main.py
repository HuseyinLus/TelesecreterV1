import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure the backend directory is in the Python path so it can import Telesecretary namespace properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Telesecreter_API.routers import doctor_controller, user_controller,department_controller,appointment_controller,scheduale_controller


app = FastAPI(
    title="Telesecretary API",
    description="Backend API for the Telesecretary application",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect all routers
app.include_router(user_controller.router)
app.include_router(doctor_controller.router)
app.include_router(department_controller.router)
app.include_router(appointment_controller.router)
app.include_router(scheduale_controller.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Telesecretary API! Visit /docs for Swagger documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
