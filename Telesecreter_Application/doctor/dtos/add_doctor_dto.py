from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class AddDoctorRequest(BaseModel):
    full_name: str
    email: str
    department_id: UUID
    specialty: str
    phone_number: str = ""
    ratings: float = 0.0
    is_available: bool = True
