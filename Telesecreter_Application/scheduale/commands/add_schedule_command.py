from Telesecreter_Domain.entities.scheduale import DoctorSchedule
from Telesecreter_Domain.interfaces.i_scheduale_repository import IScheduleRepository
from Telesecreter_Application.scheduale.dtos.add_schedule_dto import AddScheduleRequest
from Telesecreter_Application.scheduale.dtos.scheduale_dto import SchedualeDTO


class AddScheduleCommand:

    def __init__(self, schedule_repo: IScheduleRepository):
        self._schedule_repo = schedule_repo

    def execute(self, request: AddScheduleRequest) -> SchedualeDTO:
        schedule = DoctorSchedule(
            doctor_id=request.doctor_id,
            day_of_week=request.day_of_week,
            start_time=request.start_time,
            end_time=request.end_time,
        )
        self._schedule_repo.add(schedule)
        return SchedualeDTO.from_entity(schedule)
