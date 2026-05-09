Software Requirements Specification — 
Callie
Team Members
Huseyin Lus

---

# Introduction

## 1.1 Purpose
This Software Requirements Specification defines the functional and non-functional requirements
for TelesecreterV1, a telemedicine appointment management system for clinics. The purpose of
the system is to allow patients to book, reschedule, and cancel medical appointments through
an AI-driven telephone agent, while giving clinic staff a real-time calendar dashboard for
monitoring and managing appointments.

## 1.2 Scope
TelesecreterV1 is a web-based system with a REST API backend and a calendar dashboard
frontend. It allows patients to interact with a voice-AI telephone agent to book appointments
without human staff involvement. Clinic administrators and staff can view, manage, and
track all appointments through a calendar interface. The system does not include electronic
health records, billing or insurance processing, telemedicine video or audio consultation,
or automated medical diagnosis.

## 1.3 Intended Audience
This document is intended for:
- Developers
- System analysts
- Clinic administrators
- Testers
- Project supervisors

## 1.4 Definitions and Abbreviations
- SRS: Software Requirements Specification
- KPI: Key Performance Indicator
- API: Application Programming Interface
- CQRS: Command Query Responsibility Segregation
- ORM: Object-Relational Mapper
- Webhook: An HTTP callback endpoint invoked by an external service
- Voice-AI Agent: An automated telephone agent (e.g. Retell) that interacts with patients
- Appointment: A scheduled visit between a patient and a doctor at a specific date and time
- Slot: A specific time interval within a doctor's available schedule

## 1.5 References
- Project Overview: TelesecreterV1 (project_overview.md)
- Developer Reference: README_Dev.md
- Development Roadmap: todo.txt

---

# Overall Description

## 2.1 Product Perspective
TelesecreterV1 is a standalone clinic appointment management system designed to replace
manual phone-based booking handled by human receptionists. It acts as an autonomous
telephone secretary: a voice-AI agent answers patient calls, queries the backend via webhook
endpoints, and books appointments without staff intervention. Clinic staff interact with the
system through a web dashboard rather than through phone calls or spreadsheets.

## 2.2 Product Functions
The system will:
- Allow patients to search for doctors by name and department through the voice-AI agent
- Check doctor availability and return open time slots
- Book, confirm, cancel, and reschedule appointments
- Send confirmation notifications to patients upon successful booking
- Display a real-time appointment calendar dashboard for clinic staff
- Expose a REST API for all resources with full CRUD operations
- Support role-based access for patients and administrators

## 2.3 User Classes and Characteristics

### Patient
Patients interact with the system primarily through a voice-AI telephone call. They do not
require technical skills. Their interaction is guided by the voice agent through a structured
booking dialog. Patients may also receive SMS or email confirmation of their appointment.

### Clinic Administrator / Staff
Clinic staff access the system through the web dashboard. They are expected to have basic
computer skills. They use the calendar to monitor appointments, check doctor schedules,
and manage day-to-day clinic operations.

### Voice-AI Agent (Retell / Twilio)
The voice-AI agent is a software client, not a human. It authenticates against the backend
and calls webhook endpoints to perform doctor search, slot checking, and appointment
confirmation on behalf of the patient during a phone call.

## 2.4 Operating Environment
The system operates in:
- Modern web browsers (Chrome, Edge, Firefox, Safari)
- Desktop and laptop computers for clinic staff dashboard access
- Any phone line capable of connecting to the Retell/Twilio telephony platform
- Internet or clinic intranet connection for API and dashboard access

## 2.5 Design and Implementation Constraints
- Single-developer team; architecture must remain navigable and maintainable by one person
- Clean Architecture layering must be strictly maintained; no business logic in the API layer
- SQLite is used as the database; repository abstraction must allow future migration
- Voice-AI integration is provider-dependent on Retell/Twilio; webhook endpoints must remain
  provider-agnostic at the backend level
- Limited development time requires prioritization of core booking flow before extended features

## 2.6 Assumptions and Dependencies
- Patients have access to a standard telephone or mobile phone
- Clinic staff have internet access and a supported browser
- The Retell or Twilio platform is configured and operational
- An email or SMS notification service is available for confirmation delivery
- All users with dashboard access have registered accounts

---

# Specific Requirements

## 3.1 Functional Requirements

