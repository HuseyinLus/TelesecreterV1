class DoctorNotFoundError(Exception):
    """Raised when no doctor matches the given lookup criteria."""
    def __init__(self, detail: str):
        super().__init__(f"Doctor not found: {detail}")


class PastDateError(Exception):
    """Raised when the requested date is before today."""
    def __init__(self):
        super().__init__("Date cannot be in the past")


class InvalidTimeFormatError(Exception):
    """Raised when requested_time is not a valid HH:MM string."""
    def __init__(self, time_str: str):
        super().__init__(f"Invalid time format: '{time_str}'. Use HH:MM (e.g. 09:30)")
