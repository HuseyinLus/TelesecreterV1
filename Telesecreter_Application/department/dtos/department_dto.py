from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class DepartmentDTO:
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime
    
    @staticmethod
    def from_entity(department) -> "DepartmentDTO":
        return DepartmentDTO(
            id=department.id,
            name=department.name,
            created_at=department.created_at,
            updated_at=department.updated_at,
        )