from dataclasses import dataclass
from uuid import UUID


@dataclass
class GetUserByPhoneDTO:
    id: UUID
    full_name: str
    phone_number: str
    is_registered: bool

    @staticmethod
    def from_entity(user) -> "GetUserByPhoneDTO":
        return GetUserByPhoneDTO(
            id=user.id,
            full_name=user.full_name,
            phone_number=user.phone_number,
            is_registered=True,
        )
