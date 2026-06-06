from uuid import UUID
from Telesecreter_Domain.interfaces.i_department_repository import IDepartmentRepository
from Telesecreter_Application.department.commands.update_department_command import DepartmentNotFoundException


class DeleteDepartmentCommand:

    def __init__(self, department_repo: IDepartmentRepository):
        self._department_repo = department_repo

    def execute(self, department_id: UUID) -> None:
        if self._department_repo.get_by_id(department_id) is None:
            raise DepartmentNotFoundException(department_id)
        self._department_repo.delete(department_id)
