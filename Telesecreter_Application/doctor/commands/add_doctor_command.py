from Telesecreter_Domain.entities.doctor import Doctor
from Telesecreter_Domain.interfaces.i_doctor_repository import IDoctorRepository
from Telesecreter_Application.doctor.dtos.add_doctor_dto import AddDoctorRequest
from Telesecreter_Application.doctor.dtos.doctor_dto import DoctorDTO


class AddDoctorCommand:

    def __init__(self, doctor_repo: IDoctorRepository):
        self._doctor_repo = doctor_repo

    def execute(self, request: AddDoctorRequest) -> DoctorDTO:
        doctor = Doctor(
            full_name=request.full_name,
            email=request.email,
            department_id=request.department_id,
            specialty=request.specialty,
            phone_number=request.phone_number,
            ratings=request.ratings,
            is_available=request.is_available,
        )
        self._doctor_repo.add(doctor)
        return DoctorDTO.from_entity(doctor)
