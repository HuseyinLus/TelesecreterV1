from Telesecreter_Infrastructure.data_access.repositories.user_repository import UserRepository
from Telesecreter_Infrastructure.data_access.repositories.doctor_repository import DoctorRepository
from Telesecreter_Infrastructure.data_access.repositories.department_repository import DepartmentRepository
from Telesecreter_Infrastructure.data_access.repositories.appointment_repository import AppointmentRepository
from Telesecreter_Infrastructure.data_access.repositories.scheduale_repository import ScheduleRepository

from Telesecreter_Domain.interfaces.i_user_repository import IUserRepository
from Telesecreter_Domain.interfaces.i_doctor_repository import IDoctorRepository
from Telesecreter_Domain.interfaces.i_department_repository import IDepartmentRepository
from Telesecreter_Domain.interfaces.i_appointment_repository import IAppointmentRepository
from Telesecreter_Domain.interfaces.i_scheduale_repository import IScheduleRepository


def get_user_repo() -> IUserRepository:
    return UserRepository()


def get_doctor_repo() -> IDoctorRepository:
    return DoctorRepository()


def get_department_repo() -> IDepartmentRepository:
    return DepartmentRepository()


def get_appointment_repo() -> IAppointmentRepository:
    return AppointmentRepository()


def get_schedule_repo() -> IScheduleRepository:
    return ScheduleRepository()