### FR1. User Registration and Authentication
- The system shall allow patients and administrators to register using a phone number.
- The system shall authenticate users via phone-number-based OTP (one-time password).
- The system shall restrict access to resources based on user role (PATIENT, ADMIN).
- The system shall hash and securely store all user passwords.

### FR2. Profile Management
- The system shall allow users to view and edit their profile information.
- The system shall store each user's full name, email, phone number, and role.
- The system shall mark users as active or inactive.

### FR3. Doctor Management
- The system shall allow administrators to create, update, and delete doctor records.
- Each doctor record shall include full name, email, phone number, specialty, department,
  rating, and availability status.
- The system shall allow filtering doctors by department and availability.

### FR4. Department Management
- The system shall allow administrators to create and manage medical departments.
- Each department shall have a unique name.
- The system shall associate doctors with departments.

### FR5. Doctor Schedule Management
- The system shall allow administrators to define weekly availability schedules per doctor.
- Each schedule entry shall specify the day of the week and the start and end time.
- The system shall enforce one schedule entry per doctor per day of the week.

### FR6. Appointment Creation
- The system shall allow patients (via voice-AI agent or direct API) to create appointments.
- Each appointment shall record the patient, doctor, date, start time, end time, and status.
- The system shall prevent double-bookings by enforcing uniqueness on doctor, date,
  and start time.
- The default appointment status shall be PENDING upon creation.

### FR7. Appointment Status Management
- The system shall support the following appointment statuses:
  - PENDING
  - CONFIRMED
  - CANCELLED
  - COMPLETED
  - RESCHEDULED
- The system shall allow authorized users to update appointment status.
- The system shall record the cancellation timestamp and reason when an appointment is cancelled.

### FR8. Doctor Search Webhook
- The system shall expose a webhook endpoint (POST /search-doctor) that accepts a doctor
  name and department name as input.
- The system shall return a list of matching doctors sorted by rating in descending order.
- The search shall support partial, case-insensitive name matching.

### FR9. Availability Check Webhook
- The system shall expose a webhook endpoint (POST /check-slots) that accepts a doctor
  identifier and a requested date.
- The system shall return available time slots for that doctor on that date based on their
  schedule and existing bookings.
- If no slots are available on the requested date, the system shall return the nearest
  available date.

### FR10. Appointment Confirmation Webhook
- The system shall expose a webhook endpoint (POST /confirm-booking) that creates a
  confirmed appointment record in the database.
- The system shall trigger a confirmation notification to the patient upon successful booking.
- The webhook shall be invoked by the voice-AI agent at the end of the booking call.

### FR11. Appointment Cancellation Webhook
- The system shall expose a webhook endpoint (POST /cancel-appointment) that cancels an
  existing appointment.
- The system shall record the reason for cancellation and update the appointment status.

### FR12. Notification and Confirmation Delivery
- The system shall send an appointment confirmation message to the patient via SMS or email
  after a successful booking.
- The system shall send reminder notifications before upcoming appointment deadlines.
- Notification delivery shall be handled via Twilio or an equivalent messaging service.

### FR13. Calendar Dashboard
- The system shall provide a web-based calendar dashboard accessible to clinic staff.
- The dashboard shall display appointments in week view, day view, and list view.
- The dashboard shall allow filtering appointments by doctor.
- The dashboard shall show an agenda panel for today's appointments.
- The dashboard shall display real-time statistics including total appointments, confirmed
  count, and confirmation rate.

### FR14. Search and Filter
- The system shall allow users to search for doctors by name and department.
- The system shall allow filtering appointments by doctor, date, and status.
- The system shall allow retrieving appointments for a specific user or doctor.

### FR15. Access Control
- The system shall ensure that only authenticated users can access API endpoints.
- The system shall prevent patients from accessing or modifying other patients' appointment
  records.
- The system shall restrict administrative operations (doctor and schedule management) to
  users with the ADMIN role.

---

## 3.2 Non-Functional Requirements

### NFR1. Usability
- The calendar dashboard shall be operable by clinic staff with basic computer skills.
- The voice-AI booking dialog shall complete a full appointment booking within 3 minutes.
- The interface shall minimize the number of steps required to view or manage appointments.

### NFR2. Performance
- The dashboard shall load within 3 seconds under normal usage conditions.
- Webhook endpoints shall return a response within 2 seconds to avoid voice-AI call timeouts.
- The system shall support concurrent access by multiple staff and ongoing voice calls
  without significant performance degradation.

