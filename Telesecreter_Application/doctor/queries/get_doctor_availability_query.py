from datetime import datetime, date
from uuid import UUID

from Telesecreter_Domain.interfaces.i_scheduale_repository import IScheduleRepository
from Telesecreter_Application.doctor.Exceptions.doctor_exception_handlers import PastDateError


class GetDoctorAvailabilityQuery:

    def __init__(self, schedule_repo: IScheduleRepository):
        self._schedule_repo = schedule_repo

    def execute(self, doctor_id: UUID, date_str: str) -> bool:
        target_date = datetime.strptime(date_str, "%m.%d").replace(year=date.today().year).date()

        if target_date < date.today():
            raise PastDateError()

        schedules = self._schedule_repo.get_by_doctor_and_day(doctor_id, target_date.weekday())
        return len(schedules) > 0
