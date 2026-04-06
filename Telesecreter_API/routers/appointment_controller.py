from fastapi import APIRouter, Depends

from Telesecreter_Domain.interfaces.i_appointment_repository import IAppointmentRepository
from Telesecreter_Application.appointment.dtos.appointment_dto import AppointmentDTO
from Telesecreter_Application.appointment.queries.get_all_appointmens_query import GetAllAppointmentsQuery
from Telesecreter_API.dependencies.dependency_injection import get_appointment_repo 

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.get("/", response_model=list[AppointmentDTO])
def get_all_appointments(repo:IAppointmentRepository = Depends(get_appointment_repo)):
    return GetAllAppointmentsQuery(repo).execute()