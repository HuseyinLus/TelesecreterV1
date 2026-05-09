from datetime import datetime, date, time
from uuid import UUID

from Telesecreter_Domain.interfaces.i_appointment_repository import IAppointmentRepository
from Telesecreter_Application.doctor.Exceptions.doctor_exception_handlers import InvalidTimeFormatError


class CheckSlotAvailabilityQuery:

    def __init__(self, appointment_repo: IAppointmentRepository):
        self._appointment_repo = appointment_repo

    def execute(self, doctor_id: UUID, date_str: str, requested_time: str) -> bool:
        appointment_date = self._parse_date(date_str)
        appointment_time = self._parse_time(requested_time)

        slot_taken = self._appointment_repo.exists_by_doctor_date_time(
            doctor_id, appointment_date, appointment_time
        )
        return not slot_taken

    def _parse_date(self, date_str: str) -> date:
        for fmt in ("%Y-%m-%d", "%m.%d"):
            try:
                parsed = datetime.strptime(date_str, fmt)
                if fmt == "%m.%d":
                    parsed = parsed.replace(year=date.today().year)
                return parsed.date()
            except ValueError:
                continue
        raise ValueError(f"Invalid date format: '{date_str}'. Use YYYY-MM-DD or MM.DD")

    def _parse_time(self, time_str: str) -> time:
        for fmt in ("%H:%M", "%H:%M:%S"):
            try:
                return datetime.strptime(time_str, fmt).time()
            except ValueError:
                continue
        raise InvalidTimeFormatError(time_str)
