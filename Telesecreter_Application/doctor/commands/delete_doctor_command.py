from uuid import UUID
from Telesecreter_Domain.interfaces.i_doctor_repository import IDoctorRepository
from Telesecreter_Application.doctor.Exceptions.doctor_exception_handlers import DoctorNotFoundError


class DeleteDoctorCommand:

    def __init__(self, doctor_repo: IDoctorRepository):
        self._doctor_repo = doctor_repo

    def execute(self, doctor_id: UUID) -> None:
        if self._doctor_repo.get_by_id(doctor_id) is None:
            raise DoctorNotFoundError(str(doctor_id))
        self._doctor_repo.delete(doctor_id)
