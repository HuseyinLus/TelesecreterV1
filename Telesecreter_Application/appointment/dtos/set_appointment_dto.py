from dataclasses import dataclass
from datetime import date, time, datetime
from uuid import UUID

from pydantic import BaseModel

from Telesecreter_Domain.enums.appointment_status import AppointmentStatus


class SetAppointmentRequest(BaseModel):
    doctor_id: UUID
    user_id: UUID
    date: date
    start_time: time


@dataclass
class SetAppointmentResponse:
    id: UUID
    doctor_id: UUID
    user_id: UUID
    date: date
    start_time: time
    end_time: time
    status: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(appointment) -> "SetAppointmentResponse":
        return SetAppointmentResponse(
            id=appointment.id,
            doctor_id=appointment.doctor_id,
            user_id=appointment.user_id,
            date=appointment.date,
            start_time=appointment.start_time,
            end_time=appointment.end_time,
            status=appointment.status.value if isinstance(appointment.status, AppointmentStatus) else appointment.status,
            created_at=appointment.created_at,
            updated_at=appointment.updated_at,
        )
