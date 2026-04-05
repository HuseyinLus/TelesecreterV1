from abc import abstractmethod
from typing import Optional
from uuid import UUID
from Telesecreter_Domain.interfaces.i_base_repository import IBaseRepository
from Telesecreter_Domain.entities.user import User


class IUserRepository(IBaseRepository[User]):

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_by_phone(self, phone_number: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_active_users(self) -> list[User]:
        raise NotImplementedError