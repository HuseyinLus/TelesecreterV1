from dataclasses import dataclass, field
from datetime import date, time
from uuid import UUID


@dataclass
class AvailableSlotDTO:
    start_time: time
    end_time: time


@dataclass
class DoctorAvailabilityDTO:
    doctor_id: UUID
    date: date
    available_slots: list[AvailableSlotDTO] = field(default_factory=list)
