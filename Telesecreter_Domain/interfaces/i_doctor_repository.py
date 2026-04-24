from abc import abstractmethod
from typing import Optional
from uuid import UUID
from Telesecreter_Domain.interfaces.i_base_repository import IBaseRepository
from Telesecreter_Domain.entities.doctor import Doctor


class IDoctorRepository(IBaseRepository[Doctor]):

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Doctor]:
        raise NotImplementedError

    @abstractmethod
    def get_by_department(self, department_id: UUID) -> list[Doctor]:
        raise NotImplementedError

    @abstractmethod
    def get_available_doctors(self) -> list[Doctor]:
        raise NotImplementedError

    @abstractmethod
    def get_by_name(self, name: str) -> list[Doctor]:
        raise NotImplementedError