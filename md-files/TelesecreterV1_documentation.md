# TelesecreterV1 — Project Introduction & Technical Review

**Student:** Huseyin Lus
**Date:** April 2026

---

## 1. Project Overview

TelesecreterV1 is a telemedicine appointment management system built around a core concept: an AI-powered telephone secretary that allows patients to book medical appointments by making a phone call. Instead of navigating a website or app, a patient calls a clinic number, speaks with an AI voice agent, and the agent interacts with the backend in real time to find a doctor, check availability, and confirm a booking.

The system is split into two independent parts:

- **Backend (Python / FastAPI):** A REST API that manages doctors, patients, appointments, departments, and schedules. It also exposes webhook endpoints designed to be called by a voice AI agent (Retell/Twilio integration).
- **Frontend (React / Vite):** A real-time appointment calendar dashboard for clinic staff, allowing them to view and manage all appointments across doctors.

---

## 2. Motivation & Problem Statement

Traditional clinic appointment booking relies on a human receptionist answering calls, looking up doctor availability manually, and entering appointments into a system. This process is slow, error-prone, and unavailable outside office hours.

TelesecreterV1 replaces this flow with an automated AI telephone secretary. The backend is specifically designed to be called by a voice agent mid-conversation, meaning every API response must be fast, deterministic, and machine-readable. The frontend gives the clinic staff visibility into everything the AI books.

---

## 3. System Architecture

The backend strictly follows **Clean Architecture** with four separated layers. The core rule is that dependencies only point inward — the domain layer has no knowledge of the database or the web framework.

```
Telesecreter_API           →  HTTP layer (FastAPI routers, no business logic)
Telesecreter_Application   →  Business logic (CQRS-style Query/Command classes)
Telesecreter_Domain        →  Core model (entities, interfaces, enums)
Telesecreter_Infrastructure →  Data access (SQLAlchemy ORM, repositories, migrations)
```

### Request Flow

Every HTTP request follows this strict path:

```
HTTP Request → Router → Query Class → Repository Interface → Repository Implementation → SQLite → Entity → DTO → JSON Response
```

The router never touches the database. The domain layer never imports SQLAlchemy. This separation means the database could be swapped from SQLite to PostgreSQL by only changing the infrastructure layer.

### Key Design Patterns

**Repository Pattern:** The domain layer defines abstract interfaces (`IDoctorRepository`, `IUserRepository`, etc.) that declare what operations are available. The infrastructure layer provides the concrete SQLAlchemy implementations. The application layer only ever interacts with the interface, never the implementation.

**CQRS (Command Query Responsibility Segregation):** Every read operation is encapsulated in a Query class (e.g. `GetAllDoctorsQuery`, `GetDoctorByIdQuery`). Every write operation will be a Command class. This keeps business logic out of both the router and the repository.

**DTO Mapping:** Domain entities are never serialised directly to JSON. Each resource has a dedicated DTO with a `from_entity()` static method. FastAPI uses `response_model=` to validate and serialise only the DTO fields, keeping internal domain state private.

**Dependency Injection:** FastAPI's `Depends()` system is used throughout. A single file (`dependency_injection.py`) is the only place where concrete repository classes are instantiated. Swapping an implementation requires changing one line.

---

## 4. Domain Model

The system manages five core entities:

| Entity | Key Fields | Relationships |
|---|---|---|
| `User` | full_name, email, phone_number, role (PATIENT/ADMIN) | Has many Appointments |
| `Doctor` | full_name, email, specialty, department_id, rating, is_available | Belongs to Department, has many Appointments and Schedules |
| `Department` | name | Has many Doctors |
| `Appointment` | user_id, doctor_id, date, start_time, end_time, status | Belongs to User and Doctor |
| `DoctorSchedule` | doctor_id, day_of_week, start_time, end_time | Belongs to Doctor |

