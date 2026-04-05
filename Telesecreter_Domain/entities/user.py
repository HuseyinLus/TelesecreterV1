from uuid import UUID
from Telesecreter_Domain.common.base_entity import BaseEntity
from Telesecreter_Domain.enums.user_role import UserRole

class User(BaseEntity):
    def __init__(
        self,
        full_name: str,
        phone_number: str,
        email: str,
        hashed_password: str,
        role: UserRole = UserRole.PATIENT,
        is_active: bool = True,
        id: UUID | None = None,
    ):
        super().__init__(id)
        self.full_name = full_name
        self.phone_number = phone_number
        self.email = email
        self.hashed_password = hashed_password
        self.role = role
        self.is_active = is_active