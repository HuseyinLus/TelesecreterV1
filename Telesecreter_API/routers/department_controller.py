from fastapi import APIRouter, Depends

from Telesecreter_Domain.interfaces.i_department_repository import IDepartmentRepository
from Telesecreter_Application.department.dtos import department_dto
from Telesecreter_Application.department.queries.get_all_departments_query import GetAllDepartmentsQuery
from Telesecreter_API.dependencies.dependency_injection import get_department_repo

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.get("/", response_model=list[department_dto.DepartmentDTO])
def get_all_departments(repo: IDepartmentRepository = Depends(get_department_repo)):
    return GetAllDepartmentsQuery(repo).execute()