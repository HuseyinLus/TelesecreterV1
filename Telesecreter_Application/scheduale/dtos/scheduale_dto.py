from dataclasses import dataclass
from uuid import UUID
from datetime import time, datetime


@dataclass
class SchedualeDTO:
    id: UUID
    doctor_id: UUID
    day_of_week: int
    start_time: time
    end_time: time
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(scheduale) -> "SchedualeDTO":
        return SchedualeDTO(
            id=scheduale.id,
            doctor_id=scheduale.doctor_id,
            day_of_week=scheduale.day_of_week,
            start_time=scheduale.start_time,
            end_time=scheduale.end_time,
            created_at=scheduale.created_at,
            updated_at=scheduale.updated_at,
        )