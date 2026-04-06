from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class DoctorDTO:
    id: UUID
    full_name: str
    speciality: str
    phone_number: str
    email: str
    is_available: bool
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(doctor) -> "DoctorDTO":
        return DoctorDTO(
            id=doctor.id,
            full_name=doctor.full_name,
            speciality=doctor.specialty,
            phone_number=doctor.phone_number,
            email=doctor.email,
            is_available=doctor.is_available,
            created_at=doctor.created_at,
            updated_at=doctor.updated_at,
        )