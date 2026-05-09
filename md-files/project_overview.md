Team Members
Huseyin Lus – Student ID: (your student ID here)

1. System Title and Domain
System Name: TelesecreterV1
Application Domain: A system designed to support telemedicine appointment management for
clinics, integrating a voice-AI telephone secretary with a backend REST API and a calendar
dashboard for clinic staff.

2. Problem Statement
Healthcare providers commonly rely on manual phone calls, spreadsheets, and fragmented
scheduling tools to manage patient appointments. This approach frequently results in
double-bookings, missed appointments, unclear availability, and high administrative overhead.
These challenges primarily affect clinic receptionists, doctors, and patients seeking timely
care. The resulting impact includes reduced clinic efficiency, patient dissatisfaction, and
increased cost of administrative labor.

3. Stakeholders and User Roles
Stakeholders: Patients, clinic doctors, clinic administrators, and voice-AI telephone agents.

User Role 1: Patient
1 Book, reschedule, and cancel medical appointments via phone or direct interaction.
2 Receive confirmation and reminder notifications for upcoming appointments.
3 Search for doctors by name, department, or specialty.

User Role 2: Clinic Administrator / Staff
1 View and manage the full appointment calendar through the dashboard.
2 Monitor doctor availability and schedule across departments.
3 Oversee appointment statuses and handle escalations.

User Role 3: Voice-AI Agent (Retell / Twilio)
1 Accept inbound patient phone calls and guide them through booking.
2 Invoke webhook endpoints to search doctors, check slots, and confirm bookings.
3 Trigger appointment status updates upon call completion.

4. System Boundary
In-Scope Functions:
1 Doctor search by name, department, and specialty.
2 Doctor schedule management and availability checking.
3 Appointment creation, confirmation, cancellation, and rescheduling.
4 Webhook layer for voice-AI telephone agent integration.
5 Calendar dashboard for clinic staff with week, day, and list views.
6 Automated appointment confirmation notifications (SMS / email via Twilio).

Out-of-Scope Functions:
1 Electronic health records (EHR) or medical record management.
2 Billing, insurance processing, or payment functionality.
3 Telemedicine video or audio consultation delivery.
4 Hospital-wide resource management (operating rooms, equipment).
5 Automated medical diagnosis or symptom assessment.

5. High-Level Capabilities
1 Patients can book appointments through a voice-AI phone call without human staff involvement.
2 The system searches for available doctors by department and rating, returning the best match.
3 Clinic staff can view and manage all appointments through a real-time calendar dashboard.
4 The backend enforces no double-bookings via unique constraints on doctor, date, and time slot.
5 The system sends automated confirmation messages upon successful appointment booking.
6 Administrators can manage doctors, departments, users, and schedules through REST API endpoints.

6. Mission and Vision
The mission of TelesecreterV1 is to eliminate manual appointment coordination overhead in
clinics by providing an AI-driven, self-service booking experience accessible by phone. The
vision is a fully autonomous medical receptionist that operates 24/7, reduces no-shows, and
gives clinic staff a clear real-time view of daily activity.

7. Objectives
1 Reduce manual appointment booking calls handled by human staff by at least 60%.
2 Eliminate double-bookings through automated slot validation.
3 Achieve appointment confirmation delivery within 30 seconds of booking.
4 Provide clinic staff with a calendar view that reflects real-time appointment state.

8. Success Criteria and KPIs
1 Number of appointments booked end-to-end via the voice-AI agent without staff intervention.
2 Rate of double-booking conflicts (target: 0%).
3 Average time from call start to confirmed booking.
4 Confirmation message delivery success rate.
5 Clinic staff satisfaction with the calendar dashboard.

9. Constraints and Risks
1 Single-developer team; mitigation through strict Clean Architecture layering and CQRS to
  keep the codebase navigable and maintainable by one person.
2 Voice-AI integration dependency on Retell/Twilio; mitigation by isolating all telephony
  logic behind webhook endpoints so the core backend is provider-agnostic.
3 SQLite scalability ceiling; mitigation by abstracting all data access behind repository
  interfaces, allowing a database swap without touching domain or application layers.
4 Patient data privacy; mitigation through role-based access controls, hashed passwords,
  and planned phone-number OTP authentication.
