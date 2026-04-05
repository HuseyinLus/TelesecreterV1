from Telesecreter_Domain.common.base_entity import BaseEntity
from uuid import UUID
 
 
class Department(BaseEntity):
    def __init__(
        self,
        name: str,
        id: UUID | None = None,
    ):
        super().__init__(id)
        self.name = name
