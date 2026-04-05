from abc import abstractmethod
from typing import Optional
from Telesecreter_Domain.interfaces.i_base_repository import IBaseRepository
from Telesecreter_Domain.entities.department import Department


class IDepartmentRepository(IBaseRepository[Department]):

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Department]:
        raise NotImplementedError