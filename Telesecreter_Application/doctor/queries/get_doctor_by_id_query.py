from uuid import UUID

from Telesecreter_Domain.interfaces.i_doctor_repository import IDoctorRepository
from Telesecreter_Application.doctor.dtos.get_doctor_by_id_dto import GetDoctorByIdDTO
from Telesecreter_Application.doctor.Exceptions.doctor_exception_handlers import DoctorNotFoundError


class GetDoctorByIdQuery:

    def __init__(self, doctor_repository: IDoctorRepository):
        self._repository = doctor_repository

    def execute(self, doctor_id: UUID) -> GetDoctorByIdDTO:
        doctor = self._repository.get_by_id(doctor_id)
        if doctor is None:
            raise DoctorNotFoundError(f"id={doctor_id}")
        return GetDoctorByIdDTO.from_entity(doctor)
