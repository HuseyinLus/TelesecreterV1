from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import date, time, datetime

from Telesecreter_Domain.enums.appointment_status import AppointmentStatus


@dataclass
class GetAppointmentByDoctorIdDTO:
    id: UUID
    user_id: UUID
    doctor_id: UUID
    date: date
    start_time: time
    end_time: time
    status: str
    cancelled_at: Optional[str]
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(appointment) -> "GetAppointmentByDoctorIdDTO":
        return GetAppointmentByDoctorIdDTO(
            id=appointment.id,
            user_id=appointment.user_id,
            doctor_id=appointment.doctor_id,
            date=appointment.date,
            start_time=appointment.start_time,
            end_time=appointment.end_time,
            status=appointment.status.value if isinstance(appointment.status, AppointmentStatus) else appointment.status,
            cancelled_at=appointment.cancelled_at,
            created_at=appointment.created_at,
            updated_at=appointment.updated_at,
        )