### NFR3. Reliability
- The system shall be available at least 95% of the time during clinic operating hours.
- The system shall preserve all appointment and patient data without loss during normal
  operation.
- No double-bookings shall be permitted under any concurrent booking conditions.

### NFR4. Security
- The system shall require authenticated access to all non-public endpoints.
- The system shall implement role-based access control distinguishing PATIENT and ADMIN roles.
- The system shall store all passwords in hashed form.
- All client-server communication shall occur over HTTPS.
- Patient personal data shall be protected from unauthorized access.

### NFR5. Maintainability
- The backend shall follow Clean Architecture with strict layer separation so that individual
  layers can be modified without impacting others.
- All data access shall be abstracted behind repository interfaces to allow database
  replacement without changing domain or application logic.
- The codebase shall follow CQRS conventions; all business logic shall reside in query and
  command classes, not in API routers.

### NFR6. Scalability
- The repository abstraction layer shall allow migration from SQLite to a production-grade
  database (e.g. PostgreSQL) without changes to the domain or application layers.
- The system architecture shall support the addition of new entity types, webhook endpoints,
  and notification channels without structural refactoring.

### NFR7. Compatibility
- The dashboard shall be accessible through Chrome, Edge, Firefox, and Safari.
- The dashboard shall be responsive and usable on tablet and desktop screen sizes.
- The backend API shall be compatible with any HTTP client, including Retell, Twilio, and
  standard REST clients.

---

# External Interface Requirements

## 4.1 User Interface
The system interface shall include:
- Clinic staff login page
- Calendar dashboard with week, day, and list views
- Doctor filter and date navigation toolbar
- Appointment detail drawer with status, patient, doctor, date, and action buttons
- Today's agenda panel
- AI activity statistics panel (total booked, confirmed count, confirmation rate)
- Doctor legend with color coding

## 4.2 Software Interfaces
The system shall interact with:
- Retell or Twilio telephony platform via webhook HTTP callbacks
- Twilio or equivalent messaging service for SMS/email notification delivery
- SQLite database via SQLAlchemy ORM and Alembic migration management
- Optionally a university or clinic authentication system for single sign-on

## 4.3 Communications Interfaces
- Internet-based client-server communication over REST/HTTP
- Secure HTTPS connection for all data transfer
- Webhook endpoints exposed for voice-AI agent integration

---

# System Features

## 5.1 Voice-AI Telephone Booking

Patients call the clinic number. The voice-AI agent guides the patient through searching for
a doctor, selecting an available date and time, and confirming the appointment.

Inputs: patient phone call, spoken name, department preference, requested date and time
Outputs: confirmed appointment record, patient confirmation message, appointment status CONFIRMED

## 5.2 Doctor Search and Availability

The system locates the most suitable available doctor matching the patient's request and
returns open time slots for the selected date.

Inputs: doctor name (partial), department name, requested date
Outputs: sorted doctor list by rating, list of available time slots, nearest available date
if requested slot is full

## 5.3 Appointment Management

Clinic staff and authorized users can create, view, update, and cancel appointments through
the REST API or dashboard.

Inputs: patient ID, doctor ID, date, time slot, status update, cancellation reason
Outputs: updated appointment record, notification to patient, calendar dashboard refresh

## 5.4 Calendar Dashboard

Clinic staff can view and navigate all appointments in a structured calendar interface with
filtering and detail inspection.

Inputs: selected view mode, selected doctor filter, selected date
Outputs: appointment blocks in calendar grid, appointment detail drawer, agenda summary,
AI activity statistics

## 5.5 Notification System

The system reminds patients of upcoming appointments and confirms new bookings
automatically.

Inputs: appointment confirmation event, upcoming appointment deadline
Outputs: SMS or email confirmation message, reminder notification to patient

---

# Use Case Summary

## Use Case 1: Book Appointment via Voice-AI Agent

Actor: Patient (via Voice-AI Agent)
Precondition: Patient calls the clinic number; Retell agent is operational
Main Flow:
1. Patient calls and states the doctor name and preferred date.
2. Voice-AI agent calls POST /search-doctor with name and department.
3. System returns matching doctors sorted by rating.
4. Voice-AI agent calls POST /check-slots for the selected doctor and date.
5. System returns available time slots.
6. Patient selects a time slot.
7. Voice-AI agent calls POST /confirm-booking.
8. System creates appointment with status CONFIRMED.
9. System sends confirmation SMS/email to patient.
10. Call ends.

## Use Case 2: Cancel Appointment

Actor: Patient (via Voice-AI Agent) or Clinic Administrator
Precondition: Appointment exists with status PENDING or CONFIRMED
Main Flow:
1. Actor identifies the appointment to cancel.
2. Actor calls POST /cancel-appointment with appointment ID and reason.
3. System updates appointment status to CANCELLED.
4. System records cancellation timestamp and reason.
5. System notifies the patient of the cancellation.

## Use Case 3: View Appointment Calendar

Actor: Clinic Administrator / Staff
Precondition: Staff member is authenticated and dashboard is loaded
Main Flow:
1. Staff opens the calendar dashboard.
2. System fetches all appointments from the backend.
3. Staff selects view mode (week, day, or list).
4. System displays appointments in the selected view.
5. Staff optionally filters by doctor.
6. Staff clicks an appointment block to open the detail drawer.
7. System displays appointment details, patient info, status, and action options.

## Use Case 4: Check Doctor Availability

Actor: Voice-AI Agent
Precondition: Doctor exists in the system with a schedule defined
Main Flow:
1. Voice-AI agent calls POST /check-slots with doctor ID and requested date.
2. System retrieves the doctor's weekly schedule for that day of the week.
3. System checks existing appointments on that date for conflicts.
4. System returns available time slots.
5. If no slots are available, system returns the nearest available date.

## Use Case 5: Manage Doctor Schedule

Actor: Clinic Administrator
Precondition: Doctor record exists; administrator is authenticated with ADMIN role
Main Flow:
1. Administrator creates or updates a schedule entry for a doctor.
2. Administrator specifies the day of the week and the start and end time.
3. System validates that only one entry exists per doctor per day.
4. System saves the schedule.
5. Updated availability is immediately reflected in slot-checking responses.

---

# Data Requirements

The system shall store:
- User information (name, email, phone number, role, hashed password, active status)
- Doctor information (name, email, phone, specialty, department, rating, availability)
- Department information (name)
- Doctor schedules (doctor, day of week, start time, end time)
- Appointment records (patient, doctor, date, time slot, status, cancellation details)
- Appointment status history
- Notification delivery records

## Main Entities
- User
- Doctor
- Department
- DoctorSchedule
- Appointment
- Notification

## Key Relationships
- Department has many Doctors
- Doctor has many DoctorSchedules (one per day of week)
- Doctor has many Appointments
- User (Patient) has many Appointments
- Appointment links one User and one Doctor

---

# Constraints and Risks

## Constraints
- Single-developer team; feature scope must be prioritized around the core booking flow
- SQLite used for development; production deployment may require database migration
- Voice-AI telephony integration depends on Retell/Twilio platform availability

## Risks

**Voice-AI provider dependency**
Mitigation: all telephony logic is isolated behind webhook endpoints; the backend is
provider-agnostic and can be connected to any HTTP-capable agent platform.

**Double-booking under concurrent requests**
Mitigation: the database enforces a unique constraint on (doctor_id, date, start_time);
conflicting concurrent inserts will be rejected at the database level.

**Data privacy for patient records**
Mitigation: role-based access control, hashed passwords, HTTPS-only communication, and
phone-number OTP authentication prevent unauthorized access to patient data.

**User adoption by clinic staff**
Mitigation: the dashboard is designed to minimize steps and present a familiar calendar
interface requiring no technical background.

---

# Success Criteria

The system will be considered successful if it achieves:
- At least 60% of appointment bookings completed by the voice-AI agent without staff intervention
- Zero double-booking incidents enforced by database constraints
- Appointment confirmation messages delivered within 30 seconds of booking
- Dashboard page load time under 3 seconds under normal usage
- Clinic staff satisfaction with the calendar dashboard

## KPIs
- Number of appointments booked end-to-end via voice-AI without staff involvement
- Double-booking conflict rate (target: 0%)
- Average time from call start to confirmed booking
- Confirmation message delivery success rate
- Clinic staff satisfaction rating

---

# Future Enhancements

Possible future additions:
- Integration with hospital Electronic Health Record (EHR) systems
- Multi-clinic and multi-branch support
- Patient mobile app for self-service booking without phone call
- Real-time analytics dashboard for clinic management
- Automated appointment reminder calls via voice-AI
- Insurance and billing integration
- Video telemedicine session scheduling
- Multi-language support for the voice-AI agent
