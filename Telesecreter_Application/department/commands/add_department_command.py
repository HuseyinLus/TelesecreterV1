from Telesecreter_Domain.entities.department import Department
from Telesecreter_Domain.interfaces.i_department_repository import IDepartmentRepository
from Telesecreter_Application.department.dtos.add_department_dto import AddDepartmentRequest
from Telesecreter_Application.department.dtos.department_dto import DepartmentDTO


class AddDepartmentCommand:

    def __init__(self, department_repo: IDepartmentRepository):
        self._department_repo = department_repo

    def execute(self, request: AddDepartmentRequest) -> DepartmentDTO:
        department = Department(name=request.name)
        self._department_repo.add(department)
        return DepartmentDTO.from_entity(department)
