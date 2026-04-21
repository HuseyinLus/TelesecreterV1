from uuid import UUID

from Telesecreter_Domain.interfaces.i_appointment_repository import IAppointmentRepository
from Telesecreter_Domain.interfaces.i_doctor_repository import IDoctorRepository
from Telesecreter_Application.appointment.dtos.get_appointment_by_doctor_id_dto import GetAppointmentByDoctorIdDTO
from Telesecreter_Application.appointment.exceptions.appointment_exception_handlers import DoctorNotFoundError


class GetAppointmentByDoctorIdQuery:

    def __init__(
        self,
        appointment_repository: IAppointmentRepository,
        doctor_repository: IDoctorRepository,
    ):
        self._repository = appointment_repository
        self._doctor_repository = doctor_repository

    def execute(self, doctor_id: UUID) -> list[GetAppointmentByDoctorIdDTO]:
        if not self._doctor_repository.get_by_id(doctor_id):
            raise DoctorNotFoundError(doctor_id)

        appointments = self._repository.get_by_doctor(doctor_id)
        return [GetAppointmentByDoctorIdDTO.from_entity(a) for a in appointments]
