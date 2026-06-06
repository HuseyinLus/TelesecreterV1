class AppointmentNotFoundError(Exception):
    def __init__(self, appointment_id):
        super().__init__(f"Appointment with id '{appointment_id}' not found.")


class DoctorNotAvailableError(Exception):
    """Raised when the doctor has no schedule on the requested date."""
    def __init__(self):
        super().__init__("Doctor is not available at the given date")


class DoctorNotFoundError(Exception):
    """Raised when the provided doctor_id does not exist."""
    def __init__(self, doctor_id):
        super().__init__(f"Invalid Doctor id: {doctor_id}")


class PastDateError(Exception):
    """Raised when the requested date is before today."""
    def __init__(self):
        super().__init__("Appointment date cannot be before today")


class DoctorNotAvailableAtTimeError(Exception):
    """Raised when the requested time slot is already booked."""
    def __init__(self):
        super().__init__("Doctor is not available in the selected time")
