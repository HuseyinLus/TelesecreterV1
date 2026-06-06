from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from Telesecreter_Domain.interfaces.i_appointment_repository import IAppointmentRepository
from Telesecreter_Domain.interfaces.i_doctor_repository import IDoctorRepository
from Telesecreter_Application.appointment.dtos.appointment_dto import AppointmentDTO
from Telesecreter_Application.appointment.dtos.get_appointment_by_doctor_id_dto import GetAppointmentByDoctorIdDTO
from Telesecreter_Application.appointment.dtos.set_appointment_dto import SetAppointmentRequest, SetAppointmentResponse
from Telesecreter_Application.appointment.queries.get_all_appointmens_query import GetAllAppointmentsQuery
from Telesecreter_Application.appointment.queries.get_appointment_by_doctor_id_query import GetAppointmentByDoctorIdQuery
from Telesecreter_Application.appointment.queries.check_slot_availability_query import CheckSlotAvailabilityQuery
from Telesecreter_Application.appointment.commands.set_appointment_command import SetAppointmentCommand
from Telesecreter_Application.appointment.dtos.cancel_appointment_dto import CancelAppointmentRequest
from Telesecreter_Application.appointment.commands.cancel_appointment_command import CancelAppointmentCommand
from Telesecreter_Application.appointment.commands.delete_appointment_command import DeleteAppointmentCommand
from Telesecreter_Application.appointment.exceptions.appointment_exception_handlers import DoctorNotFoundError, AppointmentNotFoundError
from Telesecreter_Application.doctor.Exceptions.doctor_exception_handlers import InvalidTimeFormatError
from Telesecreter_API.dependencies.dependency_injection import get_appointment_repo, get_doctor_repo

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.get("/", response_model=list[AppointmentDTO])
def get_all_appointments(repo: IAppointmentRepository = Depends(get_appointment_repo)):
    return GetAllAppointmentsQuery(repo).execute()


@router.post("/set", response_model=SetAppointmentResponse, status_code=201)
def set_appointment(
    request: SetAppointmentRequest,
    appointment_repo: IAppointmentRepository = Depends(get_appointment_repo),
):
    try:
        return SetAppointmentCommand(appointment_repo).execute(
            doctor_id=request.args.doctor_id,
            user_id=request.args.user_id,
            target_date=request.args.date,
            start_time=request.args.start_time,
        )
    except IntegrityError:
        raise HTTPException(status_code=409, detail="This time slot is already booked for the selected doctor.")


@router.get("/slots/check")
def check_slot_availability(
    doctor_id: UUID,
    date_str: str,
    requested_time: str,
    appointment_repo: IAppointmentRepository = Depends(get_appointment_repo),
):
    try:
        is_available = CheckSlotAvailabilityQuery(appointment_repo).execute(
            doctor_id, date_str, requested_time
        )
        return {"is_slot_available": is_available}
    except InvalidTimeFormatError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{appointment_id}/cancel", response_model=AppointmentDTO)
def cancel_appointment(
    appointment_id: UUID,
    request: CancelAppointmentRequest,
    appointment_repo: IAppointmentRepository = Depends(get_appointment_repo),
):
    try:
        return CancelAppointmentCommand(appointment_repo).execute(appointment_id, request)
    except AppointmentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{appointment_id}", status_code=204)
def delete_appointment(
    appointment_id: UUID,
    appointment_repo: IAppointmentRepository = Depends(get_appointment_repo),
):
    try:
        DeleteAppointmentCommand(appointment_repo).execute(appointment_id)
    except AppointmentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


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
