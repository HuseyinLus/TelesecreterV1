from Telesecreter_Domain.interfaces.i_doctor_repository import IDoctorRepository
from Telesecreter_Application.doctor.dtos.doctor_dto import DoctorDTO

class GetAllDoctorsQuery:

    def __init__(self,doctor_repository: IDoctorRepository):
        self._repository = doctor_repository

    def excecute(self) -> list[DoctorDTO]:
        doctors = self._repository.get_all()
        return [DoctorDTO.from_entity(doctor) for doctor in doctors]