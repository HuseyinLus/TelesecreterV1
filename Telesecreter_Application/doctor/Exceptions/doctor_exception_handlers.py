class DoctorNotFoundError(Exception):
    """Raised when no doctor matches the given lookup criteria."""
    def __init__(self, detail: str):
        super().__init__(f"Doctor not found: {detail}")
