from typing import Optional
from uuid import UUID

from Telesecreter_Domain.interfaces.i_department_repository import IDepartmentRepository
from Telesecreter_Domain.entities.department import Department
from Telesecreter_Infrastructure.data_access.configurations.models.department_model import DepartmentModel
from Telesecreter_Infrastructure.data_access.repositories.repository import GenericRepository
from Telesecreter_Infrastructure.data_access.db.database import get_db


def _map(row: DepartmentModel) -> Department:
    return Department(
        id=UUID(row.id),
        name=row.name,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


class DepartmentRepository(GenericRepository[Department, DepartmentModel], IDepartmentRepository):

    def __init__(self):
        super().__init__(DepartmentModel, _map)

    def add(self, entity: Department) -> Department:
        model = DepartmentModel(
            id=str(entity.id),
            name=entity.name,
        )
        with get_db() as session:
            session.add(model)
        return entity

    def update(self, entity: Department) -> Department:
        with get_db() as session:
            model = session.get(DepartmentModel, str(entity.id))
            if model is None:
                raise ValueError(f"Department {entity.id} not found")
            model.name = entity.name
        return entity

    def get_by_name(self, name: str) -> Optional[Department]:
        with get_db() as session:
            row = session.query(DepartmentModel).filter(DepartmentModel.name == name).first()
            return _map(row) if row else None