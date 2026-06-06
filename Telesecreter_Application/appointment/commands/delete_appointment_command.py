from uuid import UUID
from Telesecreter_Domain.interfaces.i_appointment_repository import IAppointmentRepository
from Telesecreter_Application.appointment.exceptions.appointment_exception_handlers import AppointmentNotFoundError


class DeleteAppointmentCommand:

    def __init__(self, appointment_repo: IAppointmentRepository):
        self._appointment_repo = appointment_repo

    def execute(self, appointment_id: UUID) -> None:
        if self._appointment_repo.get_by_id(appointment_id) is None:
            raise AppointmentNotFoundError(appointment_id)
        self._appointment_repo.delete(appointment_id)
