from abc import abstractmethod
from uuid import UUID
from Telesecreter_Domain.interfaces.i_base_repository import IBaseRepository
from Telesecreter_Domain.entities.scheduale import DoctorSchedule


class IScheduleRepository(IBaseRepository[DoctorSchedule]):

    @abstractmethod
    def get_by_doctor(self, doctor_id: UUID) -> list[DoctorSchedule]:
        raise NotImplementedError

    @abstractmethod
    def get_by_doctor_and_day(self, doctor_id: UUID, day_of_week: int) -> list[DoctorSchedule]:
        raise   