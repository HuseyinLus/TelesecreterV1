from uuid import UUID
from Telesecreter_Domain.interfaces.i_doctor_repository import IDoctorRepository
from Telesecreter_Application.doctor.dtos.update_doctor_dto import UpdateDoctorRequest
from Telesecreter_Application.doctor.dtos.doctor_dto import DoctorDTO
from Telesecreter_Application.doctor.Exceptions.doctor_exception_handlers import DoctorNotFoundError


class UpdateDoctorCommand:

    def __init__(self, doctor_repo: IDoctorRepository):
        self._doctor_repo = doctor_repo

    def execute(self, doctor_id: UUID, request: UpdateDoctorRequest) -> DoctorDTO:
        doctor = self._doctor_repo.get_by_id(doctor_id)
        if doctor is None:
            raise DoctorNotFoundError(str(doctor_id))

        if request.full_name is not None:
            doctor.full_name = request.full_name
        if request.email is not None:
            doctor.email = request.email
        if request.department_id is not None:
            doctor.department_id = request.department_id
        if request.specialty is not None:
            doctor.specialty = request.specialty
        if request.phone_number is not None:
            doctor.phone_number = request.phone_number
        if request.ratings is not None:
            doctor.ratings = request.ratings
        if request.is_available is not None:
            doctor.is_available = request.is_available

        self._doctor_repo.update(doctor)
        return DoctorDTO.from_entity(doctor)
