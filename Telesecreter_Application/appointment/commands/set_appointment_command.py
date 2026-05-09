from datetime import date, datetime, time, timedelta
from uuid import UUID

from Telesecreter_Domain.entities.appointments import Appointment
from Telesecreter_Domain.enums.appointment_status import AppointmentStatus
from Telesecreter_Domain.interfaces.i_appointment_repository import IAppointmentRepository
from Telesecreter_Application.appointment.dtos.set_appointment_dto import SetAppointmentResponse

_SLOT_DURATION = timedelta(minutes=30)


class SetAppointmentCommand:

    def __init__(self, appointment_repo: IAppointmentRepository):
        self._appointment_repo = appointment_repo

    def execute(
        self,
        doctor_id: UUID,
        user_id: UUID,
        target_date: date,
        start_time: time,
    ) -> SetAppointmentResponse:
        end_time = (datetime.combine(target_date, start_time) + _SLOT_DURATION).time()
        appointment = Appointment(
            doctor_id=doctor_id,
            user_id=user_id,
            date=target_date,
            start_time=start_time,
            end_time=end_time,
            status=AppointmentStatus.CONFIRMED,
        )
        self._appointment_repo.add(appointment)
        return SetAppointmentResponse.from_entity(appointment)
