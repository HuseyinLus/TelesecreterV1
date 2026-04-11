# Files

## File: CLAUDE.md
````markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server
uvicorn Telesecreter_API.main:app --reload

# Run with specific host/port
uvicorn Telesecreter_API.main:app --reload --host 0.0.0.0 --port 8000

# Database migrations
alembic upgrade head        # Apply all migrations
alembic revision --autogenerate -m "description"  # Generate new migration

# Seed the database with sample data
python Telesecreter_Infrastructure/seeds/db_seeds.py
```

No test framework is configured yet. The interactive API docs are available at `http://localhost:8000/docs`.

## Architecture

This is a **Python FastAPI** telemedicine appointment management backend, organized in **Clean Architecture** layers:

```
Telesecreter_API/           → Presentation: FastAPI routers, dependency injection
Telesecreter_Application/   → Application: CQRS-style queries/commands, DTOs
Telesecreter_Domain/        → Domain: entities, interfaces (repository contracts), enums
Telesecreter_Infrastructure/ → Infrastructure: SQLAlchemy ORM models, repository implementations, Alembic migrations
```

### Request Flow

```
Router (controller) → Query/Command class → IRepository interface → Repository implementation → SQLite DB
```

Dependency injection is configured in `Telesecreter_API/dependencies/` and wired via FastAPI's `Depends()`.

### Key Patterns

- **Repository Pattern**: Domain layer defines abstract interfaces (`IUserRepository`, `IDoctorRepository`, etc.); infrastructure layer provides SQLAlchemy implementations.
- **CQRS-style**: Business logic lives in query classes (e.g., `GetAllDoctorsQuery`) under `Telesecreter_Application/`, not in routers.
- **DTOs**: Each application module has DTOs for API responses, separate from domain entities and ORM models.
- **Mapper layer**: Converts between SQLAlchemy ORM models and domain entities.
- **Generic base repository**: `Telesecreter_Infrastructure/data_access/repositories/` has a base implementation handling common CRUD.

### Domain Entities

- `Doctor` — belongs to a `Department`, has many `Appointments` and `DoctorSchedules`
- `User` — has roles (`UserRole.PATIENT`, `UserRole.ADMIN`), has many `Appointments`
- `Appointment` — links `Doctor` and `User`, tracked by `AppointmentStatus` enum
- `DoctorSchedule` — doctor availability by day/time slot
- `BaseEntity` — provides `id`, `created_at`, `updated_at` to all entities

### Database

SQLite at `data/telesecreter.db`. Alembic manages migrations from `Telesecreter_Infrastructure/data_access/migrations/`. ORM models live in `Telesecreter_Infrastructure/data_access/configurations/`.

### Current State

Basic GET endpoints are implemented for all 5 resources (`/doctors`, `/users`, `/departments`, `/appointments`, `/scheduales`). CRUD operations (create, update, delete) and webhook endpoints (`search_doctor`, `check_slots`, `confirm_booking`) are planned next per `todo.txt`.

Note: "scheduales" is the intentional (though misspelled) naming used throughout the codebase for schedules — maintain this spelling for consistency.
````

## File: context.txt
````
This file is a merged representation of the entire codebase, combined into a single document by Repomix.

<file_summary>
This section contains a summary of this file.

<purpose>
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.
</purpose>

<file_format>
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  - File path as an attribute
  - Full contents of the file
</file_format>

<usage_guidelines>
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.
</usage_guidelines>

<notes>
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)
</notes>

</file_summary>

<directory_structure>
data/
  telesecreter.db
Telesecreter_API/
  dependencies/
    dependency_injection.py
  routers/
    appointment_controller.py
    department_controller.py
    doctor_controller.py
    scheduale_controller.py
    user_controller.py
  main.py
Telesecreter_Application/
  appointment/
    dtos/
      appointment_dto.py
    queries/
      get_all_appointmens_query.py
    __init__.py
  department/
    dtos/
      department_dto.py
    queries/
      get_all_departments_query.py
    __init__.py
  doctor/
    dtos/
      doctor_dto.py
    queries/
      get_all_doctors_query.py
    __init__.py
  scheduale/
    dtos/
      scheduale_dto.py
    queries/
      get_all_scheduales_query.py
    __init__.py
  user/
    dtos/
      user_dto.py
    queries/
      get_all_users_query.py
    __init__.py
  __init__.py
Telesecreter_Domain/
  common/
    base_entity.py
  entities/
    appointments.py
    department.py
    doctor.py
    scheduale.py
    user.py
  enums/
    appointment_status.py
    user_role.py
  interfaces/
    __init__.py
    i_appointment_repository.py
    i_base_repository.py
    i_department_repository.py
    i_doctor_repository.py
    i_scheduale_repository.py
    i_user_repository.py
  __init__.py
Telesecreter_Infrastructure/
  data_access/
    configurations/
      common/
        __init__.py
        base_model.py
      models/
        __init__.py
        appintment.py
        department_model.py
        doctor_model.py
        schedual_model.py
        user_model.py
      __init__.py
    db/
      database.py
    migrations/
      versions/
        3eaebeceed60_add_department_id_to_doctors.py
        c2a7cdd538a3_initial_tables.py
      env.py
      README
      script.py.mako
    repositories/
      appointment_repository.py
      department_repository.py
      doctor_repository.py
      repository.py
      scheduale_repository.py
      user_repository.py
    __init__.py
  seeds/
    db_seeds.py
  __init__.py
.gitignore
alembic.ini
CLAUDE.md
requirements.txt
todo.txt
</directory_structure>

<files>
This section contains the contents of the repository's files.

<file path="CLAUDE.md">
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server
uvicorn Telesecreter_API.main:app --reload

# Run with specific host/port
uvicorn Telesecreter_API.main:app --reload --host 0.0.0.0 --port 8000

# Database migrations
alembic upgrade head        # Apply all migrations
alembic revision --autogenerate -m "description"  # Generate new migration

# Seed the database with sample data
python Telesecreter_Infrastructure/seeds/db_seeds.py
```

No test framework is configured yet. The interactive API docs are available at `http://localhost:8000/docs`.

## Architecture

This is a **Python FastAPI** telemedicine appointment management backend, organized in **Clean Architecture** layers:

```
Telesecreter_API/           → Presentation: FastAPI routers, dependency injection
Telesecreter_Application/   → Application: CQRS-style queries/commands, DTOs
Telesecreter_Domain/        → Domain: entities, interfaces (repository contracts), enums
Telesecreter_Infrastructure/ → Infrastructure: SQLAlchemy ORM models, repository implementations, Alembic migrations
```

### Request Flow

```
Router (controller) → Query/Command class → IRepository interface → Repository implementation → SQLite DB
```

Dependency injection is configured in `Telesecreter_API/dependencies/` and wired via FastAPI's `Depends()`.

### Key Patterns

- **Repository Pattern**: Domain layer defines abstract interfaces (`IUserRepository`, `IDoctorRepository`, etc.); infrastructure layer provides SQLAlchemy implementations.
- **CQRS-style**: Business logic lives in query classes (e.g., `GetAllDoctorsQuery`) under `Telesecreter_Application/`, not in routers.
- **DTOs**: Each application module has DTOs for API responses, separate from domain entities and ORM models.
- **Mapper layer**: Converts between SQLAlchemy ORM models and domain entities.
- **Generic base repository**: `Telesecreter_Infrastructure/data_access/repositories/` has a base implementation handling common CRUD.

### Domain Entities

- `Doctor` — belongs to a `Department`, has many `Appointments` and `DoctorSchedules`
- `User` — has roles (`UserRole.PATIENT`, `UserRole.ADMIN`), has many `Appointments`
- `Appointment` — links `Doctor` and `User`, tracked by `AppointmentStatus` enum
- `DoctorSchedule` — doctor availability by day/time slot
- `BaseEntity` — provides `id`, `created_at`, `updated_at` to all entities

### Database

SQLite at `data/telesecreter.db`. Alembic manages migrations from `Telesecreter_Infrastructure/data_access/migrations/`. ORM models live in `Telesecreter_Infrastructure/data_access/configurations/`.

### Current State

Basic GET endpoints are implemented for all 5 resources (`/doctors`, `/users`, `/departments`, `/appointments`, `/scheduales`). CRUD operations (create, update, delete) and webhook endpoints (`search_doctor`, `check_slots`, `confirm_booking`) are planned next per `todo.txt`.

Note: "scheduales" is the intentional (though misspelled) naming used throughout the codebase for schedules — maintain this spelling for consistency.
</file>

<file path="Telesecreter_API/dependencies/dependency_injection.py">
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
</file>

<file path="Telesecreter_API/routers/appointment_controller.py">
from fastapi import APIRouter, Depends

from Telesecreter_Domain.interfaces.i_appointment_repository import IAppointmentRepository
from Telesecreter_Application.appointment.dtos.appointment_dto import AppointmentDTO
from Telesecreter_Application.appointment.queries.get_all_appointmens_query import GetAllAppointmentsQuery
from Telesecreter_API.dependencies.dependency_injection import get_appointment_repo 

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.get("/", response_model=list[AppointmentDTO])
def get_all_appointments(repo:IAppointmentRepository = Depends(get_appointment_repo)):
    return GetAllAppointmentsQuery(repo).execute()
</file>

<file path="Telesecreter_API/routers/department_controller.py">
from fastapi import APIRouter, Depends

from Telesecreter_Domain.interfaces.i_department_repository import IDepartmentRepository
from Telesecreter_Application.department.dtos import department_dto
from Telesecreter_Application.department.queries.get_all_departments_query import GetAllDepartmentsQuery
from Telesecreter_API.dependencies.dependency_injection import get_department_repo

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.get("/", response_model=list[department_dto.DepartmentDTO])
def get_all_departments(repo: IDepartmentRepository = Depends(get_department_repo)):
    return GetAllDepartmentsQuery(repo).excecute()
</file>

<file path="Telesecreter_API/routers/scheduale_controller.py">
from fastapi import APIRouter, Depends

from Telesecreter_Domain.interfaces.i_scheduale_repository import IScheduleRepository
from Telesecreter_Application.scheduale.queries.get_all_scheduales_query import GetAllSchedualesQuery
from Telesecreter_Application.scheduale.dtos import scheduale_dto
from Telesecreter_API.dependencies.dependency_injection import get_schedule_repo

router = APIRouter(prefix="/scheduales", tags=["Scheduales"])

@router.get("/", response_model=list[scheduale_dto.SchedualeDTO])
def get_all_scheduales(repo: IScheduleRepository = Depends(get_schedule_repo)):
    return GetAllSchedualesQuery(repo).execute()
</file>

<file path="Telesecreter_Application/appointment/dtos/appointment_dto.py">
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class AppointmentDTO:
    id: UUID
    user_id: UUID
    doctor_id: UUID
    date: datetime
    start_time: datetime
    end_time: datetime
    status: str
    cancelled_at: datetime
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(appointment) -> "AppointmentDTO":
        return AppointmentDTO(
            id=appointment.id,
            user_id=appointment.user_id,
            doctor_id=appointment.doctor_id,
            date=appointment.date,
            start_time=appointment.start_time,
            end_time=appointment.end_time,
            status=appointment.status,
            cancelled_at=appointment.cancelled_at,
            created_at=appointment.created_at,
            updated_at=appointment.updated_at,
        )
</file>

<file path="Telesecreter_Application/appointment/queries/get_all_appointmens_query.py">
from Telesecreter_Domain.interfaces.i_appointment_repository import IAppointmentRepository
from Telesecreter_Application.appointment.dtos.appointment_dto import AppointmentDTO

class GetAllAppointmentsQuery:

    def __init__(self, appointment_repository: IAppointmentRepository):
        self._repository = appointment_repository

    def execute(self) -> list[AppointmentDTO]:
        appointments = self._repository.get_all()
        return [AppointmentDTO.from_entity(appointment) for appointment in appointments ]
</file>

<file path="Telesecreter_Application/appointment/__init__.py">

</file>

