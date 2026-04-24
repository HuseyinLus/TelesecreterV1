from uuid import UUID
from datetime import datetime
from Telesecreter_Domain.common.base_entity import BaseEntity


class Department(BaseEntity):
    def __init__(
        self,
        name: str,
        id: UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(id, created_at, updated_at)
        self.name = name
