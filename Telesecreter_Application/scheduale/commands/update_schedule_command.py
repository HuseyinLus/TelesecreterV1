from uuid import UUID
from Telesecreter_Domain.interfaces.i_scheduale_repository import IScheduleRepository
from Telesecreter_Application.scheduale.dtos.update_schedule_dto import UpdateScheduleRequest
from Telesecreter_Application.scheduale.dtos.scheduale_dto import SchedualeDTO


class ScheduleNotFoundException(Exception):
    def __init__(self, schedule_id: UUID):
        super().__init__(f"Schedule with id '{schedule_id}' not found.")
        self.schedule_id = schedule_id


class UpdateScheduleCommand:

    def __init__(self, schedule_repo: IScheduleRepository):
        self._schedule_repo = schedule_repo

    def execute(self, schedule_id: UUID, request: UpdateScheduleRequest) -> SchedualeDTO:
        schedule = self._schedule_repo.get_by_id(schedule_id)
        if schedule is None:
            raise ScheduleNotFoundException(schedule_id)

        if request.day_of_week is not None:
            schedule.day_of_week = request.day_of_week
        if request.start_time is not None:
            schedule.start_time = request.start_time
        if request.end_time is not None:
            schedule.end_time = request.end_time

        self._schedule_repo.update(schedule)
        return SchedualeDTO.from_entity(schedule)