<file path="Telesecreter_Application/department/dtos/department_dto.py">
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class DepartmentDTO:
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime
    
    @staticmethod
    def from_entity(department) -> "DepartmentDTO":
        return DepartmentDTO(
            id=department.id,
            name=department.name,
            created_at=department.created_at,
            updated_at=department.updated_at,
        )
</file>

<file path="Telesecreter_Application/department/queries/get_all_departments_query.py">
from Telesecreter_Domain.interfaces.i_department_repository import IDepartmentRepository
from Telesecreter_Application.department.dtos.department_dto import DepartmentDTO


class GetAllDepartmentsQuery:

    def __init__(self, department_repository: IDepartmentRepository):
        self._repository = department_repository

    def excecute(self) -> list[DepartmentDTO]:
        departments = self._repository.get_all()
        return [DepartmentDTO.from_entity(department) for department in departments]
</file>

<file path="Telesecreter_Application/department/__init__.py">

</file>

<file path="Telesecreter_Application/doctor/__init__.py">

</file>

<file path="Telesecreter_Application/scheduale/dtos/scheduale_dto.py">
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class SchedualeDTO:
    id: UUID
    doctor_id: UUID
    day_of_week: str
    start_time: datetime
    end_time: datetime
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(scheduale) -> "SchedualeDTO":
        return SchedualeDTO(
            id=scheduale.id,
            doctor_id=scheduale.doctor_id,
            day_of_week=scheduale.day_of_week,
            start_time=scheduale.start_time,
            end_time=scheduale.end_time,
            created_at=scheduale.created_at,
            updated_at=scheduale.updated_at,
        )
</file>

<file path="Telesecreter_Application/scheduale/queries/get_all_scheduales_query.py">
from Telesecreter_Domain.interfaces.i_scheduale_repository import IScheduleRepository
from Telesecreter_Application.scheduale.dtos import scheduale_dto

class GetAllSchedualesQuery:

    def __init__(self, scheduale_repository: IScheduleRepository):
        self._repository = scheduale_repository

    def execute(self) -> list[scheduale_dto.SchedualeDTO]:
        scheduales = self._repository.get_all()
        return [scheduale_dto.SchedualeDTO.from_entity(scheduale) for scheduale in scheduales]
</file>

<file path="Telesecreter_Application/scheduale/__init__.py">

</file>

