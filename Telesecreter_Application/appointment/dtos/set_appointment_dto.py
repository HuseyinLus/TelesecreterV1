from dataclasses import dataclass
from datetime import date, time
from uuid import UUID

from pydantic import BaseModel


class SetAppointmentArgs(BaseModel):
    doctor_id: UUID
    user_id: UUID
    date: date
    start_time: time


class SetAppointmentRequest(BaseModel):
    args: SetAppointmentArgs


@dataclass
class SetAppointmentResponse:
    success: bool
    doctor_id: UUID
    user_id: UUID
    date: date
    start_time: time

    @staticmethod
    def from_entity(appointment) -> "SetAppointmentResponse":
        return SetAppointmentResponse(
            success=True,
            doctor_id=appointment.doctor_id,
            user_id=appointment.user_id,
            date=appointment.date,
            start_time=appointment.start_time,
        )
