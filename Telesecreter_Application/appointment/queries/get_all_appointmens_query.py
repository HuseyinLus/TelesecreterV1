from Telesecreter_Domain.interfaces.i_appointment_repository import IAppointmentRepository
from Telesecreter_Application.appointment.dtos.appointment_dto import AppointmentDTO

class GetAllAppointmentsQuery:

    def __init__(self, appointment_repository: IAppointmentRepository):
        self._repository = appointment_repository

    def execute(self) -> list[AppointmentDTO]:
        appointments = self._repository.get_all()
        return [AppointmentDTO.from_entity(appointment) for appointment in appointments ]