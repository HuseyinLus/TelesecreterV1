from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from Telesecreter_Domain.interfaces.i_department_repository import IDepartmentRepository
from Telesecreter_Application.department.dtos.department_dto import DepartmentDTO
from Telesecreter_Application.department.dtos.add_department_dto import AddDepartmentRequest
from Telesecreter_Application.department.dtos.update_department_dto import UpdateDepartmentRequest
from Telesecreter_Application.department.queries.get_all_departments_query import GetAllDepartmentsQuery
from Telesecreter_Application.department.commands.add_department_command import AddDepartmentCommand
from Telesecreter_Application.department.commands.update_department_command import UpdateDepartmentCommand, DepartmentNotFoundException
from Telesecreter_Application.department.commands.delete_department_command import DeleteDepartmentCommand
from Telesecreter_API.dependencies.dependency_injection import get_department_repo

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("/", response_model=list[DepartmentDTO])
def get_all_departments(repo: IDepartmentRepository = Depends(get_department_repo)):
    return GetAllDepartmentsQuery(repo).execute()


@router.post("/", response_model=DepartmentDTO, status_code=201)
def add_department(request: AddDepartmentRequest, repo: IDepartmentRepository = Depends(get_department_repo)):
    return AddDepartmentCommand(repo).execute(request)


@router.put("/{department_id}", response_model=DepartmentDTO)
def update_department(department_id: UUID, request: UpdateDepartmentRequest, repo: IDepartmentRepository = Depends(get_department_repo)):
    try:
        return UpdateDepartmentCommand(repo).execute(department_id, request)
    except DepartmentNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{department_id}", status_code=204)
def delete_department(department_id: UUID, repo: IDepartmentRepository = Depends(get_department_repo)):
    try:
        DeleteDepartmentCommand(repo).execute(department_id)
    except DepartmentNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))