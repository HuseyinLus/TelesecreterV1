from uuid import UUID
from typing import Optional
from Telesecreter_Domain.common.base_entity import BaseEntity


class Doctor(BaseEntity):
    def __init__(
        self,
        full_name: str,
        email: str,
        department_id: UUID,
        specialty: str,
        phone_number: str = "",
        ratings: Optional[float] = None,
        years_of_experience: int = 0,
        bio: Optional[str] = None,
        is_available: bool = True,
        id: UUID | None = None,
    ):
        super().__init__(id)
        ratings = ratings if ratings is not None else 0.0
        self.full_name = full_name
        self.email = email
        self.phone_number = phone_number
        self.department_id = department_id
        self.specialty = specialty
        self.is_available = is_available