from Telesecreter_Domain.interfaces.i_doctor_repository import IDoctorRepository
from Telesecreter_Application.doctor.dtos.get_doctor_by_name_dto import GetDoctorByNameDTO
from Telesecreter_Application.doctor.Exceptions.doctor_exception_handlers import DoctorNotFoundError


class GetDoctorByNameQuery:

    def __init__(self, doctor_repository: IDoctorRepository):
        self._repository = doctor_repository

    def execute(self, name: str) -> list[GetDoctorByNameDTO]:
        doctors = self._repository.get_by_name(name.strip())
        if not doctors:
            raise DoctorNotFoundError(f"name='{name}'")
        return [GetDoctorByNameDTO.from_entity(doctor) for doctor in doctors]
