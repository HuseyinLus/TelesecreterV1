from uuid import UUID
from Telesecreter_Domain.interfaces.i_department_repository import IDepartmentRepository
from Telesecreter_Application.department.dtos.update_department_dto import UpdateDepartmentRequest
from Telesecreter_Application.department.dtos.department_dto import DepartmentDTO


class DepartmentNotFoundException(Exception):
    def __init__(self, department_id: UUID):
        super().__init__(f"Department with id '{department_id}' not found.")
        self.department_id = department_id


class UpdateDepartmentCommand:

    def __init__(self, department_repo: IDepartmentRepository):
        self._department_repo = department_repo

    def execute(self, department_id: UUID, request: UpdateDepartmentRequest) -> DepartmentDTO:
        department = self._department_repo.get_by_id(department_id)
        if department is None:
            raise DepartmentNotFoundException(department_id)

        department.name = request.name
        self._department_repo.update(department)
        return DepartmentDTO.from_entity(department)
