from abc import abstractmethod
from datetime import date
from uuid import UUID
from Telesecreter_Domain.interfaces.i_base_repository import IBaseRepository
from Telesecreter_Domain.entities.appointments import Appointment
from Telesecreter_Domain.enums.appointment_status import AppointmentStatus


class IAppointmentRepository(IBaseRepository[Appointment]):

    @abstractmethod
    def get_by_user(self, user_id: UUID) -> list[Appointment]:
        raise NotImplementedError

    @abstractmethod
    def get_by_doctor(self, doctor_id: UUID) -> list[Appointment]:
        raise NotImplementedError

    @abstractmethod
    def get_by_doctor_and_date(self, doctor_id: UUID, date: date) -> list[Appointment]:
        raise NotImplementedError

    @abstractmethod
    def get_by_status(self, status: AppointmentStatus) -> list[Appointment]:
        raise NotImplementedError