<file path="Telesecreter_Application/user/dtos/user_dto.py">
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class UserDTO:
    id: UUID
    full_name: str
    phone_number: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(user) -> "UserDTO":
        return UserDTO(
            id=user.id,
            full_name=user.full_name,
            phone_number=user.phone_number,
            email=user.email,
            role=user.role.value,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
</file>

<file path="Telesecreter_Application/user/queries/get_all_users_query.py">
from Telesecreter_Domain.interfaces.i_user_repository import IUserRepository
from Telesecreter_Application.user.dtos.user_dto import UserDTO


class GetAllUsersQuery:

    def __init__(self, user_repository: IUserRepository):
        self._repository = user_repository

    def execute(self) -> list[UserDTO]:
        users = self._repository.get_all()
        return [UserDTO.from_entity(user) for user in users]
</file>

<file path="Telesecreter_Application/user/__init__.py">

</file>

<file path="Telesecreter_Application/__init__.py">

</file>

<file path="Telesecreter_Domain/common/base_entity.py">
import uuid
from datetime import datetime, timezone


class BaseEntity:
    def __init__(self, id: uuid.UUID | None = None):
        self.id: uuid.UUID = id or uuid.uuid4()
        self.created_at: datetime = datetime.now(timezone.utc)
        self.updated_at: datetime = datetime.now(timezone.utc)

    def set_updated(self) -> None:
        self.updated_at = datetime.now(timezone.utc)

    def __eq__(self, other) -> bool:
        if not isinstance(other, BaseEntity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
</file>

<file path="Telesecreter_Domain/entities/appointments.py">
from uuid import UUID
from datetime import date, time
from typing import Optional
from Telesecreter_Domain.common.base_entity import BaseEntity
from Telesecreter_Domain.enums.appointment_status import AppointmentStatus


class Appointment(BaseEntity):
    def __init__(
        self,
        user_id: UUID,
        doctor_id: UUID,
        date: date,
        start_time: time,
        end_time: time,
        status: AppointmentStatus = AppointmentStatus.PENDING,
        notes: Optional[str] = None,
        cancelled_at: Optional[str] = None,
        cancellation_reason: Optional[str] = None,
        id: UUID | None = None,
    ):
        super().__init__(id)
        self.user_id = user_id
        self.doctor_id = doctor_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.cancelled_at = cancelled_at
        self.cancellation_reason = cancellation_reason
</file>

<file path="Telesecreter_Domain/entities/department.py">
from Telesecreter_Domain.common.base_entity import BaseEntity
from uuid import UUID
 
 
class Department(BaseEntity):
    def __init__(
        self,
        name: str,
        id: UUID | None = None,
    ):
        super().__init__(id)
        self.name = name
</file>

<file path="Telesecreter_Domain/entities/doctor.py">
from uuid import UUID
from typing import Optional
from Telesecreter_Domain.common.base_entity import BaseEntity


class Doctor(BaseEntity):
    def __init__(
        self,
        full_name: str,
        email: str,
        department_id: UUID,
        specialty: str,
        phone_number: str = "",
        ratings: Optional[float] = None,
        years_of_experience: int = 0,
        bio: Optional[str] = None,
        is_available: bool = True,
        id: UUID | None = None,
    ):
        super().__init__(id)
        ratings = ratings if ratings is not None else 0.0
        self.full_name = full_name
        self.email = email
        self.phone_number = phone_number
        self.department_id = department_id
        self.specialty = specialty
        self.is_available = is_available
</file>

<file path="Telesecreter_Domain/entities/scheduale.py">
from uuid import UUID
from datetime import time
from Telesecreter_Domain.common.base_entity import BaseEntity


class DoctorSchedule(BaseEntity):
    def __init__(
        self,
        doctor_id: UUID,
        day_of_week: int,
        start_time: time,
        end_time: time,
        id: UUID | None = None,
    ):
        super().__init__(id)
        self.doctor_id = doctor_id
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time
</file>

<file path="Telesecreter_Domain/entities/user.py">
from uuid import UUID
from Telesecreter_Domain.common.base_entity import BaseEntity
from Telesecreter_Domain.enums.user_role import UserRole

class User(BaseEntity):
    def __init__(
        self,
        full_name: str,
        phone_number: str,
        email: str,
        hashed_password: str,
        role: UserRole = UserRole.PATIENT,
        is_active: bool = True,
        id: UUID | None = None,
    ):
        super().__init__(id)
        self.full_name = full_name
        self.phone_number = phone_number
        self.email = email
        self.hashed_password = hashed_password
        self.role = role
        self.is_active = is_active
</file>

<file path="Telesecreter_Domain/enums/appointment_status.py">
import enum


class AppointmentStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    RESCHEDULED = "rescheduled"
</file>

<file path="Telesecreter_Domain/enums/user_role.py">
import enum


class UserRole(enum.Enum):
    PATIENT = "patient"
    ADMIN = "admin"
</file>

<file path="Telesecreter_Domain/interfaces/__init__.py">

</file>

<file path="Telesecreter_Domain/interfaces/i_appointment_repository.py">
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
</file>

<file path="Telesecreter_Domain/interfaces/i_base_repository.py">
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional
from uuid import UUID

T = TypeVar("T")


class IBaseRepository(ABC, Generic[T]):

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def add(self, entity: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError
</file>

<file path="Telesecreter_Domain/interfaces/i_department_repository.py">
from abc import abstractmethod
from typing import Optional
from Telesecreter_Domain.interfaces.i_base_repository import IBaseRepository
from Telesecreter_Domain.entities.department import Department


class IDepartmentRepository(IBaseRepository[Department]):

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Department]:
        raise NotImplementedError
</file>

<file path="Telesecreter_Domain/interfaces/i_doctor_repository.py">
from abc import abstractmethod
from typing import Optional
from uuid import UUID
from Telesecreter_Domain.interfaces.i_base_repository import IBaseRepository
from Telesecreter_Domain.entities.doctor import Doctor


class IDoctorRepository(IBaseRepository[Doctor]):

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Doctor]:
        raise NotImplementedError

    @abstractmethod
    def get_by_department(self, department_id: UUID) -> list[Doctor]:
        raise NotImplementedError

    @abstractmethod
    def get_available_doctors(self) -> list[Doctor]:
        raise NotImplementedError
</file>

<file path="Telesecreter_Domain/interfaces/i_scheduale_repository.py">
from abc import abstractmethod
from uuid import UUID
from Telesecreter_Domain.interfaces.i_base_repository import IBaseRepository
from Telesecreter_Domain.entities.scheduale import DoctorSchedule


class IScheduleRepository(IBaseRepository[DoctorSchedule]):

    @abstractmethod
    def get_by_doctor(self, doctor_id: UUID) -> list[DoctorSchedule]:
        raise NotImplementedError

    @abstractmethod
    def get_by_doctor_and_day(self, doctor_id: UUID, day_of_week: int) -> list[DoctorSchedule]:
        raise
</file>

<file path="Telesecreter_Domain/interfaces/i_user_repository.py">
from abc import abstractmethod
from typing import Optional
from uuid import UUID
from Telesecreter_Domain.interfaces.i_base_repository import IBaseRepository
from Telesecreter_Domain.entities.user import User


class IUserRepository(IBaseRepository[User]):

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_by_phone(self, phone_number: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_active_users(self) -> list[User]:
        raise NotImplementedError
</file>

<file path="Telesecreter_Domain/__init__.py">

</file>

<file path="Telesecreter_Infrastructure/data_access/configurations/common/__init__.py">

</file>

<file path="Telesecreter_Infrastructure/data_access/configurations/common/base_model.py">
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


def utc_now():
    return datetime.now(timezone.utc)


class BaseModel(Base):
    """Abstract base for all ORM models — mirrors domain BaseEntity fields."""
    __abstract__ = True

    id = Column(String, primary_key=True, default=generate_uuid)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)
</file>

<file path="Telesecreter_Infrastructure/data_access/configurations/models/__init__.py">

</file>

<file path="Telesecreter_Infrastructure/data_access/configurations/models/appintment.py">
from sqlalchemy import Column, String, Date, Time, ForeignKey, Enum, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from Telesecreter_Infrastructure.data_access.configurations.common.base_model import BaseModel
from Telesecreter_Domain.enums.appointment_status import AppointmentStatus


class AppointmentModel(BaseModel):
    __tablename__ = "appointments"

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    doctor_id = Column(String, ForeignKey("doctors.id"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.PENDING, nullable=False)
    cancelled_at = Column(String, nullable=True)
    cancellation_reason = Column(String, nullable=True)

    user = relationship("UserModel", back_populates="appointments")
    doctor = relationship("DoctorModel", back_populates="appointments")

    __table_args__ = (
        Index("ix_appointment_user", "user_id"),
        Index("ix_appointment_doctor_date", "doctor_id", "date"),
        UniqueConstraint("doctor_id", "date", "start_time", name="uq_doctor_timeslot"),
    )
</file>

<file path="Telesecreter_Infrastructure/data_access/configurations/models/schedual_model.py">
from sqlalchemy import Column, String, Integer, Time, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from Telesecreter_Infrastructure.data_access.configurations.common.base_model import BaseModel

class DoctorScheduleModel(BaseModel):
    __tablename__ = "doctor_schedules"

    doctor_id = Column(String, ForeignKey("doctors.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    doctor = relationship("DoctorModel", back_populates="schedules")

    __table_args__ = (
        Index("ix_schedule_doctor", "doctor_id"),
        UniqueConstraint("doctor_id", "day_of_week", name="uq_doctor_day"),
    )
</file>

<file path="Telesecreter_Infrastructure/data_access/configurations/models/user_model.py">
from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.orm import relationship
from Telesecreter_Infrastructure.data_access.configurations.common.base_model import BaseModel
from Telesecreter_Domain.enums.user_role import UserRole


class UserModel(BaseModel):
    __tablename__ = "users"

    full_name       = Column(String, nullable=False)
    phone_number    = Column(String, unique=True, nullable=False)
    email           = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role            = Column(Enum(UserRole), nullable=False, default=UserRole.PATIENT)
    is_active       = Column(Boolean, default=True, nullable=False)

    appointments = relationship("AppointmentModel", back_populates="user")
</file>

<file path="Telesecreter_Infrastructure/data_access/configurations/__init__.py">

</file>

<file path="Telesecreter_Infrastructure/data_access/db/database.py">
import sqlite3
import logging
from pathlib import Path
from contextlib import contextmanager
 
logger = logging.getLogger(__name__)
 
# Resolves to TelesecreterV1/data/telesecreter.db
DB_PATH = Path(__file__).parents[3] / "data" / "telesecreter.db"
 
# Ensure the data directory exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
 
 
def get_connection() -> sqlite3.Connection:
    """
    Create and return a new SQLite connection.
    - Row factory set so rows behave like dicts (access by column name).
    - Foreign key enforcement enabled per connection.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
 
 
@contextmanager
def get_db():
    """
    Context manager that yields a connection and handles
    commit/rollback/close automatically.
 
    Usage:
        with get_db() as conn:
            conn.execute("INSERT INTO ...")
    """
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error("Database error, rolling back: %s", e)
        raise
    finally:
        conn.close()
 
 
def init_db(schema_path: Path | None = None) -> None:
    """
    Initialize the database by running a SQL schema file.
 
    Args:
        schema_path: Path to the .sql schema file.
                     Defaults to schema.sql in the same directory.
    """
    if schema_path is None:
        schema_path = Path(__file__).parent / "schema.sql"
 
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
 
    with get_db() as conn:
        sql = schema_path.read_text(encoding="utf-8")
        conn.executescript(sql)
 
    logger.info("Database initialized from %s", schema_path)
 
 
def check_connection() -> bool:
    """
    Quick health-check — returns True if the DB is reachable.
    """
    try:
        with get_db() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error("Database health-check failed: %s", e)
        return False
</file>

<file path="Telesecreter_Infrastructure/data_access/migrations/versions/3eaebeceed60_add_department_id_to_doctors.py">
"""add department_id to doctors

Revision ID: 3eaebeceed60
Revises: c2a7cdd538a3
Create Date: 2026-04-05 14:12:26.773799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3eaebeceed60'
down_revision: Union[str, Sequence[str], None] = 'c2a7cdd538a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('doctors', schema=None) as batch_op:
        batch_op.add_column(sa.Column('department_id', sa.String(), nullable=False))
        batch_op.create_foreign_key('fk_doctors_department_id', 'departments', ['department_id'], ['id'])

def downgrade() -> None:
    with op.batch_alter_table('doctors', schema=None) as batch_op:
        batch_op.drop_constraint('fk_doctors_department_id', type_='foreignkey')
        batch_op.drop_column('department_id')
</file>

<file path="Telesecreter_Infrastructure/data_access/migrations/versions/c2a7cdd538a3_initial_tables.py">
"""initial tables

Revision ID: c2a7cdd538a3
Revises: 
Create Date: 2026-04-05 13:54:28.967739

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2a7cdd538a3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('departments',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', name='uq_department_name')
    )
    op.create_table('doctors',
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('specialty', sa.String(), nullable=False),
    sa.Column('is_available', sa.Boolean(), nullable=False),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('users',
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('role', sa.Enum('PATIENT', 'ADMIN', name='userrole'), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number')
    )
    op.create_table('appointments',
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('doctor_id', sa.String(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'CONFIRMED', 'CANCELLED', 'COMPLETED', 'RESCHEDULED', name='appointmentstatus'), nullable=False),
    sa.Column('cancelled_at', sa.String(), nullable=True),
    sa.Column('cancellation_reason', sa.String(), nullable=True),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('doctor_id', 'date', 'start_time', name='uq_doctor_timeslot')
    )
    with op.batch_alter_table('appointments', schema=None) as batch_op:
        batch_op.create_index('ix_appointment_doctor_date', ['doctor_id', 'date'], unique=False)
        batch_op.create_index('ix_appointment_user', ['user_id'], unique=False)

    op.create_table('doctor_schedules',
    sa.Column('doctor_id', sa.String(), nullable=False),
    sa.Column('day_of_week', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('doctor_id', 'day_of_week', name='uq_doctor_day')
    )
    with op.batch_alter_table('doctor_schedules', schema=None) as batch_op:
        batch_op.create_index('ix_schedule_doctor', ['doctor_id'], unique=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('doctor_schedules', schema=None) as batch_op:
        batch_op.drop_index('ix_schedule_doctor')

    op.drop_table('doctor_schedules')
    with op.batch_alter_table('appointments', schema=None) as batch_op:
        batch_op.drop_index('ix_appointment_user')
        batch_op.drop_index('ix_appointment_doctor_date')

    op.drop_table('appointments')
    op.drop_table('users')
    op.drop_table('doctors')
    op.drop_table('departments')
    # ### end Alembic commands ###
</file>

<file path="Telesecreter_Infrastructure/data_access/migrations/env.py">
import sys
from pathlib import Path

# Add project root (TelesecreterV1/) to Python path
sys.path.insert(0, str(Path(__file__).parents[3]))

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from Telesecreter_Infrastructure.data_access.configurations.common.base_model import Base
from Telesecreter_Infrastructure.data_access.configurations.models.department_model import DepartmentModel  # noqa: F401
from Telesecreter_Infrastructure.data_access.configurations.models.user_model import UserModel              # noqa: F401
from Telesecreter_Infrastructure.data_access.configurations.models.doctor_model import DoctorModel          # noqa: F401
from Telesecreter_Infrastructure.data_access.configurations.models.schedual_model import DoctorScheduleModel  # noqa: F401
from Telesecreter_Infrastructure.data_access.configurations.models.appintment import AppointmentModel       # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
</file>

<file path="Telesecreter_Infrastructure/data_access/migrations/README">
Generic single-database configuration.
</file>

<file path="Telesecreter_Infrastructure/data_access/migrations/script.py.mako">
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, Sequence[str], None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    """Upgrade schema."""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Downgrade schema."""
    ${downgrades if downgrades else "pass"}
</file>

<file path="Telesecreter_Infrastructure/data_access/repositories/appointment_repository.py">
from datetime import date
from uuid import UUID
from Telesecreter_Domain.interfaces.i_appointment_repository import IAppointmentRepository
from Telesecreter_Domain.entities.appointments import Appointment
from Telesecreter_Domain.enums.appointment_status import AppointmentStatus
from Telesecreter_Infrastructure.data_access.configurations.models.appintment import AppointmentModel
from Telesecreter_Infrastructure.data_access.repositories.repository import GenericRepository
from Telesecreter_Infrastructure.data_access.db.database import get_db


def _map(row) -> Appointment:
    return Appointment(
        id=row["id"],
        user_id=row["user_id"],
        doctor_id=row["doctor_id"],
        date=row["date"],
        start_time=row["start_time"],
        end_time=row["end_time"],
        status=AppointmentStatus(row["status"]),
        notes=row["notes"] if "notes" in row.keys() else None,
        cancelled_at=row["cancelled_at"],
        cancellation_reason=row["cancellation_reason"],
    )


class AppointmentRepository(GenericRepository[Appointment, AppointmentModel], IAppointmentRepository):

    def __init__(self):
        super().__init__(AppointmentModel, _map)

    def get_by_user(self, user_id: UUID) -> list[Appointment]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM appointments WHERE user_id = ?", (str(user_id),)).fetchall()
            return [_map(row) for row in rows]

    def get_by_doctor(self, doctor_id: UUID) -> list[Appointment]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM appointments WHERE doctor_id = ?", (str(doctor_id),)).fetchall()
            return [_map(row) for row in rows]

    def get_by_doctor_and_date(self, doctor_id: UUID, date: date) -> list[Appointment]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM appointments WHERE doctor_id = ? AND date = ?",
                (str(doctor_id), str(date))
            ).fetchall()
            return [_map(row) for row in rows]

    def get_by_status(self, status: AppointmentStatus) -> list[Appointment]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM appointments WHERE status = ?", (status.value,)).fetchall()
            return [_map(row) for row in rows]
</file>

<file path="Telesecreter_Infrastructure/data_access/repositories/department_repository.py">
from typing import Optional
from Telesecreter_Domain.interfaces.i_department_repository import IDepartmentRepository
from Telesecreter_Domain.entities.department import Department
from Telesecreter_Infrastructure.data_access.configurations.models.department_model import DepartmentModel
from Telesecreter_Infrastructure.data_access.repositories.repository import GenericRepository
from Telesecreter_Infrastructure.data_access.db.database import get_db


def _map(row) -> Department:
    return Department(
        id=row["id"],
        name=row["name"],
    )


class DepartmentRepository(GenericRepository[Department, DepartmentModel], IDepartmentRepository):

    def __init__(self):
        super().__init__(DepartmentModel, _map)

    def get_by_name(self, name: str) -> Optional[Department]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM departments WHERE name = ?", (name,)).fetchone()
            return _map(row) if row else None
</file>

<file path="Telesecreter_Infrastructure/data_access/repositories/repository.py">
from typing import Generic, TypeVar, Optional, Type
from uuid import UUID
from Telesecreter_Infrastructure.data_access.db.database import get_db
from Telesecreter_Domain.interfaces.i_base_repository import IBaseRepository

T = TypeVar("T")
M = TypeVar("M")


class GenericRepository(IBaseRepository[T], Generic[T, M]):
    """
    Generic SQLite repository.
    T = Domain entity type
    M = SQLAlchemy model type
    """

    def __init__(self, model_class: Type[M], mapper):
        self._model = model_class
        self._mapper = mapper  # callable: model -> entity

    def get_by_id(self, id: UUID) -> Optional[T]:
        with get_db() as conn:
            row = conn.execute(
                f"SELECT * FROM {self._model.__tablename__} WHERE id = ?", (str(id),)
            ).fetchone()
            return self._mapper(row) if row else None

    def get_all(self) -> list[T]:
        with get_db() as conn:
            rows = conn.execute(
                f"SELECT * FROM {self._model.__tablename__}"
            ).fetchall()
            return [self._mapper(row) for row in rows]

    def add(self, entity: T) -> T:
        data = vars(entity)
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        values = [str(v) if not isinstance(v, (int, float, bool, type(None))) else v for v in data.values()]
        with get_db() as conn:
            conn.execute(
                f"INSERT INTO {self._model.__tablename__} ({columns}) VALUES ({placeholders})",
                values
            )
        return entity

    def update(self, entity: T) -> T:
        data = {k: v for k, v in vars(entity).items() if k != "id"}
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        values = [str(v) if not isinstance(v, (int, float, bool, type(None))) else v for v in data.values()]
        values.append(str(entity.id))
        with get_db() as conn:
            conn.execute(
                f"UPDATE {self._model.__tablename__} SET {set_clause} WHERE id = ?",
                values
            )
        return entity

    def delete(self, id: UUID) -> None:
        with get_db() as conn:
            conn.execute(
                f"DELETE FROM {self._model.__tablename__} WHERE id = ?", (str(id),)
            )
</file>

<file path="Telesecreter_Infrastructure/data_access/__init__.py">

</file>

<file path="Telesecreter_Infrastructure/seeds/db_seeds.py">
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2]))

from datetime import date, time
from Telesecreter_Infrastructure.data_access.configurations.common.base_model import Base
from Telesecreter_Infrastructure.data_access.configurations.models.department_model import DepartmentModel
from Telesecreter_Infrastructure.data_access.configurations.models.doctor_model import DoctorModel
from Telesecreter_Infrastructure.data_access.configurations.models.user_model import UserModel
from Telesecreter_Infrastructure.data_access.configurations.models.schedual_model import DoctorScheduleModel
from Telesecreter_Infrastructure.data_access.configurations.models.appintment import AppointmentModel
from Telesecreter_Domain.enums.user_role import UserRole
from Telesecreter_Domain.enums.appointment_status import AppointmentStatus
from Telesecreter_Infrastructure.data_access.db.database import get_db
import uuid


