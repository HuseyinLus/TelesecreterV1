from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from Telesecreter_Domain.interfaces.i_doctor_repository import IDoctorRepository
from Telesecreter_Application.doctor.dtos.doctor_dto import DoctorDTO
from Telesecreter_Application.doctor.dtos.get_doctor_by_id_dto import GetDoctorByIdDTO
from Telesecreter_Application.doctor.dtos.get_doctor_by_name_dto import GetDoctorByNameDTO
from Telesecreter_Application.doctor.dtos.add_doctor_dto import AddDoctorRequest
from Telesecreter_Application.doctor.dtos.update_doctor_dto import UpdateDoctorRequest
from Telesecreter_Application.doctor.queries.get_all_doctors_query import GetAllDoctorsQuery
from Telesecreter_Application.doctor.queries.get_doctor_by_id_query import GetDoctorByIdQuery
from Telesecreter_Application.doctor.queries.get_doctor_by_name_query import GetDoctorByNameQuery
from Telesecreter_Application.doctor.commands.add_doctor_command import AddDoctorCommand
from Telesecreter_Application.doctor.commands.update_doctor_command import UpdateDoctorCommand
from Telesecreter_Application.doctor.commands.delete_doctor_command import DeleteDoctorCommand
from Telesecreter_Application.doctor.Exceptions.doctor_exception_handlers import DoctorNotFoundError
from Telesecreter_API.dependencies.dependency_injection import get_doctor_repo

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.get("/", response_model=list[DoctorDTO])
def get_all_doctors(repo: IDoctorRepository = Depends(get_doctor_repo)):
    return GetAllDoctorsQuery(repo).execute()


@router.get("/search", response_model=list[GetDoctorByNameDTO])
def get_doctor_by_name(name: str, repo: IDoctorRepository = Depends(get_doctor_repo)):
    try:
        return GetDoctorByNameQuery(repo).execute(name)
    except DoctorNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{doctor_id}", response_model=GetDoctorByIdDTO)
def get_doctor_by_id(doctor_id: UUID, repo: IDoctorRepository = Depends(get_doctor_repo)):
    try:
        return GetDoctorByIdQuery(repo).execute(doctor_id)
    except DoctorNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=DoctorDTO, status_code=201)
def add_doctor(request: AddDoctorRequest, repo: IDoctorRepository = Depends(get_doctor_repo)):
    return AddDoctorCommand(repo).execute(request)


@router.put("/{doctor_id}", response_model=DoctorDTO)
def update_doctor(doctor_id: UUID, request: UpdateDoctorRequest, repo: IDoctorRepository = Depends(get_doctor_repo)):
    try:
        return UpdateDoctorCommand(repo).execute(doctor_id, request)
    except DoctorNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{doctor_id}", status_code=204)
def delete_doctor(doctor_id: UUID, repo: IDoctorRepository = Depends(get_doctor_repo)):
    try:
        DeleteDoctorCommand(repo).execute(doctor_id)
    except DoctorNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))