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
