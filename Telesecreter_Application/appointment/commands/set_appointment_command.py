from datetime import date, datetime, time, timedelta
from uuid import UUID

from Telesecreter_Domain.entities.appointments import Appointment
from Telesecreter_Domain.enums.appointment_status import AppointmentStatus
from Telesecreter_Domain.interfaces.i_appointment_repository import IAppointmentRepository
from Telesecreter_Domain.interfaces.i_doctor_repository import IDoctorRepository
from Telesecreter_Domain.interfaces.i_scheduale_repository import IScheduleRepository
from Telesecreter_Application.appointment.dtos.set_appointment_dto import SetAppointmentResponse
from Telesecreter_Application.appointment.Exceptions.appointment_exception_handlers import (
    DoctorNotAvailableAtTimeError,
    DoctorNotAvailableError,
    DoctorNotFoundError,
)

_SLOT_DURATION = timedelta(minutes=30)
_ACTIVE_STATUSES = {AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED}


class SetAppointmentCommand:

    def __init__(
        self,
        doctor_repo: IDoctorRepository,
        schedule_repo: IScheduleRepository,
        appointment_repo: IAppointmentRepository,
    ):
        self._doctor_repo = doctor_repo
        self._schedule_repo = schedule_repo
        self._appointment_repo = appointment_repo

    def execute(
        self,
        doctor_id: UUID,
        user_id: UUID,
        target_date: date,
        start_time: time,
    ) -> SetAppointmentResponse:

        # 1. Doctor must exist
        if not self._doctor_repo.get_by_id(doctor_id):
            raise DoctorNotFoundError(doctor_id)

        # 2. Doctor must work on that weekday
        schedules = self._schedule_repo.get_by_doctor_and_day(doctor_id, target_date.weekday())
        if not schedules:
            raise DoctorNotAvailableError()

        # 3. Requested time slot must not be already booked
        existing = self._appointment_repo.get_by_doctor_and_date(doctor_id, target_date)
        booked_start_times = {
            a.start_time for a in existing
            if a.status in _ACTIVE_STATUSES
        }
        if start_time in booked_start_times:
            raise DoctorNotAvailableAtTimeError()

        # 4. Build and persist the appointment
        end_time = (datetime.combine(target_date, start_time) + _SLOT_DURATION).time()
        appointment = Appointment(
            doctor_id=doctor_id,
            user_id=user_id,
            date=target_date,
            start_time=start_time,
            end_time=end_time,
            status=AppointmentStatus.PENDING,
        )
        self._appointment_repo.add(appointment)

        return SetAppointmentResponse.from_entity(appointment)
