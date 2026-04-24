from Telesecreter_Domain.interfaces.i_scheduale_repository import IScheduleRepository
from Telesecreter_Application.scheduale.dtos import scheduale_dto

class GetAllSchedualesQuery:

    def __init__(self, scheduale_repository: IScheduleRepository):
        self._repository = scheduale_repository

    def execute(self) -> list[scheduale_dto.SchedualeDTO]:
        scheduales = self._repository.get_all()
        return [scheduale_dto.SchedualeDTO.from_entity(scheduale) for scheduale in scheduales]