def seed():
    with get_db() as conn:
        try:
            # 1. Departments
            departments = [
                {"id": str(uuid.uuid4()), "name": "General Practice"},
                {"id": str(uuid.uuid4()), "name": "Cardiology"},
                {"id": str(uuid.uuid4()), "name": "Neurology"},
                {"id": str(uuid.uuid4()), "name": "Orthopedics"},
            ]
            conn.executemany(
                "INSERT INTO departments (id, name, created_at, updated_at) VALUES (:id, :name, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
                departments
            )
            print("✅ Departments added")

            # 2. Doctors
            doctors = [
                {"id": str(uuid.uuid4()), "full_name": "Dr. John Smith",   "email": "john.smith@hospital.com",   "phone_number": "+1234567890", "department_id": departments[0]["id"], "specialty": "General Medicine", "is_available": 1, "rating": 4.5},
                {"id": str(uuid.uuid4()), "full_name": "Dr. Sarah Connor",  "email": "sarah.connor@hospital.com",  "phone_number": "+1234567891", "department_id": departments[1]["id"], "specialty": "Cardiology",       "is_available": 1, "rating": 4.9},
                {"id": str(uuid.uuid4()), "full_name": "Dr. Emily Davis",   "email": "emily.davis@hospital.com",   "phone_number": "+1234567892", "department_id": departments[2]["id"], "specialty": "Neurology",        "is_available": 1, "rating": 3.8},
                {"id": str(uuid.uuid4()), "full_name": "Dr. James Wilson",  "email": "james.wilson@hospital.com",  "phone_number": "+1234567893", "department_id": departments[3]["id"], "specialty": "Orthopedics",      "is_available": 1, "rating": 4.2},
            ]
            conn.executemany(
                """INSERT INTO doctors (id, full_name, email, phone_number, department_id, specialty, is_available, rating, created_at, updated_at)
                   VALUES (:id, :full_name, :email, :phone_number, :department_id, :specialty, :is_available, :rating, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""",
                doctors
            )
            print("✅ Doctors added")

            # 3. Schedules (Mon-Fri, 09:00-17:00 for each doctor)
            schedules = [
                {"id": str(uuid.uuid4()), "doctor_id": doctor["id"], "day_of_week": day, "start_time": "09:00:00", "end_time": "17:00:00"}
                for doctor in doctors
                for day in range(0, 5)
            ]
            conn.executemany(
                """INSERT INTO doctor_schedules (id, doctor_id, day_of_week, start_time, end_time, created_at, updated_at)
                   VALUES (:id, :doctor_id, :day_of_week, :start_time, :end_time, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""",
                schedules
            )
            print("✅ Schedules added")

            # 4. Users
            users = [
                {"id": str(uuid.uuid4()), "full_name": "Alice Johnson", "email": "alice@example.com", "phone_number": "+9876543210", "hashed_password": "hashed_password_here", "role": UserRole.PATIENT.value, "is_active": 1},
                {"id": str(uuid.uuid4()), "full_name": "Bob Williams",  "email": "bob@example.com",   "phone_number": "+9876543211", "hashed_password": "hashed_password_here", "role": UserRole.PATIENT.value, "is_active": 1},
            ]
            conn.executemany(
                """INSERT INTO users (id, full_name, email, phone_number, hashed_password, role, is_active, created_at, updated_at)
                   VALUES (:id, :full_name, :email, :phone_number, :hashed_password, :role, :is_active, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""",
                users
            )
            print("✅ Users added")

            # 5. Appointments
            appointments = [
                {"id": str(uuid.uuid4()), "user_id": users[0]["id"], "doctor_id": doctors[0]["id"], "date": "2026-04-10", "start_time": "09:00:00", "end_time": "09:30:00", "status": AppointmentStatus.CONFIRMED.value},
                {"id": str(uuid.uuid4()), "user_id": users[0]["id"], "doctor_id": doctors[1]["id"], "date": "2026-04-14", "start_time": "10:00:00", "end_time": "10:30:00", "status": AppointmentStatus.PENDING.value},
                {"id": str(uuid.uuid4()), "user_id": users[1]["id"], "doctor_id": doctors[2]["id"], "date": "2026-04-11", "start_time": "11:00:00", "end_time": "11:30:00", "status": AppointmentStatus.PENDING.value},
                {"id": str(uuid.uuid4()), "user_id": users[1]["id"], "doctor_id": doctors[3]["id"], "date": "2026-04-15", "start_time": "14:00:00", "end_time": "14:30:00", "status": AppointmentStatus.CONFIRMED.value},
            ]
            conn.executemany(
                """INSERT INTO appointments (id, user_id, doctor_id, date, start_time, end_time, status, created_at, updated_at)
                   VALUES (:id, :user_id, :doctor_id, :date, :start_time, :end_time, :status, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""",
                appointments
            )
            print("✅ Appointments added")

            print("🎉 All seed data inserted successfully")

        except Exception as e:
            print(f"❌ Error: {e}")
            raise


if __name__ == "__main__":
    seed()
</file>

<file path="Telesecreter_Infrastructure/__init__.py">

</file>

<file path=".gitignore">
# Python cache
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.so

# Virtual environment
venv1/
.venv/a
venv/
ENV/
env/
*.env

# Jupyter Notebook checkpoints
.ipynb_checkpoints/

# VSCode / PyCharm
.vscode/
.idea/

# Logs
*.log
logs/
*.out
*.err

# Data
model/data/
*.csv
*.tsv
*.json

# Model checkpoints
model/checkpoints/
*.bin
*.pt
*.ckpt
*.h5

# OS files
.DS_Store
Thumbs.db

# Build / distribution
build/
dist/
*.egg-info/
</file>

<file path="alembic.ini">
[alembic]
script_location = Telesecreter_Infrastructure/data_access/migrations
sqlalchemy.url = sqlite:///data/telesecreter.db

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
</file>

<file path="requirements.txt">
fastapi
uvicorn[standard]
python-multipart
pydantic>=2
SQLAlchemy>=2
alembic
python-dotenv
twilio
httpx
# v2 için (kendi STT/TTS)
faster-whisper
coqpit
# TTS (Temporarily disabled - requires Python < 3.12)
# soundfile
# numpy
# torch
# transformers
# kokoro
# soundfile
fastapi
</file>

<file path="todo.txt">
endpoints level 1
-get doctors,departments,appointments,scheduales

endpoints level 2
-get by id;users,doctorsdepartments,scheduales,appointments

endpoints level 3
get by name;users,doctorsdepartments,scheduales,appointments

endpoints level 4
update;users,doctorsdepartments,scheduales,appointments

endpoint levl 5
delete;users,doctorsdepartments,scheduales,appointments

webhook;
-get doctors scheduale webhook
-book appointment webhook
-cancel appointment webhook


Webhook Adı,Görevi,Neden Önemli?
search_doctor,Semptom -> Departman -> Doktor (Rating'e göre),"Projenin ""Zekası"""
check_slots,Seçilen doktorun boş saatlerini getirir,"Projenin ""Fonksiyonu"""
confirm_booking,Randevuyu Appointments tablosuna INSERT eder,"Projenin ""Bütünlüğü"""


gorevler
-ilk olarak bul endpointlerin nasil calisr iclerinde nevar
-sora ekle book appointment,reccomend doctor by symphtom
-sora ekle confirm appointment email
-sora ekle reschedual appointment


ne yaptik;
get all endpointii yazdik herbir entity icin 
simdi lazim set appointment, recommend doctor yapalim calissin webhookle
zamana gore diger endpointleri de yazalim
</file>

<file path="Telesecreter_Application/doctor/dtos/doctor_dto.py">
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class DoctorDTO:
    id: UUID
    full_name: str
    speciality: str
    phone_number: str
    email: str
    is_available: bool
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(doctor) -> "DoctorDTO":
        return DoctorDTO(
            id=doctor.id,
            full_name=doctor.full_name,
            speciality=doctor.specialty,
            phone_number=doctor.phone_number,
            email=doctor.email,
            is_available=doctor.is_available,
            created_at=doctor.created_at,
            updated_at=doctor.updated_at,
        )
</file>

<file path="Telesecreter_Application/doctor/queries/get_all_doctors_query.py">
from Telesecreter_Domain.interfaces.i_doctor_repository import IDoctorRepository
from Telesecreter_Application.doctor.dtos.doctor_dto import DoctorDTO

class GetAllDoctorsQuery:

    def __init__(self,doctor_repository: IDoctorRepository):
        self._repository = doctor_repository

    def execute(self) -> list[DoctorDTO]:
        doctors = self._repository.get_all()
        return [DoctorDTO.from_entity(doctor) for doctor in doctors]
</file>

<file path="Telesecreter_Infrastructure/data_access/configurations/models/department_model.py">
from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.orm import relationship
from Telesecreter_Infrastructure.data_access.configurations.common.base_model import BaseModel


class DepartmentModel(BaseModel):
    __tablename__ = "departments"

    name = Column(String, nullable=False)

    doctors = relationship("DoctorModel", back_populates="department")

    __table_args__ = (
        UniqueConstraint("name", name="uq_department_name"),
    )

    @property
    def doctor_ids(self) -> list[str]:
        return [doctor.id for doctor in self.doctors]
</file>

<file path="Telesecreter_Infrastructure/data_access/configurations/models/doctor_model.py">
from sqlalchemy import Column, ForeignKey, String, Boolean, Float
from sqlalchemy.orm import relationship
from Telesecreter_Infrastructure.data_access.configurations.common.base_model import BaseModel


class DoctorModel(BaseModel):
    __tablename__ = "doctors"

    full_name    = Column(String, nullable=False)
    email        = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=True, default="")
    department_id = Column(String, ForeignKey("departments.id"), nullable=False)
    specialty    = Column(String, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    rating       = Column(Float, nullable=True, default=None)

    department   = relationship("DepartmentModel", back_populates="doctors")
    appointments = relationship("AppointmentModel", back_populates="doctor")
    schedules    = relationship("DoctorScheduleModel", back_populates="doctor")
</file>

<file path="Telesecreter_Infrastructure/data_access/repositories/scheduale_repository.py">
from uuid import UUID
from Telesecreter_Domain.interfaces.i_scheduale_repository import IScheduleRepository
from Telesecreter_Domain.entities.scheduale import DoctorSchedule
from Telesecreter_Infrastructure.data_access.configurations.models.schedual_model import DoctorScheduleModel
from Telesecreter_Infrastructure.data_access.repositories.repository import GenericRepository
from Telesecreter_Infrastructure.data_access.db.database import get_db


def _map(row) -> DoctorSchedule:
    return DoctorSchedule(
        id=row["id"],
        doctor_id=row["doctor_id"],
        day_of_week=row["day_of_week"],
        start_time=row["start_time"],
        end_time=row["end_time"],
    )


class ScheduleRepository(GenericRepository[DoctorSchedule, DoctorScheduleModel], IScheduleRepository):

    def __init__(self):
        super().__init__(DoctorScheduleModel, _map)

    def get_by_doctor(self, doctor_id: UUID) -> list[DoctorSchedule]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM doctor_schedules WHERE doctor_id = ?", (str(doctor_id),)).fetchall()
            return [_map(row) for row in rows]

    def get_by_doctor_and_day(self, doctor_id: UUID, day_of_week: int) -> list[DoctorSchedule]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM doctor_schedules WHERE doctor_id = ? AND day_of_week = ?",
                (str(doctor_id), day_of_week)
            ).fetchall()
            return [_map(row) for row in rows]
</file>

<file path="Telesecreter_Infrastructure/data_access/repositories/user_repository.py">
from typing import Optional
from uuid import UUID
from Telesecreter_Domain.interfaces.i_user_repository import IUserRepository
from Telesecreter_Domain.entities.user import User
from Telesecreter_Domain.enums.user_role import UserRole
from Telesecreter_Infrastructure.data_access.configurations.models.user_model import UserModel
from Telesecreter_Infrastructure.data_access.repositories.repository import GenericRepository
from Telesecreter_Infrastructure.data_access.db.database import get_db


