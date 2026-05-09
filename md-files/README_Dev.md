# TelesecreterV1

A telemedicine appointment management system with a FastAPI backend and a React frontend. The system enables booking, managing, and viewing medical appointments through a voice-AI-ready webhook layer and a full calendar UI.

---

## Table of Contents

1. [Overview](#overview)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Architecture](#architecture)
5. [Domain Model](#domain-model)
6. [Database Schema](#database-schema)
7. [API Reference](#api-reference)
8. [Frontend](#frontend)
9. [Getting Started](#getting-started)
10. [Roadmap](#roadmap)

---

## Overview

TelesecreterV1 is split into two independent parts:

| Part | Technology | Purpose |
|------|-----------|---------|
| `Telesecreter_*` packages | Python / FastAPI | REST API backend |
| `frontend/` | React / Vite | Calendar dashboard UI |

The backend is designed for a voice-AI telephone secretary: a Retell/Twilio phone agent calls the webhook endpoints to search for a doctor, check availability, and confirm a booking on behalf of the patient. The frontend gives clinic staff a real-time appointment calendar.

---

## Tech Stack

### Backend
- **Python 3.11+**
- **FastAPI** — HTTP framework with automatic OpenAPI docs
- **SQLAlchemy 2** — ORM (models only, query execution uses raw sqlite3)
- **Alembic** — database migrations
- **SQLite** — database (`data/telesecreter.db`)
- **Twilio / faster-whisper / httpx** — telephony and audio integrations (planned)

### Frontend
- **React 18** with Vite
- **Framer Motion** — animations (appointment drawer)
- **Lucide React** — icons

---

## Project Structure

```
TelesecreterV1/
├── Telesecreter_API/               # Presentation layer
│   ├── dependencies/
│   │   └── dependency_injection.py # Factory functions for FastAPI Depends()
│   ├── routers/                    # FastAPI route handlers (thin controllers)
│   │   ├── appointment_controller.py
│   │   ├── department_controller.py
│   │   ├── doctor_controller.py
│   │   ├── scheduale_controller.py
│   │   └── user_controller.py
│   └── main.py                     # App factory, CORS, router registration
│
├── Telesecreter_Application/       # Application layer (CQRS)
│   ├── appointment/
│   │   ├── dtos/appointment_dto.py
│   │   └── queries/get_all_appointmens_query.py
│   ├── department/
│   ├── doctor/
│   ├── scheduale/
│   └── user/
│
├── Telesecreter_Domain/            # Domain layer (pure Python, no I/O)
│   ├── common/base_entity.py       # id, created_at, updated_at
│   ├── entities/                   # Domain entity classes
│   ├── enums/                      # AppointmentStatus, UserRole
│   └── interfaces/                 # Abstract repository contracts
│
├── Telesecreter_Infrastructure/    # Infrastructure layer
│   └── data_access/
│       ├── configurations/
│       │   ├── common/base_model.py  # SQLAlchemy BaseModel
│       │   └── models/               # ORM model classes
│       ├── db/database.py            # SQLite connection, context manager
│       ├── migrations/               # Alembic versions
│       └── repositories/             # Concrete repository implementations
│
├── frontend/                       # React dashboard
│   └── src/
│       ├── components/calendar/    # Calendar UI components
│       ├── hooks/                  # Data-fetching hooks
│       ├── pages/CalendarPage.jsx
│       └── utils/
│
├── data/telesecreter.db            # SQLite database file
├── alembic.ini
├── requirements.txt
└── todo.txt
```

---

## Architecture

The backend follows **Clean Architecture** with four strictly separated layers. Dependencies only point inward (API → Application → Domain ← Infrastructure).

```
┌─────────────────────────────────────────────┐
│  Telesecreter_API  (FastAPI routers)         │  ← HTTP in/out
│  • No business logic                         │
│  • Calls Query/Command objects via Depends() │
└────────────────────┬────────────────────────┘
                     │
┌────────────────────▼────────────────────────┐
│  Telesecreter_Application  (CQRS queries)    │  ← Business logic
│  • Query classes execute use-cases           │
│  • Maps entities → DTOs                      │
└────────────────────┬────────────────────────┘
                     │
┌────────────────────▼────────────────────────┐
│  Telesecreter_Domain  (pure Python)          │  ← Core model
│  • Entity classes                            │
│  • Abstract repository interfaces            │
│  • Enums                                     │
└────────────────────┬────────────────────────┘
                     │ implements
┌────────────────────▼────────────────────────┐
│  Telesecreter_Infrastructure  (I/O)          │  ← Data access
│  • SQLAlchemy ORM models                     │
│  • GenericRepository + concrete repos        │
│  • Alembic migrations                        │
└─────────────────────────────────────────────┘
```

### Request Flow

```
HTTP Request
  → FastAPI Router
    → Query class (e.g. GetAllDoctorsQuery)
      → IRepository interface
        → Repository implementation (sqlite3)
          → SQLite DB
            → Domain entity (via _map function)
              → DTO (via from_entity)
                → JSON Response
```

### Key Patterns

**Repository Pattern** — `Telesecreter_Domain/interfaces/` defines abstract `IBaseRepository[T]` with `get_by_id`, `get_all`, `add`, `update`, `delete`. Each resource extends it with domain-specific methods. `GenericRepository` in Infrastructure implements the base CRUD using raw sqlite3 strings against the SQLAlchemy model's `__tablename__`.

**CQRS-style Queries** — Each read use-case is a class with an `execute()` method. The router calls it and never touches the repository directly. Write operations (commands) are planned but not yet implemented.

**DTO mapping** — Each DTO has a `from_entity(entity)` static method. Entities are never serialised directly to JSON; the router declares `response_model=list[XyzDTO]`.

**Dependency Injection** — `dependency_injection.py` provides zero-argument factory functions (`get_doctor_repo`, etc.) wired through FastAPI's `Depends()`. Swapping a repository implementation only requires changing one line there.

---

## Domain Model

### Entities

#### BaseEntity
All entities extend `BaseEntity`.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `UUID` | Auto-generated UUID4 |
| `created_at` | `datetime` | UTC timestamp |
| `updated_at` | `datetime` | UTC timestamp, updated on change |

#### User

| Field | Type | Notes |
|-------|------|-------|
| `full_name` | `str` | |
| `phone_number` | `str` | Unique |
| `email` | `str` | Unique |
| `hashed_password` | `str` | |
| `role` | `UserRole` | `PATIENT` or `ADMIN` |
| `is_active` | `bool` | Default `True` |

#### Doctor

| Field | Type | Notes |
|-------|------|-------|
| `full_name` | `str` | |
| `email` | `str` | Unique |
| `phone_number` | `str` | |
| `department_id` | `UUID` | FK → Department |
| `specialty` | `str` | |
| `ratings` | `float` | 0–5, used for sorting in search |
| `is_available` | `bool` | Default `True` |

#### Department

| Field | Type |
|-------|------|
| `name` | `str` (unique) |

#### Appointment

| Field | Type | Notes |
|-------|------|-------|
| `user_id` | `UUID` | FK → User |
| `doctor_id` | `UUID` | FK → Doctor |
| `date` | `date` | |
| `start_time` | `time` | |
| `end_time` | `time` | |
| `status` | `AppointmentStatus` | Default `PENDING` |
| `cancelled_at` | `str?` | ISO timestamp |
| `cancellation_reason` | `str?` | |

#### DoctorSchedule

| Field | Type | Notes |
|-------|------|-------|
| `doctor_id` | `UUID` | FK → Doctor |
| `day_of_week` | `int` | 0 = Monday … 6 = Sunday |
| `start_time` | `time` | |
| `end_time` | `time` | |

### Enums

**AppointmentStatus**: `PENDING` · `CONFIRMED` · `CANCELLED` · `COMPLETED` · `RESCHEDULED`

**UserRole**: `PATIENT` · `ADMIN`

### Entity Relationships

```
Department ─< Doctor ─< DoctorSchedule
                │
                └─< Appointment >─ User
```

---

## Database Schema

SQLite file: `data/telesecreter.db`

Migrations are in `Telesecreter_Infrastructure/data_access/migrations/versions/`.

| Table | Key constraints |
|-------|----------------|
| `departments` | `UNIQUE(name)` |
| `doctors` | `UNIQUE(email)`, FK `department_id → departments.id` |
| `users` | `UNIQUE(email)`, `UNIQUE(phone_number)` |
| `appointments` | `UNIQUE(doctor_id, date, start_time)` — one slot per doctor, FK `user_id`, `doctor_id` |
| `doctor_schedules` | `UNIQUE(doctor_id, day_of_week)` — one schedule entry per doctor per day |

Indexes: `ix_appointment_user(user_id)`, `ix_appointment_doctor_date(doctor_id, date)`, `ix_schedule_doctor(doctor_id)`.

---

## API Reference

Base URL: `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

### Utility

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check / welcome message |
| `GET` | `/today` | Returns today's date |

### Doctors — `GET /doctors/`

Returns all doctors.

**Response** `200 OK`
```json
[
  {
    "id": "uuid",
    "full_name": "Dr. John Smith",
    "email": "john.smith@hospital.com",
    "specialty": "General Medicine",
    "department_id": "uuid",
    "is_available": true,
    "created_at": "...",
    "updated_at": "..."
  }
]
```

### Users — `GET /users/`

Returns all users.

### Departments — `GET /departments/`

Returns all departments.

### Appointments — `GET /appointments/`

Returns all appointments.

### Schedules — `GET /scheduales/`

Returns all doctor schedules.

> **Note:** The intentional spelling "scheduales" is used throughout the codebase for consistency with the original naming.

### Repository-level query methods (not yet exposed as endpoints)

These are implemented in the repository layer and ready to wire up:

| Repository | Method | Purpose |
|-----------|--------|---------|
| `AppointmentRepository` | `get_by_user(user_id)` | All appointments for a user |
| `AppointmentRepository` | `get_by_doctor(doctor_id)` | All appointments for a doctor |
| `AppointmentRepository` | `get_by_doctor_and_date(doctor_id, date)` | Availability check |
| `AppointmentRepository` | `get_by_status(status)` | Filter by status |
| `DoctorRepository` | `get_by_email(email)` | Look up doctor |
| `DoctorRepository` | `get_by_department(department_id)` | Doctors in department |
| `DoctorRepository` | `get_available_doctors()` | Only available doctors |
| `DepartmentRepository` | `get_by_name(name)` | Exact department name match |
| `ScheduleRepository` | `get_by_doctor(doctor_id)` | All schedules for a doctor |
| `ScheduleRepository` | `get_by_doctor_and_day(doctor_id, day)` | Specific day availability |
| `UserRepository` | `get_by_email(email)` | Look up user |
| `UserRepository` | `get_by_phone(phone_number)` | Look up user by phone |
| `UserRepository` | `get_active_users()` | Active users only |

---

## Frontend

Located in `frontend/`. A React + Vite calendar dashboard that connects to the backend REST API.

### Pages

**`CalendarPage`** (`src/pages/CalendarPage.jsx`) — The main view. Manages view mode, date navigation, doctor filter, and selected appointment state. Renders a two-column layout: calendar area on the left, right rail with today's agenda and AI activity stats.

### Calendar Components (`src/components/calendar/`)

| Component | Description |
|-----------|-------------|
| `CalendarToolbar` | Date navigation (prev/next/today), view switcher (week/day/list), doctor filter dropdown |
| `WeekCalendar` | 7-column time-grid showing appointments as positioned blocks for the selected week |
| `DayView` | Single-day time-grid, same layout as week but one column |
| `ListView` | Flat list of upcoming appointments, sorted by date |
| `AppointmentDrawer` | Animated side drawer (Framer Motion) showing appointment details: doctor, patient ID, status pill, date/time, actions (Reschedule / Cancel) |
| `TodayAgenda` | Right-rail card showing today's appointments at a glance |
| `AIStatsCard` | Right-rail card showing total booked, confirmed count, and confirmed rate — derived live from the appointments API |
| `DoctorLegend` | Color-coded legend mapping doctors to their calendar colors |
| `AppointmentBlock` | Individual appointment block rendered inside the time grid |
| `NowIndicator` | Red line showing current time in the time grid |

### Hooks

| Hook | Description |
|------|-------------|
| `useDoctors` | Fetches `/doctors/` and returns doctor list |
| `useAppointments` | Fetches `/appointments/` and returns appointment list |
| `useToday` | Returns today's date string |

### Color system

Doctor colors are assigned by index from a fixed palette (`teal`, `sage`, `amber`, `indigo`, `rose`) via `getDoctorColor(index)` in `utils/constants`. The same color is used for the appointment block, the legend dot, and the drawer avatar background.

---

## Getting Started

### Backend

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Apply database migrations
alembic upgrade head

# 3. (Optional) Seed sample data
python Telesecreter_Infrastructure/seeds/db_seeds.py

# 4. Start the development server
uvicorn Telesecreter_API.main:app --reload

# API available at http://localhost:8000
# Swagger UI at  http://localhost:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# UI available at http://localhost:5173
```

The backend allows CORS from `localhost:5173` and `localhost:5174` out of the box.

### Adding a database migration

```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

---

## Roadmap

Planned work tracked in `todo.txt`:

### Endpoint levels
- **Level 2** — Get-by-ID for all five resources
- **Level 3** — Name/field-based search
- **Level 4** — Update (PUT/PATCH) for all resources
- **Level 5** — Delete for all resources

### Webhook layer (voice AI integration)

| Webhook | Purpose |
|---------|---------|
| `POST /search-doctor` | Symptom → Department → sorted Doctor list (by rating) |
| `POST /check-slots` | Return available time slots for a doctor on a date |
| `POST /confirm-booking` | Insert a confirmed appointment into the DB |
| `POST /cancel-appointment` | Cancel an existing appointment |

### Other planned features
- Authentication via phone number (OTP / OAuth)
- Appointment confirmation SMS/email via Twilio
- Reschedule appointment flow
- Recommend nearest available date when requested slot is full
- Retell.ai voice agent configuration wired to the webhook endpoints
