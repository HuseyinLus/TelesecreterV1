from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class DoctorDTO:
    id: UUID
    full_name: str
    specialization: str
    phone_number: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(doctor) -> "DoctorDTO":
        return DoctorDTO(
            id=doctor.id,
            full_name=doctor.full_name,
            specialization=doctor.specialization,
            phone_number=doctor.phone_number,
            email=doctor.email,
            is_active=doctor.is_active,
            created_at=doctor.created_at,
            updated_at=doctor.updated_at,
        )