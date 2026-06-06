from uuid import UUID
from Telesecreter_Domain.interfaces.i_scheduale_repository import IScheduleRepository
from Telesecreter_Application.scheduale.commands.update_schedule_command import ScheduleNotFoundException


class DeleteScheduleCommand:

    def __init__(self, schedule_repo: IScheduleRepository):
        self._schedule_repo = schedule_repo

    def execute(self, schedule_id: UUID) -> None:
        if self._schedule_repo.get_by_id(schedule_id) is None:
            raise ScheduleNotFoundException(schedule_id)
        self._schedule_repo.delete(schedule_id)
