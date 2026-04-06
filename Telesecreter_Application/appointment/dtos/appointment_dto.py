from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class AppointmentDTO:
    id: UUID
    user_id: UUID
    doctor_id: UUID
    date: datetime
    start_time: datetime
    end_time: datetime
    status: str
    cancelled_at: datetime
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(appointment) -> "AppointmentDTO":
        return AppointmentDTO(
            id=appointment.id,
            user_id=appointment.user_id,
            doctor_id=appointment.doctor_id,
            date=appointment.date,
            start_time=appointment.start_time,
            end_time=appointment.end_time,
            status=appointment.status,
            cancelled_at=appointment.cancelled_at,
            created_at=appointment.created_at,
            updated_at=appointment.updated_at,
        )