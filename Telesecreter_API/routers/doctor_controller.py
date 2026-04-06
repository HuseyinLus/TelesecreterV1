from fastapi import APIRouter, Depends

from Telesecreter_Domain.interfaces.i_doctor_repository import IDoctorRepository
from Telesecreter_Application.doctor.dtos.doctor_dto import DoctorDTO
from Telesecreter_Application.doctor.queries.get_all_doctors_query import GetAllDoctorsQuery
from Telesecreter_API.dependencies.dependency_injection import get_doctor_repo

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.get("/", response_model=list[DoctorDTO])
def get_all_doctors(repo: IDoctorRepository = Depends(get_doctor_repo)):
    return GetAllDoctorsQuery(repo).execute()