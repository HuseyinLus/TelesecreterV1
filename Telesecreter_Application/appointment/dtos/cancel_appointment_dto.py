from typing import Optional
from pydantic import BaseModel


class CancelAppointmentRequest(BaseModel):
    cancellation_reason: Optional[str] = None
