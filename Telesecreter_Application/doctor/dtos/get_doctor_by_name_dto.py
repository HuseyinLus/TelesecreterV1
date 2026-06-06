from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class GetDoctorByNameDTO:
    id: UUID
    full_name: str
    specialty: str
    phone_number: str
    email: str
    is_available: bool
    department_id: UUID
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(doctor) -> "GetDoctorByNameDTO":
        return GetDoctorByNameDTO(
            id=doctor.id,
            full_name=doctor.full_name,
            specialty=doctor.specialty,
            phone_number=doctor.phone_number,
            email=doctor.email,
            is_available=doctor.is_available,
            department_id=doctor.department_id,
            created_at=doctor.created_at,
            updated_at=doctor.updated_at,
        )
