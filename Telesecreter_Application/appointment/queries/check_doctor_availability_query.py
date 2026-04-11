from datetime import date, datetime, timedelta
from uuid import UUID

from Telesecreter_Domain.enums.appointment_status import AppointmentStatus
from Telesecreter_Domain.interfaces.i_appointment_repository import IAppointmentRepository
from Telesecreter_Domain.interfaces.i_doctor_repository import IDoctorRepository
from Telesecreter_Domain.interfaces.i_scheduale_repository import IScheduleRepository
from Telesecreter_Application.appointment.dtos.availability_dto import AvailableSlotDTO, DoctorAvailabilityDTO
from Telesecreter_Application.appointment.Exceptions.appointment_exception_handlers import DoctorNotAvailableError, DoctorNotFoundError, PastDateError

_SLOT_MINUTES = 30
_SLOT_DELTA = timedelta(minutes=_SLOT_MINUTES)

# Statuses that still occupy a slot
_ACTIVE_STATUSES = {
    AppointmentStatus.PENDING,
    AppointmentStatus.CONFIRMED,
}


class CheckDoctorAvailabilityQuery:

    def __init__(
        self,
        schedule_repo: IScheduleRepository,
        appointment_repo: IAppointmentRepository,
        doctor_repo: IDoctorRepository,
    ):
        self._schedule_repo = schedule_repo
        self._appointment_repo = appointment_repo
        self._doctor_repo = doctor_repo

    def execute(self, doctor_id: UUID, target_date: date) -> DoctorAvailabilityDTO:
        if not self._doctor_repo.get_by_id(doctor_id):
            raise DoctorNotFoundError(doctor_id)

        if target_date < date.today():
            raise PastDateError()

        # DB stores day_of_week as 0=Monday … 6=Sunday (matches Python weekday())
        schedules = self._schedule_repo.get_by_doctor_and_day(
            doctor_id, target_date.weekday()
        )
        if not schedules:
            raise DoctorNotAvailableError()

        schedule = schedules[0]  # unique constraint: one row per doctor per day

        booked = self._appointment_repo.get_by_doctor_and_date(doctor_id, target_date)
        booked_windows = {
            (a.start_time, a.end_time)
            for a in booked
            if a.status in _ACTIVE_STATUSES
        }

        slots = []
        cursor = datetime.combine(target_date, schedule.start_time)
        work_end = datetime.combine(target_date, schedule.end_time)

        while cursor + _SLOT_DELTA <= work_end:
            slot_end = cursor + _SLOT_DELTA
            if (cursor.time(), slot_end.time()) not in booked_windows:
                slots.append(AvailableSlotDTO(
                    start_time=cursor.time(),
                    end_time=slot_end.time(),
                ))
            cursor = slot_end

        return DoctorAvailabilityDTO(
            doctor_id=doctor_id,
            date=target_date,
            available_slots=slots,
        )
