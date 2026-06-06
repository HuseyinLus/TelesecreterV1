from typing import Optional
from datetime import time
from pydantic import BaseModel


class UpdateScheduleRequest(BaseModel):
    day_of_week: Optional[int] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
