from Telesecreter_Domain.interfaces.i_department_repository import IDepartmentRepository
from Telesecreter_Application.department.dtos.department_dto import DepartmentDTO


class GetAllDepartmentsQuery:

    def __init__(self, department_repository: IDepartmentRepository):
        self._repository = department_repository

    def excecute(self) -> list[DepartmentDTO]:
        departments = self._repository.get_all()
        return [DepartmentDTO.from_entity(department) for department in departments]
