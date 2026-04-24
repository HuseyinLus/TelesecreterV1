from uuid import UUID
from datetime import time, datetime
from Telesecreter_Domain.common.base_entity import BaseEntity


class DoctorSchedule(BaseEntity):
    def __init__(
        self,
        doctor_id: UUID,
        day_of_week: int,
        start_time: time,
        end_time: time,
        id: UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(id, created_at, updated_at)
        self.doctor_id = doctor_id
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time