from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class UserDTO:
    id: UUID
    full_name: str
    phone_number: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(user) -> "UserDTO":
        return UserDTO(
            id=user.id,
            full_name=user.full_name,
            phone_number=user.phone_number,
            email=user.email,
            role=user.role.value,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )