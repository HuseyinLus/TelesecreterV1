# TelesecreterV1 — Design Diagrams

---

## 1. Architectural Diagram (High-Level Component Architecture)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                              │
│                                                                         │
│   Patient (Phone Call)          Clinic Staff UI         Voice-AI Agent  │
│   - Speaks to AI agent          - Calendar dashboard    - Webhook calls │
│   - Hears confirmations         - Appointment drawer    - JSON in/out   │
│   - Receives SMS/email          - Doctor filter                         │
│                                                                         │
│                    REST API  /  WebHook Endpoints                       │
└───────────────────────┬─────────────────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────────────────┐
│                        APPLICATION LAYER                                │
│                                                                         │
│  ┌──────────────────┐  ┌──────────────────────┐  ┌──────────────────┐  │
│  │  Appointment     │  │  Doctor Search &     │  │  Notification    │  │
│  │  Management      │  │  Availability        │  │  Engine          │  │
│  │  Component       │  │  Component           │  │  Component       │  │
│  └──────────────────┘  └──────────────────────┘  └──────────────────┘  │
│                                                                         │
└───────────────────────┬─────────────────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────────────────┐
│              DATA LAYER — Data Access & Storage Component               │
│              with Role-Based Access Control (PATIENT / ADMIN)           │
│                                                                         │
│    Appointments Table   Doctors Table   Users Table   Schedules Table   │
└─────────────────────────────────────────────────────────────────────────┘
```

       | Component | Role in Architecture |
       |---|---|
       | Patient (Phone Call) | Initiates appointment booking through voice interaction |
       | Clinic Staff UI | Views and manages appointments through the calendar dashboard |
       | Voice-AI Agent | Calls webhook endpoints on behalf of the patient during a phone call |
       | Appointment Management Component | Handles appointment creation, status updates, cancellation, and rescheduling |
       | Doctor Search & Availability Component | Resolves doctor search by name/department and returns available time slots |
       | Notification Engine Component | Delivers SMS/email confirmations and deadline reminders |
       | Data Access & Storage Component | Encapsulates all database operations and enforces role-based access control |

---

## 2. Component Interaction Diagram (Data Flow)

```
                        Voice-AI Agent
                              │
                    1. POST /confirm-booking
                              │
                              ▼
                  ┌─────────────────────┐
                  │  Appointment Mgmt   │
                  │  Component          │
                  └──────────┬──────────┘
                             │
          ┌──────────────────┼─────────────────────┐
          │                  │                      │
   2. store appointment  3. check doctor       4. trigger
          │                  │   availability       │  confirmation
          ▼                  ▼                      ▼
 ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐
 │  Data Access    │  │  Doctor Search & │  │  Notification   │
 │  & Storage      │  │  Availability    │  │  Engine         │
 └─────────────────┘  └──────────────────┘  └────────┬────────┘
                                                      │
                                              5. send SMS / email
                                                      │
                                                      ▼
                                              Patient & Staff
```

| Component | Interaction Role |
|---|---|
| Voice-AI Agent | Initiates the booking request and orchestrates the webhook call sequence |
| Appointment Management Component | Validates input, enforces no-double-booking rule, and coordinates sub-calls |
| Doctor Search & Availability Component | Confirms the doctor exists and the requested slot is free |
| Data Access & Storage Component | Persists the appointment and retrieves doctor/schedule data |
| Notification Engine | Triggers SMS or email confirmation after successful appointment creation |

---

## 3. Detailed Design Diagram — Appointment Management Component

### 3.1 Class Diagram (UML-Style)

```
┌─────────────────────────────────────────────┐
│           AppointmentManagementService       │
│─────────────────────────────────────────────│
│ Methods:                                     │
│  + confirmBooking(request) : AppointmentDTO  │
│  + cancelAppointment(id, reason) : bool      │
│  + rescheduleAppointment(id, date, time)     │
│  + getAppointmentsByDoctor(doctor_id)        │
│  + getAppointmentsByUser(user_id)            │
│ Internal Helpers:                            │
│  - _checkSlotAvailability(doctor_id, date,   │
│      start_time) : bool                      │
│  - _resolveNearestDate(doctor_id) : date     │
└────────────────────────┬────────────────────┘
                         │ uses
              ┌──────────▼──────────┐
              │   Appointment        │
              │   (Entity)           │
              │─────────────────────│
              │  id: UUID            │
              │  user_id: UUID       │
              │  doctor_id: UUID     │
              │  date: date          │
              │  start_time: time    │
              │  end_time: time      │
              │  status: enum        │
              │  cancelled_at: str   │
              │  cancellation_reason │
              │─────────────────────│
              │  AppointmentStatus   │
              │  (enum)              │
              │  PENDING             │
              │  CONFIRMED           │
              │  CANCELLED           │
              │  COMPLETED           │
              │  RESCHEDULED         │
              └─────────────────────┘
```

### 3.2 State Machine Diagram (Appointment Lifecycle)

```
                    ┌────────────────┐
                    │  Appointment   │
                    │    Created     │
                    │ {Status=PENDING}│
                    └───────┬────────┘
                            │
                  voice-AI confirms booking
                            │
                            ▼
                    ┌───────────────┐
                    │  CONFIRMED    │◄─── admin overrides
                    └──────┬────────┘
                           │
             ┌─────────────┼──────────────┐
             │             │              │
      patient cancels  appointment    patient/admin
             │           passes          reschedules
             ▼             │              │
      ┌────────────┐        ▼              ▼
      │ CANCELLED  │   ┌──────────┐  ┌────────────┐
      │ (final)    │   │ COMPLETED│  │RESCHEDULED │
      └────────────┘   │ (final)  │  │            │
                       └──────────┘  └─────┬──────┘
                                           │
                                    new appointment
                                    CONFIRMED created
```

---

## 4. Detailed Design Diagram — Notification Engine

### 4.1 Sequence Diagram (Confirmation Sending)

```
Cron/Event    Notification    Appointment Mgmt    Data Access    SMS/Email
Trigger       Engine          Component           Component      Service
    │              │                │                  │              │
    │─triggerEvent─►              │                  │              │
    │              │─getUpcoming───►                 │              │
    │              │              │──getTasks()───────►             │
    │              │              │◄──return list─────┤             │
    │              │◄──return list─┤                  │             │
    │              │              │                   │             │
    │    for each appointment:    │                   │             │
    │              │              │                   │             │
    │              │  if hoursLeft <= 48:             │             │
    │              │──getAssignee(user_id)────────────►            │
    │              │◄──return patient──────────────────┤            │
    │              │─────────────────────────────sendReminder()────►│
    │              │                                   │            │
    │              │──logNotification()────────────────►           │
    │◄─────────────┤ done                              │            │
```

### 4.2 Activity Diagram (Notification Decision Logic)

```
Start: Event Trigger (booking confirmed / scheduled check)
              │
              ▼
    Query active appointments
    (status != CANCELLED, COMPLETED)
              │
              ▼
    For each appointment — compute hoursLeft = appointment_datetime - now()
              │
         ┌────┴────┐
         │ Decision │
         └────┬─────┘
              │
   ┌──────────┼────────────────┐
   │          │                │
hoursLeft  hoursLeft       hoursLeft
  < 0      <= 48              > 48
   │          │                │
   ▼          ▼                ▼
Send        Send           No notification
OVERDUE     REMINDER       (wait for next
alert to    at 48h and     cycle)
patient     24h mark
& doctor
   │          │                │
   └──────────┴────────────────┘
              │
              ▼
    Log notification & mark sent (avoid duplicates)
              │
              ▼
             End
```

---

## Summary Table

| Diagram | Type | Purpose |
|---|---|---|
| 1. Architectural Diagram | High-Level Component | Shows the 3-layer separation: Presentation, Application, Data |
| 2. Component Interaction | Data Flow | Shows how a booking flows from voice-AI agent through to persistence and notification |
| 3a. Class Diagram | UML Class | Defines AppointmentManagementService methods and Appointment entity structure |
| 3b. State Machine | State Diagram | Maps all valid Appointment status transitions |
| 4a. Sequence Diagram | UML Sequence | Details the notification delivery flow across components |
| 4b. Activity Diagram | Activity / Decision | Shows the per-appointment decision logic for reminder vs overdue vs no notification |
