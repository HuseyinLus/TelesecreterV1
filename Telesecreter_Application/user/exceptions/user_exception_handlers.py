from uuid import UUID


class UserNotFoundException(Exception):
    def __init__(self, user_id: UUID):
        super().__init__(f"User with id '{user_id}' not found.")
        self.user_id = user_id


class PhoneNumberNotFoundException(Exception):
    def __init__(self, phone_number: str):
        super().__init__(f"Phone number '{phone_number}' not found.")
        self.phone_number = phone_number
