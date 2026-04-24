from uuid import UUID
from datetime import date, time, datetime
from typing import Optional
from Telesecreter_Domain.common.base_entity import BaseEntity
from Telesecreter_Domain.enums.appointment_status import AppointmentStatus


class Appointment(BaseEntity):
    def __init__(
        self,
        user_id: UUID,
        doctor_id: UUID,
        date: date,
        start_time: time,
        end_time: time,
        status: AppointmentStatus = AppointmentStatus.PENDING,
        notes: Optional[str] = None,
        cancelled_at: Optional[str] = None,
        cancellation_reason: Optional[str] = None,
        id: UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(id, created_at, updated_at)
        self.user_id = user_id
        self.doctor_id = doctor_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.cancelled_at = cancelled_at
        self.cancellation_reason = cancellation_reason