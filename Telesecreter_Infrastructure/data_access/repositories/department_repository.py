from typing import Optional
from Telesecreter_Domain.interfaces.i_department_repository import IDepartmentRepository
from Telesecreter_Domain.entities.department import Department
from Telesecreter_Infrastructure.data_access.configurations.models.department_model import DepartmentModel
from Telesecreter_Infrastructure.data_access.repositories.repository import GenericRepository
from Telesecreter_Infrastructure.data_access.db.database import get_db


def _map(row) -> Department:
    return Department(
        id=row["id"],
        name=row["name"],
    )


class DepartmentRepository(GenericRepository[Department, DepartmentModel], IDepartmentRepository):

    def __init__(self):
        super().__init__(DepartmentModel, _map)

    def get_by_name(self, name: str) -> Optional[Department]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM departments WHERE name = ?", (name,)).fetchone()
            return _map(row) if row else None