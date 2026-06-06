from uuid import UUID
from datetime import time
from pydantic import BaseModel


class AddScheduleRequest(BaseModel):
    doctor_id: UUID
    day_of_week: int
    start_time: time
    end_time: time