def _map(row) -> User:
    return User(
        id=row["id"],
        full_name=row["full_name"],
        phone_number=row["phone_number"],
        email=row["email"],
        hashed_password=row["hashed_password"],
        role=UserRole(row["role"]),
        is_active=bool(row["is_active"]),
    )


class UserRepository(GenericRepository[User, UserModel], IUserRepository):

    def __init__(self):
        super().__init__(UserModel, _map)

    def get_by_email(self, email: str) -> Optional[User]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            return _map(row) if row else None

    def get_by_phone(self, phone_number: str) -> Optional[User]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM users WHERE phone_number = ?", (phone_number,)).fetchone()
            return _map(row) if row else None

    def get_active_users(self) -> list[User]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM users WHERE is_active = 1").fetchall()
            return [_map(row) for row in rows]
</file>

<file path="Telesecreter_API/routers/doctor_controller.py">
from fastapi import APIRouter, Depends

from Telesecreter_Domain.interfaces.i_doctor_repository import IDoctorRepository
from Telesecreter_Application.doctor.dtos.doctor_dto import DoctorDTO
from Telesecreter_Application.doctor.queries.get_all_doctors_query import GetAllDoctorsQuery
from Telesecreter_API.dependencies.dependency_injection import get_doctor_repo

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.get("/", response_model=list[DoctorDTO])
def get_all_doctors(repo: IDoctorRepository = Depends(get_doctor_repo)):
    return GetAllDoctorsQuery(repo).execute()
</file>

<file path="Telesecreter_API/routers/user_controller.py">
from fastapi import APIRouter, Depends

from Telesecreter_Domain.interfaces.i_user_repository import IUserRepository
from Telesecreter_Application.user.dtos.user_dto import UserDTO
from Telesecreter_Application.user.queries.get_all_users_query import GetAllUsersQuery
from Telesecreter_API.dependencies.dependency_injection import get_user_repo

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserDTO])
def get_all_users(repo: IUserRepository = Depends(get_user_repo)):
    return GetAllUsersQuery(repo).execute()
</file>

<file path="Telesecreter_Infrastructure/data_access/repositories/doctor_repository.py">
from typing import Optional
from uuid import UUID
from Telesecreter_Domain.interfaces.i_doctor_repository import IDoctorRepository
from Telesecreter_Domain.entities.doctor import Doctor
from Telesecreter_Infrastructure.data_access.configurations.models.doctor_model import DoctorModel
from Telesecreter_Infrastructure.data_access.repositories.repository import GenericRepository
from Telesecreter_Infrastructure.data_access.db.database import get_db


def _map(row) -> Doctor:
    return Doctor(
        id=row["id"],
        full_name=row["full_name"],
        email=row["email"],
        phone_number=row["phone_number"],
        department_id=row["department_id"],
        specialty=row["specialty"],
        is_available=bool(row["is_available"]),
        ratings=row["rating"],
    )


class DoctorRepository(GenericRepository[Doctor, DoctorModel], IDoctorRepository):

    def __init__(self):
        super().__init__(DoctorModel, _map)

    def get_by_email(self, email: str) -> Optional[Doctor]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM doctors WHERE email = ?", (email,)).fetchone()
            return _map(row) if row else None

    def get_by_department(self, department_id: UUID) -> list[Doctor]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM doctors WHERE department_id = ?", (str(department_id),)).fetchall()
            return [_map(row) for row in rows]

    def get_available_doctors(self) -> list[Doctor]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM doctors WHERE is_available = 1").fetchall()
            return [_map(row) for row in rows]
</file>

<file path="Telesecreter_API/main.py">
import sys
import os
from fastapi import FastAPI

# Ensure the backend directory is in the Python path so it can import Telesecretary namespace properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Telesecreter_API.routers import doctor_controller, user_controller,department_controller,appointment_controller,scheduale_controller


app = FastAPI(
    title="Telesecretary API",
    description="Backend API for the Telesecretary application",
    version="1.0.0"
)