`AppointmentStatus` is an enum with values `PENDING`, `CONFIRMED`, `CANCELLED`. The appointments table enforces a unique constraint on `(doctor_id, date, start_time)` at the database level, preventing double-booking.

---

## 5. API Endpoints (Current State)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/doctors/` | List all doctors |
| GET | `/doctors/{id}` | Get doctor by ID |
| GET | `/doctors/search?name=` | Search doctors by name |
| GET | `/users/` | List all users/patients |
| GET | `/users/{id}` | Get user by ID |
| GET | `/appointments/` | List all appointments |
| GET | `/appointments/{doctor_id}` | Get appointments by doctor |
| GET | `/departments/` | List all departments |
| GET | `/scheduales/` | List all schedules |
| GET | `/scheduales/{doctor_id}/availability` | Check doctor availability for a date |

---

## 6. Webhook Layer (Voice AI Integration)

Three webhook endpoints are designed to be called by the voice AI agent during a live phone call:

| Webhook | Purpose |
|---|---|
| `search_doctor` | Takes a symptom or department name, returns matching doctors sorted by rating |
| `check_slots` | Takes a doctor ID and date, returns available time slots |
| `confirm_booking` | Creates the appointment record and returns confirmation |

This is the core value proposition of the project. The AI agent calls these endpoints in sequence during a patient call, creating a fully automated booking flow without human involvement.

---

## 7. Frontend Dashboard

The React frontend provides clinic staff with a real-time calendar view of all appointments. Key features:

- **Three view modes:** Week view (Google Calendar-style grid), Day view (per-doctor columns), List view (tabular)
- **Appointment drawer:** Clicking any appointment opens a slide-in panel with full details
- **Today's agenda:** Right rail showing today's appointments in chronological order with live/past/upcoming status
- **Doctors page:** Full table of all registered doctors with department, specialty, contact info
- **Patients page:** Full table of all registered patients with contact info
- **AI activity stats:** Summary card showing total bookings, confirmed count, and confirmation rate

The frontend uses TanStack Query for data fetching with polling intervals, meaning the calendar refreshes automatically as new appointments are booked through the voice AI.

---

## 8. Technology Decisions

**SQLite over PostgreSQL:** Chosen for zero-configuration local development. The repository pattern means this can be swapped to PostgreSQL for production without changing any application or domain code.

**FastAPI over Django/Flask:** FastAPI's native Pydantic integration, automatic OpenAPI docs, and async support make it well-suited for a webhook-heavy system where response time during a live phone call matters.

**Clean Architecture over a simple MVC:** The voice AI integration requires the business logic to be independently testable and not coupled to HTTP concerns. A flat MVC structure would make it difficult to test booking logic without spinning up a web server.

**CQRS-style queries:** Each use case is an isolated class. This makes it straightforward to add caching, logging, or validation to a specific operation without touching other parts of the system.

---

## 9. Current State & Roadmap

**Implemented:**
- Full GET endpoint layer for all five resources
- Doctor search by name and department
- Doctor availability checking by date
- Appointment booking (set appointment command)
- Complete frontend calendar dashboard
- Doctors and Patients management pages
- Database migrations with Alembic
- Seed data (24 doctors, 22 patients, 24 appointments)

**Planned:**
- Full CRUD endpoints (update, delete) for all resources
- Authentication with phone number-based login (OAuth)
- Retell/Twilio voice agent configuration and live webhook integration
- Appointment confirmation SMS to patient after booking
- Reschedule appointment endpoint
- Nearest available date suggestion when requested slot is taken

---

## 10. Running the Project

```bash
# Backend
pip install -r requirements.txt
alembic upgrade head
python Telesecreter_Infrastructure/seeds/db_seeds.py
uvicorn Telesecreter_API.main:app --reload
# API → http://localhost:8000
# Docs → http://localhost:8000/docs

# Frontend
cd frontend && npm install
cp .env.example .env.local  # set VITE_API_BASE_URL=http://localhost:8000
npm run dev
# UI → http://localhost:5173
```
