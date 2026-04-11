from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from Telesecreter_Domain.interfaces.i_appointment_repository import IAppointmentRepository
from Telesecreter_Domain.interfaces.i_doctor_repository import IDoctorRepository
from Telesecreter_Domain.interfaces.i_scheduale_repository import IScheduleRepository
from Telesecreter_Application.appointment.dtos.appointment_dto import AppointmentDTO
from Telesecreter_Application.appointment.dtos.availability_dto import DoctorAvailabilityDTO
from Telesecreter_Application.appointment.dtos.get_appointment_by_doctor_id_dto import GetAppointmentByDoctorIdDTO
from Telesecreter_Application.appointment.dtos.set_appointment_dto import SetAppointmentRequest, SetAppointmentResponse
from Telesecreter_Application.appointment.queries.get_all_appointmens_query import GetAllAppointmentsQuery
from Telesecreter_Application.appointment.queries.check_doctor_availability_query import CheckDoctorAvailabilityQuery
from Telesecreter_Application.appointment.queries.get_appointment_by_doctor_id_query import GetAppointmentByDoctorIdQuery
from Telesecreter_Application.appointment.commands.set_appointment_command import SetAppointmentCommand
from Telesecreter_Application.appointment.Exceptions.appointment_exception_handlers import (
    DoctorNotAvailableAtTimeError,
    DoctorNotAvailableError,
    DoctorNotFoundError,
    PastDateError,
)
from Telesecreter_API.dependencies.dependency_injection import get_appointment_repo, get_doctor_repo, get_schedule_repo

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.get("/", response_model=list[AppointmentDTO])
def get_all_appointments(repo: IAppointmentRepository = Depends(get_appointment_repo)):
    return GetAllAppointmentsQuery(repo).execute()


@router.post("/set", response_model=SetAppointmentResponse, status_code=201)
def set_appointment(
    request: SetAppointmentRequest,
    appointment_repo: IAppointmentRepository = Depends(get_appointment_repo),
    schedule_repo: IScheduleRepository = Depends(get_schedule_repo),
    doctor_repo: IDoctorRepository = Depends(get_doctor_repo),
):
    try:
        return SetAppointmentCommand(doctor_repo, schedule_repo, appointment_repo).execute(
            doctor_id=request.doctor_id,
            user_id=request.user_id,
            target_date=request.date,
            start_time=request.start_time,
        )
    except DoctorNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DoctorNotAvailableError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DoctorNotAvailableAtTimeError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/doctor/{doctor_id}", response_model=list[GetAppointmentByDoctorIdDTO])
def get_appointments_by_doctor_id(
    doctor_id: UUID,
    appointment_repo: IAppointmentRepository = Depends(get_appointment_repo),
    doctor_repo: IDoctorRepository = Depends(get_doctor_repo),
):
    try:
        return GetAppointmentByDoctorIdQuery(appointment_repo, doctor_repo).execute(doctor_id)
    except DoctorNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/availability", response_model=DoctorAvailabilityDTO)
def check_availability(
    doctor_id: UUID,
    date: date,
    appointment_repo: IAppointmentRepository = Depends(get_appointment_repo),
    schedule_repo: IScheduleRepository = Depends(get_schedule_repo),
    doctor_repo: IDoctorRepository = Depends(get_doctor_repo),
):
    try:
        return CheckDoctorAvailabilityQuery(schedule_repo, appointment_repo, doctor_repo).execute(doctor_id, date)
    except PastDateError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (DoctorNotFoundError, DoctorNotAvailableError) as e:
        raise HTTPException(status_code=404, detail=str(e))