# Connect all routers
app.include_router(user_controller.router)
app.include_router(doctor_controller.router)
app.include_router(department_controller.router)
app.include_router(appointment_controller.router)
app.include_router(scheduale_controller.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Telesecretary API! Visit /docs for Swagger documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
</file>

</files>
````

## File: Telesecreter_API/dependencies/dependency_injection.py
````python
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
````

## File: Telesecreter_API/routers/appointment_controller.py
````python
from fastapi import APIRouter, Depends

from Telesecreter_Domain.interfaces.i_appointment_repository import IAppointmentRepository
from Telesecreter_Application.appointment.dtos.appointment_dto import AppointmentDTO
from Telesecreter_Application.appointment.queries.get_all_appointmens_query import GetAllAppointmentsQuery
from Telesecreter_API.dependencies.dependency_injection import get_appointment_repo 

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.get("/", response_model=list[AppointmentDTO])
def get_all_appointments(repo:IAppointmentRepository = Depends(get_appointment_repo)):
    return GetAllAppointmentsQuery(repo).execute()
````

## File: Telesecreter_API/routers/department_controller.py
````python
from fastapi import APIRouter, Depends

from Telesecreter_Domain.interfaces.i_department_repository import IDepartmentRepository
from Telesecreter_Application.department.dtos import department_dto
from Telesecreter_Application.department.queries.get_all_departments_query import GetAllDepartmentsQuery
from Telesecreter_API.dependencies.dependency_injection import get_department_repo

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.get("/", response_model=list[department_dto.DepartmentDTO])
def get_all_departments(repo: IDepartmentRepository = Depends(get_department_repo)):
    return GetAllDepartmentsQuery(repo).excecute()
````

## File: Telesecreter_API/routers/scheduale_controller.py
````python
from fastapi import APIRouter, Depends

from Telesecreter_Domain.interfaces.i_scheduale_repository import IScheduleRepository
from Telesecreter_Application.scheduale.queries.get_all_scheduales_query import GetAllSchedualesQuery
from Telesecreter_Application.scheduale.dtos import scheduale_dto
from Telesecreter_API.dependencies.dependency_injection import get_schedule_repo

router = APIRouter(prefix="/scheduales", tags=["Scheduales"])

@router.get("/", response_model=list[scheduale_dto.SchedualeDTO])
def get_all_scheduales(repo: IScheduleRepository = Depends(get_schedule_repo)):
    return GetAllSchedualesQuery(repo).execute()
````

## File: Telesecreter_Application/appointment/dtos/appointment_dto.py
````python
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class AppointmentDTO:
    id: UUID
    user_id: UUID
    doctor_id: UUID
    date: datetime
    start_time: datetime
    end_time: datetime
    status: str
    cancelled_at: datetime
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(appointment) -> "AppointmentDTO":
        return AppointmentDTO(
            id=appointment.id,
            user_id=appointment.user_id,
            doctor_id=appointment.doctor_id,
            date=appointment.date,
            start_time=appointment.start_time,
            end_time=appointment.end_time,
            status=appointment.status,
            cancelled_at=appointment.cancelled_at,
            created_at=appointment.created_at,
            updated_at=appointment.updated_at,
        )
````

## File: Telesecreter_Application/appointment/queries/get_all_appointmens_query.py
````python
from Telesecreter_Domain.interfaces.i_appointment_repository import IAppointmentRepository
from Telesecreter_Application.appointment.dtos.appointment_dto import AppointmentDTO

class GetAllAppointmentsQuery:

    def __init__(self, appointment_repository: IAppointmentRepository):
        self._repository = appointment_repository

    def execute(self) -> list[AppointmentDTO]:
        appointments = self._repository.get_all()
        return [AppointmentDTO.from_entity(appointment) for appointment in appointments ]
````

## File: Telesecreter_Application/appointment/__init__.py
````python

````

## File: Telesecreter_Application/department/dtos/department_dto.py
````python
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class DepartmentDTO:
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime
    
    @staticmethod
    def from_entity(department) -> "DepartmentDTO":
        return DepartmentDTO(
            id=department.id,
            name=department.name,
            created_at=department.created_at,
            updated_at=department.updated_at,
        )
````

## File: Telesecreter_Application/department/queries/get_all_departments_query.py
````python
from Telesecreter_Domain.interfaces.i_department_repository import IDepartmentRepository
from Telesecreter_Application.department.dtos.department_dto import DepartmentDTO


class GetAllDepartmentsQuery:

    def __init__(self, department_repository: IDepartmentRepository):
        self._repository = department_repository

    def excecute(self) -> list[DepartmentDTO]:
        departments = self._repository.get_all()
        return [DepartmentDTO.from_entity(department) for department in departments]
````

## File: Telesecreter_Application/department/__init__.py
````python

````

## File: Telesecreter_Application/doctor/__init__.py
````python

````

## File: Telesecreter_Application/scheduale/dtos/scheduale_dto.py
````python
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class SchedualeDTO:
    id: UUID
    doctor_id: UUID
    day_of_week: str
    start_time: datetime
    end_time: datetime
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(scheduale) -> "SchedualeDTO":
        return SchedualeDTO(
            id=scheduale.id,
            doctor_id=scheduale.doctor_id,
            day_of_week=scheduale.day_of_week,
            start_time=scheduale.start_time,
            end_time=scheduale.end_time,
            created_at=scheduale.created_at,
            updated_at=scheduale.updated_at,
        )
````

## File: Telesecreter_Application/scheduale/queries/get_all_scheduales_query.py
````python
from Telesecreter_Domain.interfaces.i_scheduale_repository import IScheduleRepository
from Telesecreter_Application.scheduale.dtos import scheduale_dto

class GetAllSchedualesQuery:

    def __init__(self, scheduale_repository: IScheduleRepository):
        self._repository = scheduale_repository

    def execute(self) -> list[scheduale_dto.SchedualeDTO]:
        scheduales = self._repository.get_all()
        return [scheduale_dto.SchedualeDTO.from_entity(scheduale) for scheduale in scheduales]
````

## File: Telesecreter_Application/scheduale/__init__.py
````python

````

## File: Telesecreter_Application/user/dtos/user_dto.py
````python
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class UserDTO:
    id: UUID
    full_name: str
    phone_number: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(user) -> "UserDTO":
        return UserDTO(
            id=user.id,
            full_name=user.full_name,
            phone_number=user.phone_number,
            email=user.email,
            role=user.role.value,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
````

## File: Telesecreter_Application/user/queries/get_all_users_query.py
````python
from Telesecreter_Domain.interfaces.i_user_repository import IUserRepository
from Telesecreter_Application.user.dtos.user_dto import UserDTO


class GetAllUsersQuery:

    def __init__(self, user_repository: IUserRepository):
        self._repository = user_repository

    def execute(self) -> list[UserDTO]:
        users = self._repository.get_all()
        return [UserDTO.from_entity(user) for user in users]
````

## File: Telesecreter_Application/user/__init__.py
````python

````

## File: Telesecreter_Application/__init__.py
````python

````

## File: Telesecreter_Domain/common/base_entity.py
````python
import uuid
from datetime import datetime, timezone


class BaseEntity:
    def __init__(self, id: uuid.UUID | None = None):
        self.id: uuid.UUID = id or uuid.uuid4()
        self.created_at: datetime = datetime.now(timezone.utc)
        self.updated_at: datetime = datetime.now(timezone.utc)

    def set_updated(self) -> None:
        self.updated_at = datetime.now(timezone.utc)

    def __eq__(self, other) -> bool:
        if not isinstance(other, BaseEntity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
````

## File: Telesecreter_Domain/entities/appointments.py
````python
from uuid import UUID
from datetime import date, time
from typing import Optional
from Telesecreter_Domain.common.base_entity import BaseEntity
from Telesecreter_Domain.enums.appointment_status import AppointmentStatus


class Appointment(BaseEntity):
    def __init__(
        self,
        user_id: UUID,
        doctor_id: UUID,
        date: date,
        start_time: time,
        end_time: time,
        status: AppointmentStatus = AppointmentStatus.PENDING,
        notes: Optional[str] = None,
        cancelled_at: Optional[str] = None,
        cancellation_reason: Optional[str] = None,
        id: UUID | None = None,
    ):
        super().__init__(id)
        self.user_id = user_id
        self.doctor_id = doctor_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.cancelled_at = cancelled_at
        self.cancellation_reason = cancellation_reason
````

## File: Telesecreter_Domain/entities/department.py
````python
from Telesecreter_Domain.common.base_entity import BaseEntity
from uuid import UUID
 
 
class Department(BaseEntity):
    def __init__(
        self,
        name: str,
        id: UUID | None = None,
    ):
        super().__init__(id)
        self.name = name
````

## File: Telesecreter_Domain/entities/doctor.py
````python
from uuid import UUID
from typing import Optional
from Telesecreter_Domain.common.base_entity import BaseEntity


class Doctor(BaseEntity):
    def __init__(
        self,
        full_name: str,
        email: str,
        department_id: UUID,
        specialty: str,
        phone_number: str = "",
        ratings: Optional[float] = None,
        years_of_experience: int = 0,
        bio: Optional[str] = None,
        is_available: bool = True,
        id: UUID | None = None,
    ):
        super().__init__(id)
        ratings = ratings if ratings is not None else 0.0
        self.full_name = full_name
        self.email = email
        self.phone_number = phone_number
        self.department_id = department_id
        self.specialty = specialty
        self.is_available = is_available
````

## File: Telesecreter_Domain/entities/scheduale.py
````python
from uuid import UUID
from datetime import time
from Telesecreter_Domain.common.base_entity import BaseEntity


class DoctorSchedule(BaseEntity):
    def __init__(
        self,
        doctor_id: UUID,
        day_of_week: int,
        start_time: time,
        end_time: time,
        id: UUID | None = None,
    ):
        super().__init__(id)
        self.doctor_id = doctor_id
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time
````

## File: Telesecreter_Domain/entities/user.py
````python
from uuid import UUID
from Telesecreter_Domain.common.base_entity import BaseEntity
from Telesecreter_Domain.enums.user_role import UserRole

class User(BaseEntity):
    def __init__(
        self,
        full_name: str,
        phone_number: str,
        email: str,
        hashed_password: str,
        role: UserRole = UserRole.PATIENT,
        is_active: bool = True,
        id: UUID | None = None,
    ):
        super().__init__(id)
        self.full_name = full_name
        self.phone_number = phone_number
        self.email = email
        self.hashed_password = hashed_password
        self.role = role
        self.is_active = is_active
````

## File: Telesecreter_Domain/enums/appointment_status.py
````python
import enum


class AppointmentStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    RESCHEDULED = "rescheduled"
````

## File: Telesecreter_Domain/enums/user_role.py
````python
import enum


class UserRole(enum.Enum):
    PATIENT = "patient"
    ADMIN = "admin"
````

## File: Telesecreter_Domain/interfaces/__init__.py
````python

````

## File: Telesecreter_Domain/interfaces/i_appointment_repository.py
````python
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
````

## File: Telesecreter_Domain/interfaces/i_base_repository.py
````python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional
from uuid import UUID

T = TypeVar("T")


class IBaseRepository(ABC, Generic[T]):

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def add(self, entity: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError
````

## File: Telesecreter_Domain/interfaces/i_department_repository.py
````python
from abc import abstractmethod
from typing import Optional
from Telesecreter_Domain.interfaces.i_base_repository import IBaseRepository
from Telesecreter_Domain.entities.department import Department


class IDepartmentRepository(IBaseRepository[Department]):

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Department]:
        raise NotImplementedError
````

## File: Telesecreter_Domain/interfaces/i_doctor_repository.py
````python
from abc import abstractmethod
from typing import Optional
from uuid import UUID
from Telesecreter_Domain.interfaces.i_base_repository import IBaseRepository
from Telesecreter_Domain.entities.doctor import Doctor


class IDoctorRepository(IBaseRepository[Doctor]):

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Doctor]:
        raise NotImplementedError

    @abstractmethod
    def get_by_department(self, department_id: UUID) -> list[Doctor]:
        raise NotImplementedError

    @abstractmethod
    def get_available_doctors(self) -> list[Doctor]:
        raise NotImplementedError
````

## File: Telesecreter_Domain/interfaces/i_scheduale_repository.py
````python
from abc import abstractmethod
from uuid import UUID
from Telesecreter_Domain.interfaces.i_base_repository import IBaseRepository
from Telesecreter_Domain.entities.scheduale import DoctorSchedule


class IScheduleRepository(IBaseRepository[DoctorSchedule]):

    @abstractmethod
    def get_by_doctor(self, doctor_id: UUID) -> list[DoctorSchedule]:
        raise NotImplementedError

    @abstractmethod
    def get_by_doctor_and_day(self, doctor_id: UUID, day_of_week: int) -> list[DoctorSchedule]:
        raise
````

## File: Telesecreter_Domain/interfaces/i_user_repository.py
````python
from abc import abstractmethod
from typing import Optional
from uuid import UUID
from Telesecreter_Domain.interfaces.i_base_repository import IBaseRepository
from Telesecreter_Domain.entities.user import User


class IUserRepository(IBaseRepository[User]):

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_by_phone(self, phone_number: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_active_users(self) -> list[User]:
        raise NotImplementedError
````

## File: Telesecreter_Domain/__init__.py
````python

````

## File: Telesecreter_Infrastructure/data_access/configurations/common/__init__.py
````python

````

## File: Telesecreter_Infrastructure/data_access/configurations/common/base_model.py
````python
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


def utc_now():
    return datetime.now(timezone.utc)


class BaseModel(Base):
    """Abstract base for all ORM models — mirrors domain BaseEntity fields."""
    __abstract__ = True

    id = Column(String, primary_key=True, default=generate_uuid)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)
````

## File: Telesecreter_Infrastructure/data_access/configurations/models/__init__.py
````python

````

## File: Telesecreter_Infrastructure/data_access/configurations/models/appintment.py
````python
from sqlalchemy import Column, String, Date, Time, ForeignKey, Enum, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from Telesecreter_Infrastructure.data_access.configurations.common.base_model import BaseModel
from Telesecreter_Domain.enums.appointment_status import AppointmentStatus


class AppointmentModel(BaseModel):
    __tablename__ = "appointments"

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    doctor_id = Column(String, ForeignKey("doctors.id"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.PENDING, nullable=False)
    cancelled_at = Column(String, nullable=True)
    cancellation_reason = Column(String, nullable=True)

    user = relationship("UserModel", back_populates="appointments")
    doctor = relationship("DoctorModel", back_populates="appointments")

    __table_args__ = (
        Index("ix_appointment_user", "user_id"),
        Index("ix_appointment_doctor_date", "doctor_id", "date"),
        UniqueConstraint("doctor_id", "date", "start_time", name="uq_doctor_timeslot"),
    )
````

## File: Telesecreter_Infrastructure/data_access/configurations/models/schedual_model.py
````python
from sqlalchemy import Column, String, Integer, Time, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from Telesecreter_Infrastructure.data_access.configurations.common.base_model import BaseModel

class DoctorScheduleModel(BaseModel):
    __tablename__ = "doctor_schedules"

    doctor_id = Column(String, ForeignKey("doctors.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    doctor = relationship("DoctorModel", back_populates="schedules")

    __table_args__ = (
        Index("ix_schedule_doctor", "doctor_id"),
        UniqueConstraint("doctor_id", "day_of_week", name="uq_doctor_day"),
    )
````

## File: Telesecreter_Infrastructure/data_access/configurations/models/user_model.py
````python
from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.orm import relationship
from Telesecreter_Infrastructure.data_access.configurations.common.base_model import BaseModel
from Telesecreter_Domain.enums.user_role import UserRole


class UserModel(BaseModel):
    __tablename__ = "users"

    full_name       = Column(String, nullable=False)
    phone_number    = Column(String, unique=True, nullable=False)
    email           = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role            = Column(Enum(UserRole), nullable=False, default=UserRole.PATIENT)
    is_active       = Column(Boolean, default=True, nullable=False)

    appointments = relationship("AppointmentModel", back_populates="user")
````

## File: Telesecreter_Infrastructure/data_access/configurations/__init__.py
````python

````

## File: Telesecreter_Infrastructure/data_access/db/database.py
````python
import sqlite3
import logging
from pathlib import Path
from contextlib import contextmanager
 
logger = logging.getLogger(__name__)
 
# Resolves to TelesecreterV1/data/telesecreter.db
DB_PATH = Path(__file__).parents[3] / "data" / "telesecreter.db"
 
# Ensure the data directory exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
 
 
def get_connection() -> sqlite3.Connection:
    """
    Create and return a new SQLite connection.
    - Row factory set so rows behave like dicts (access by column name).
    - Foreign key enforcement enabled per connection.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
 
 
@contextmanager
def get_db():
    """
    Context manager that yields a connection and handles
    commit/rollback/close automatically.
 
    Usage:
        with get_db() as conn:
            conn.execute("INSERT INTO ...")
    """
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error("Database error, rolling back: %s", e)
        raise
    finally:
        conn.close()
 
 
def init_db(schema_path: Path | None = None) -> None:
    """
    Initialize the database by running a SQL schema file.
 
    Args:
        schema_path: Path to the .sql schema file.
                     Defaults to schema.sql in the same directory.
    """
    if schema_path is None:
        schema_path = Path(__file__).parent / "schema.sql"
 
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
 
    with get_db() as conn:
        sql = schema_path.read_text(encoding="utf-8")
        conn.executescript(sql)
 
    logger.info("Database initialized from %s", schema_path)
 
 
def check_connection() -> bool:
    """
    Quick health-check — returns True if the DB is reachable.
    """
    try:
        with get_db() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error("Database health-check failed: %s", e)
        return False
````

## File: Telesecreter_Infrastructure/data_access/migrations/versions/3eaebeceed60_add_department_id_to_doctors.py
````python
"""add department_id to doctors

Revision ID: 3eaebeceed60
Revises: c2a7cdd538a3
Create Date: 2026-04-05 14:12:26.773799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3eaebeceed60'
down_revision: Union[str, Sequence[str], None] = 'c2a7cdd538a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('doctors', schema=None) as batch_op:
        batch_op.add_column(sa.Column('department_id', sa.String(), nullable=False))
        batch_op.create_foreign_key('fk_doctors_department_id', 'departments', ['department_id'], ['id'])

def downgrade() -> None:
    with op.batch_alter_table('doctors', schema=None) as batch_op:
        batch_op.drop_constraint('fk_doctors_department_id', type_='foreignkey')
        batch_op.drop_column('department_id')
````

## File: Telesecreter_Infrastructure/data_access/migrations/versions/c2a7cdd538a3_initial_tables.py
````python
"""initial tables

Revision ID: c2a7cdd538a3
Revises: 
Create Date: 2026-04-05 13:54:28.967739

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2a7cdd538a3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('departments',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', name='uq_department_name')
    )
    op.create_table('doctors',
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('specialty', sa.String(), nullable=False),
    sa.Column('is_available', sa.Boolean(), nullable=False),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('users',
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('role', sa.Enum('PATIENT', 'ADMIN', name='userrole'), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number')
    )
    op.create_table('appointments',
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('doctor_id', sa.String(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'CONFIRMED', 'CANCELLED', 'COMPLETED', 'RESCHEDULED', name='appointmentstatus'), nullable=False),
    sa.Column('cancelled_at', sa.String(), nullable=True),
    sa.Column('cancellation_reason', sa.String(), nullable=True),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('doctor_id', 'date', 'start_time', name='uq_doctor_timeslot')
    )
    with op.batch_alter_table('appointments', schema=None) as batch_op:
        batch_op.create_index('ix_appointment_doctor_date', ['doctor_id', 'date'], unique=False)
        batch_op.create_index('ix_appointment_user', ['user_id'], unique=False)

    op.create_table('doctor_schedules',
    sa.Column('doctor_id', sa.String(), nullable=False),
    sa.Column('day_of_week', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('doctor_id', 'day_of_week', name='uq_doctor_day')
    )
    with op.batch_alter_table('doctor_schedules', schema=None) as batch_op:
        batch_op.create_index('ix_schedule_doctor', ['doctor_id'], unique=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('doctor_schedules', schema=None) as batch_op:
        batch_op.drop_index('ix_schedule_doctor')

    op.drop_table('doctor_schedules')
    with op.batch_alter_table('appointments', schema=None) as batch_op:
        batch_op.drop_index('ix_appointment_user')
        batch_op.drop_index('ix_appointment_doctor_date')

    op.drop_table('appointments')
    op.drop_table('users')
    op.drop_table('doctors')
    op.drop_table('departments')
    # ### end Alembic commands ###
````

## File: Telesecreter_Infrastructure/data_access/migrations/env.py
````python
import sys
from pathlib import Path

# Add project root (TelesecreterV1/) to Python path
sys.path.insert(0, str(Path(__file__).parents[3]))

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from Telesecreter_Infrastructure.data_access.configurations.common.base_model import Base
from Telesecreter_Infrastructure.data_access.configurations.models.department_model import DepartmentModel  # noqa: F401
from Telesecreter_Infrastructure.data_access.configurations.models.user_model import UserModel              # noqa: F401
from Telesecreter_Infrastructure.data_access.configurations.models.doctor_model import DoctorModel          # noqa: F401
from Telesecreter_Infrastructure.data_access.configurations.models.schedual_model import DoctorScheduleModel  # noqa: F401
from Telesecreter_Infrastructure.data_access.configurations.models.appintment import AppointmentModel       # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
````

## File: Telesecreter_Infrastructure/data_access/migrations/README
````
Generic single-database configuration.
````

## File: Telesecreter_Infrastructure/data_access/migrations/script.py.mako
````
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, Sequence[str], None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    """Upgrade schema."""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Downgrade schema."""
    ${downgrades if downgrades else "pass"}
````

## File: Telesecreter_Infrastructure/data_access/repositories/appointment_repository.py
````python
from datetime import date
from uuid import UUID
from Telesecreter_Domain.interfaces.i_appointment_repository import IAppointmentRepository
from Telesecreter_Domain.entities.appointments import Appointment
from Telesecreter_Domain.enums.appointment_status import AppointmentStatus
from Telesecreter_Infrastructure.data_access.configurations.models.appintment import AppointmentModel
from Telesecreter_Infrastructure.data_access.repositories.repository import GenericRepository
from Telesecreter_Infrastructure.data_access.db.database import get_db


def _map(row) -> Appointment:
    return Appointment(
        id=row["id"],
        user_id=row["user_id"],
        doctor_id=row["doctor_id"],
        date=row["date"],
        start_time=row["start_time"],
        end_time=row["end_time"],
        status=AppointmentStatus(row["status"]),
        notes=row["notes"] if "notes" in row.keys() else None,
        cancelled_at=row["cancelled_at"],
        cancellation_reason=row["cancellation_reason"],
    )


class AppointmentRepository(GenericRepository[Appointment, AppointmentModel], IAppointmentRepository):

    def __init__(self):
        super().__init__(AppointmentModel, _map)

    def get_by_user(self, user_id: UUID) -> list[Appointment]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM appointments WHERE user_id = ?", (str(user_id),)).fetchall()
            return [_map(row) for row in rows]

    def get_by_doctor(self, doctor_id: UUID) -> list[Appointment]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM appointments WHERE doctor_id = ?", (str(doctor_id),)).fetchall()
            return [_map(row) for row in rows]

    def get_by_doctor_and_date(self, doctor_id: UUID, date: date) -> list[Appointment]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM appointments WHERE doctor_id = ? AND date = ?",
                (str(doctor_id), str(date))
            ).fetchall()
            return [_map(row) for row in rows]

    def get_by_status(self, status: AppointmentStatus) -> list[Appointment]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM appointments WHERE status = ?", (status.value,)).fetchall()
            return [_map(row) for row in rows]
````

## File: Telesecreter_Infrastructure/data_access/repositories/department_repository.py
````python
from typing import Optional
from Telesecreter_Domain.interfaces.i_department_repository import IDepartmentRepository
from Telesecreter_Domain.entities.department import Department
from Telesecreter_Infrastructure.data_access.configurations.models.department_model import DepartmentModel
from Telesecreter_Infrastructure.data_access.repositories.repository import GenericRepository
from Telesecreter_Infrastructure.data_access.db.database import get_db


def _map(row) -> Department:
    return Department(
        id=row["id"],
        name=row["name"],
    )


class DepartmentRepository(GenericRepository[Department, DepartmentModel], IDepartmentRepository):

    def __init__(self):
        super().__init__(DepartmentModel, _map)

    def get_by_name(self, name: str) -> Optional[Department]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM departments WHERE name = ?", (name,)).fetchone()
            return _map(row) if row else None
````

## File: Telesecreter_Infrastructure/data_access/repositories/repository.py
````python
from typing import Generic, TypeVar, Optional, Type
from uuid import UUID
from Telesecreter_Infrastructure.data_access.db.database import get_db
from Telesecreter_Domain.interfaces.i_base_repository import IBaseRepository

T = TypeVar("T")
M = TypeVar("M")


class GenericRepository(IBaseRepository[T], Generic[T, M]):
    """
    Generic SQLite repository.
    T = Domain entity type
    M = SQLAlchemy model type
    """

    def __init__(self, model_class: Type[M], mapper):
        self._model = model_class
        self._mapper = mapper  # callable: model -> entity

    def get_by_id(self, id: UUID) -> Optional[T]:
        with get_db() as conn:
            row = conn.execute(
                f"SELECT * FROM {self._model.__tablename__} WHERE id = ?", (str(id),)
            ).fetchone()
            return self._mapper(row) if row else None

    def get_all(self) -> list[T]:
        with get_db() as conn:
            rows = conn.execute(
                f"SELECT * FROM {self._model.__tablename__}"
            ).fetchall()
            return [self._mapper(row) for row in rows]

    def add(self, entity: T) -> T:
        data = vars(entity)
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        values = [str(v) if not isinstance(v, (int, float, bool, type(None))) else v for v in data.values()]
        with get_db() as conn:
            conn.execute(
                f"INSERT INTO {self._model.__tablename__} ({columns}) VALUES ({placeholders})",
                values
            )
        return entity

    def update(self, entity: T) -> T:
        data = {k: v for k, v in vars(entity).items() if k != "id"}
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        values = [str(v) if not isinstance(v, (int, float, bool, type(None))) else v for v in data.values()]
        values.append(str(entity.id))
        with get_db() as conn:
            conn.execute(
                f"UPDATE {self._model.__tablename__} SET {set_clause} WHERE id = ?",
                values
            )
        return entity

    def delete(self, id: UUID) -> None:
        with get_db() as conn:
            conn.execute(
                f"DELETE FROM {self._model.__tablename__} WHERE id = ?", (str(id),)
            )
````

## File: Telesecreter_Infrastructure/data_access/__init__.py
````python

````

## File: Telesecreter_Infrastructure/seeds/db_seeds.py
````python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2]))

from datetime import date, time
from Telesecreter_Infrastructure.data_access.configurations.common.base_model import Base
from Telesecreter_Infrastructure.data_access.configurations.models.department_model import DepartmentModel
from Telesecreter_Infrastructure.data_access.configurations.models.doctor_model import DoctorModel
from Telesecreter_Infrastructure.data_access.configurations.models.user_model import UserModel
from Telesecreter_Infrastructure.data_access.configurations.models.schedual_model import DoctorScheduleModel
from Telesecreter_Infrastructure.data_access.configurations.models.appintment import AppointmentModel
from Telesecreter_Domain.enums.user_role import UserRole
from Telesecreter_Domain.enums.appointment_status import AppointmentStatus
from Telesecreter_Infrastructure.data_access.db.database import get_db
import uuid


def seed():
    with get_db() as conn:
        try:
            # 1. Departments
            departments = [
                {"id": str(uuid.uuid4()), "name": "General Practice"},
                {"id": str(uuid.uuid4()), "name": "Cardiology"},
                {"id": str(uuid.uuid4()), "name": "Neurology"},
                {"id": str(uuid.uuid4()), "name": "Orthopedics"},
            ]
            conn.executemany(
                "INSERT INTO departments (id, name, created_at, updated_at) VALUES (:id, :name, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
                departments
            )
            print("✅ Departments added")

            # 2. Doctors
            doctors = [
                {"id": str(uuid.uuid4()), "full_name": "Dr. John Smith",   "email": "john.smith@hospital.com",   "phone_number": "+1234567890", "department_id": departments[0]["id"], "specialty": "General Medicine", "is_available": 1, "rating": 4.5},
                {"id": str(uuid.uuid4()), "full_name": "Dr. Sarah Connor",  "email": "sarah.connor@hospital.com",  "phone_number": "+1234567891", "department_id": departments[1]["id"], "specialty": "Cardiology",       "is_available": 1, "rating": 4.9},
                {"id": str(uuid.uuid4()), "full_name": "Dr. Emily Davis",   "email": "emily.davis@hospital.com",   "phone_number": "+1234567892", "department_id": departments[2]["id"], "specialty": "Neurology",        "is_available": 1, "rating": 3.8},
                {"id": str(uuid.uuid4()), "full_name": "Dr. James Wilson",  "email": "james.wilson@hospital.com",  "phone_number": "+1234567893", "department_id": departments[3]["id"], "specialty": "Orthopedics",      "is_available": 1, "rating": 4.2},
            ]
            conn.executemany(
                """INSERT INTO doctors (id, full_name, email, phone_number, department_id, specialty, is_available, rating, created_at, updated_at)
                   VALUES (:id, :full_name, :email, :phone_number, :department_id, :specialty, :is_available, :rating, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""",
                doctors
            )
            print("✅ Doctors added")

            # 3. Schedules (Mon-Fri, 09:00-17:00 for each doctor)
            schedules = [
                {"id": str(uuid.uuid4()), "doctor_id": doctor["id"], "day_of_week": day, "start_time": "09:00:00", "end_time": "17:00:00"}
                for doctor in doctors
                for day in range(0, 5)
            ]
            conn.executemany(
                """INSERT INTO doctor_schedules (id, doctor_id, day_of_week, start_time, end_time, created_at, updated_at)
                   VALUES (:id, :doctor_id, :day_of_week, :start_time, :end_time, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""",
                schedules
            )
            print("✅ Schedules added")

            # 4. Users
            users = [
                {"id": str(uuid.uuid4()), "full_name": "Alice Johnson", "email": "alice@example.com", "phone_number": "+9876543210", "hashed_password": "hashed_password_here", "role": UserRole.PATIENT.value, "is_active": 1},
                {"id": str(uuid.uuid4()), "full_name": "Bob Williams",  "email": "bob@example.com",   "phone_number": "+9876543211", "hashed_password": "hashed_password_here", "role": UserRole.PATIENT.value, "is_active": 1},
            ]
            conn.executemany(
                """INSERT INTO users (id, full_name, email, phone_number, hashed_password, role, is_active, created_at, updated_at)
                   VALUES (:id, :full_name, :email, :phone_number, :hashed_password, :role, :is_active, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""",
                users
            )
            print("✅ Users added")

            # 5. Appointments
            appointments = [
                {"id": str(uuid.uuid4()), "user_id": users[0]["id"], "doctor_id": doctors[0]["id"], "date": "2026-04-10", "start_time": "09:00:00", "end_time": "09:30:00", "status": AppointmentStatus.CONFIRMED.value},
                {"id": str(uuid.uuid4()), "user_id": users[0]["id"], "doctor_id": doctors[1]["id"], "date": "2026-04-14", "start_time": "10:00:00", "end_time": "10:30:00", "status": AppointmentStatus.PENDING.value},
                {"id": str(uuid.uuid4()), "user_id": users[1]["id"], "doctor_id": doctors[2]["id"], "date": "2026-04-11", "start_time": "11:00:00", "end_time": "11:30:00", "status": AppointmentStatus.PENDING.value},
                {"id": str(uuid.uuid4()), "user_id": users[1]["id"], "doctor_id": doctors[3]["id"], "date": "2026-04-15", "start_time": "14:00:00", "end_time": "14:30:00", "status": AppointmentStatus.CONFIRMED.value},
            ]
            conn.executemany(
                """INSERT INTO appointments (id, user_id, doctor_id, date, start_time, end_time, status, created_at, updated_at)
                   VALUES (:id, :user_id, :doctor_id, :date, :start_time, :end_time, :status, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""",
                appointments
            )
            print("✅ Appointments added")

            print("🎉 All seed data inserted successfully")

        except Exception as e:
            print(f"❌ Error: {e}")
            raise


if __name__ == "__main__":
    seed()
````

## File: Telesecreter_Infrastructure/__init__.py
````python

````

## File: .gitignore
````
# Python cache
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.so

# Virtual environment
venv1/
.venv/a
venv/
ENV/
env/
*.env

# Jupyter Notebook checkpoints
.ipynb_checkpoints/

# VSCode / PyCharm
.vscode/
.idea/

# Logs
*.log
logs/
*.out
*.err

# Data
model/data/
*.csv
*.tsv
*.json

# Model checkpoints
model/checkpoints/
*.bin
*.pt
*.ckpt
*.h5

# OS files
.DS_Store
Thumbs.db

# Build / distribution
build/
dist/
*.egg-info/
````

## File: alembic.ini
````ini
[alembic]
script_location = Telesecreter_Infrastructure/data_access/migrations
sqlalchemy.url = sqlite:///data/telesecreter.db

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
````

## File: requirements.txt
````
fastapi
uvicorn[standard]
python-multipart
pydantic>=2
SQLAlchemy>=2
alembic
python-dotenv
twilio
httpx
# v2 için (kendi STT/TTS)
faster-whisper
coqpit
# TTS (Temporarily disabled - requires Python < 3.12)
# soundfile
# numpy
# torch
# transformers
# kokoro
# soundfile
fastapi
````

## File: todo.txt
````
endpoints level 1
-get doctors,departments,appointments,scheduales

endpoints level 2
-get by id;users,doctorsdepartments,scheduales,appointments

endpoints level 3
get by name;users,doctorsdepartments,scheduales,appointments

endpoints level 4
update;users,doctorsdepartments,scheduales,appointments

endpoint levl 5
delete;users,doctorsdepartments,scheduales,appointments

webhook;
-get doctors scheduale webhook
-book appointment webhook
-cancel appointment webhook


Webhook Adı,Görevi,Neden Önemli?
search_doctor,Semptom -> Departman -> Doktor (Rating'e göre),"Projenin ""Zekası"""
check_slots,Seçilen doktorun boş saatlerini getirir,"Projenin ""Fonksiyonu"""
confirm_booking,Randevuyu Appointments tablosuna INSERT eder,"Projenin ""Bütünlüğü"""


gorevler
-ilk olarak bul endpointlerin nasil calisr iclerinde nevar
-sora ekle book appointment,reccomend doctor by symphtom
-sora ekle confirm appointment email
-sora ekle reschedual appointment


ne yaptik;
get all endpointii yazdik herbir entity icin 
simdi lazim set appointment, recommend doctor yapalim calissin webhookle
zamana gore diger endpointleri de yazalim
````

## File: Telesecreter_Application/doctor/dtos/doctor_dto.py
````python
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class DoctorDTO:
    id: UUID
    full_name: str
    speciality: str
    phone_number: str
    email: str
    is_available: bool
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(doctor) -> "DoctorDTO":
        return DoctorDTO(
            id=doctor.id,
            full_name=doctor.full_name,
            speciality=doctor.specialty,
            phone_number=doctor.phone_number,
            email=doctor.email,
            is_available=doctor.is_available,
            created_at=doctor.created_at,
            updated_at=doctor.updated_at,
        )
````

## File: Telesecreter_Application/doctor/queries/get_all_doctors_query.py
````python
from Telesecreter_Domain.interfaces.i_doctor_repository import IDoctorRepository
from Telesecreter_Application.doctor.dtos.doctor_dto import DoctorDTO

class GetAllDoctorsQuery:

    def __init__(self,doctor_repository: IDoctorRepository):
        self._repository = doctor_repository

    def execute(self) -> list[DoctorDTO]:
        doctors = self._repository.get_all()
        return [DoctorDTO.from_entity(doctor) for doctor in doctors]
````

## File: Telesecreter_Infrastructure/data_access/configurations/models/department_model.py
````python
from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.orm import relationship
from Telesecreter_Infrastructure.data_access.configurations.common.base_model import BaseModel


class DepartmentModel(BaseModel):
    __tablename__ = "departments"

    name = Column(String, nullable=False)

    doctors = relationship("DoctorModel", back_populates="department")

    __table_args__ = (
        UniqueConstraint("name", name="uq_department_name"),
    )

    @property
    def doctor_ids(self) -> list[str]:
        return [doctor.id for doctor in self.doctors]
````

## File: Telesecreter_Infrastructure/data_access/configurations/models/doctor_model.py
````python
from sqlalchemy import Column, ForeignKey, String, Boolean, Float
from sqlalchemy.orm import relationship
from Telesecreter_Infrastructure.data_access.configurations.common.base_model import BaseModel


class DoctorModel(BaseModel):
    __tablename__ = "doctors"

    full_name    = Column(String, nullable=False)
    email        = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=True, default="")
    department_id = Column(String, ForeignKey("departments.id"), nullable=False)
    specialty    = Column(String, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    rating       = Column(Float, nullable=True, default=None)

    department   = relationship("DepartmentModel", back_populates="doctors")
    appointments = relationship("AppointmentModel", back_populates="doctor")
    schedules    = relationship("DoctorScheduleModel", back_populates="doctor")
````

## File: Telesecreter_Infrastructure/data_access/repositories/scheduale_repository.py
````python
from uuid import UUID
from Telesecreter_Domain.interfaces.i_scheduale_repository import IScheduleRepository
from Telesecreter_Domain.entities.scheduale import DoctorSchedule
from Telesecreter_Infrastructure.data_access.configurations.models.schedual_model import DoctorScheduleModel
from Telesecreter_Infrastructure.data_access.repositories.repository import GenericRepository
from Telesecreter_Infrastructure.data_access.db.database import get_db


def _map(row) -> DoctorSchedule:
    return DoctorSchedule(
        id=row["id"],
        doctor_id=row["doctor_id"],
        day_of_week=row["day_of_week"],
        start_time=row["start_time"],
        end_time=row["end_time"],
    )


class ScheduleRepository(GenericRepository[DoctorSchedule, DoctorScheduleModel], IScheduleRepository):

    def __init__(self):
        super().__init__(DoctorScheduleModel, _map)

    def get_by_doctor(self, doctor_id: UUID) -> list[DoctorSchedule]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM doctor_schedules WHERE doctor_id = ?", (str(doctor_id),)).fetchall()
            return [_map(row) for row in rows]

    def get_by_doctor_and_day(self, doctor_id: UUID, day_of_week: int) -> list[DoctorSchedule]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM doctor_schedules WHERE doctor_id = ? AND day_of_week = ?",
                (str(doctor_id), day_of_week)
            ).fetchall()
            return [_map(row) for row in rows]
````

## File: Telesecreter_Infrastructure/data_access/repositories/user_repository.py
````python
from typing import Optional
from uuid import UUID
from Telesecreter_Domain.interfaces.i_user_repository import IUserRepository
from Telesecreter_Domain.entities.user import User
from Telesecreter_Domain.enums.user_role import UserRole
from Telesecreter_Infrastructure.data_access.configurations.models.user_model import UserModel
from Telesecreter_Infrastructure.data_access.repositories.repository import GenericRepository
from Telesecreter_Infrastructure.data_access.db.database import get_db


def _map(row) -> User:
    return User(
        id=row["id"],
        full_name=row["full_name"],
        phone_number=row["phone_number"],
        email=row["email"],
        hashed_password=row["hashed_password"],
        role=UserRole(row["role"]),
        is_active=bool(row["is_active"]),
    )


class UserRepository(GenericRepository[User, UserModel], IUserRepository):

    def __init__(self):
        super().__init__(UserModel, _map)

    def get_by_email(self, email: str) -> Optional[User]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            return _map(row) if row else None

    def get_by_phone(self, phone_number: str) -> Optional[User]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM users WHERE phone_number = ?", (phone_number,)).fetchone()
            return _map(row) if row else None

    def get_active_users(self) -> list[User]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM users WHERE is_active = 1").fetchall()
            return [_map(row) for row in rows]
````

## File: Telesecreter_API/routers/doctor_controller.py
````python
from fastapi import APIRouter, Depends

from Telesecreter_Domain.interfaces.i_doctor_repository import IDoctorRepository
from Telesecreter_Application.doctor.dtos.doctor_dto import DoctorDTO
from Telesecreter_Application.doctor.queries.get_all_doctors_query import GetAllDoctorsQuery
from Telesecreter_API.dependencies.dependency_injection import get_doctor_repo

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.get("/", response_model=list[DoctorDTO])
def get_all_doctors(repo: IDoctorRepository = Depends(get_doctor_repo)):
    return GetAllDoctorsQuery(repo).execute()
````

## File: Telesecreter_API/routers/user_controller.py
````python
from fastapi import APIRouter, Depends

from Telesecreter_Domain.interfaces.i_user_repository import IUserRepository
from Telesecreter_Application.user.dtos.user_dto import UserDTO
from Telesecreter_Application.user.queries.get_all_users_query import GetAllUsersQuery
from Telesecreter_API.dependencies.dependency_injection import get_user_repo

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserDTO])
def get_all_users(repo: IUserRepository = Depends(get_user_repo)):
    return GetAllUsersQuery(repo).execute()
