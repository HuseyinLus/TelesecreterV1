from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class UpdateDoctorRequest(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    department_id: Optional[UUID] = None
    specialty: Optional[str] = None
    phone_number: Optional[str] = None
    ratings: Optional[float] = None
    is_available: Optional[bool] = None