````

## File: Telesecreter_Infrastructure/data_access/repositories/doctor_repository.py
````python
from typing import Optional
from uuid import UUID
from Telesecreter_Domain.interfaces.i_doctor_repository import IDoctorRepository
from Telesecreter_Domain.entities.doctor import Doctor
from Telesecreter_Infrastructure.data_access.configurations.models.doctor_model import DoctorModel
from Telesecreter_Infrastructure.data_access.repositories.repository import GenericRepository
from Telesecreter_Infrastructure.data_access.db.database import get_db


def _map(row) -> Doctor:
    return Doctor(
        id=row["id"],
        full_name=row["full_name"],
        email=row["email"],
        phone_number=row["phone_number"],
        department_id=row["department_id"],
        specialty=row["specialty"],
        is_available=bool(row["is_available"]),
        ratings=row["rating"],
    )


class DoctorRepository(GenericRepository[Doctor, DoctorModel], IDoctorRepository):

    def __init__(self):
        super().__init__(DoctorModel, _map)

    def get_by_email(self, email: str) -> Optional[Doctor]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM doctors WHERE email = ?", (email,)).fetchone()
            return _map(row) if row else None

    def get_by_department(self, department_id: UUID) -> list[Doctor]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM doctors WHERE department_id = ?", (str(department_id),)).fetchall()
            return [_map(row) for row in rows]

    def get_available_doctors(self) -> list[Doctor]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM doctors WHERE is_available = 1").fetchall()
            return [_map(row) for row in rows]
````

## File: Telesecreter_API/main.py
````python
import sys
import os
from fastapi import FastAPI

# Ensure the backend directory is in the Python path so it can import Telesecretary namespace properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Telesecreter_API.routers import doctor_controller, user_controller,department_controller,appointment_controller,scheduale_controller


app = FastAPI(
    title="Telesecretary API",
    description="Backend API for the Telesecretary application",
    version="1.0.0"
)

# Connect all routers
app.include_router(user_controller.router)
app.include_router(doctor_controller.router)
app.include_router(department_controller.router)
app.include_router(appointment_controller.router)
app.include_router(scheduale_controller.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Telesecretary API! Visit /docs for Swagger documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
````