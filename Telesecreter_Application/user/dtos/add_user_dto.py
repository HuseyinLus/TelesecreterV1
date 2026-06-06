from pydantic import BaseModel
from Telesecreter_Domain.enums.user_role import UserRole


class AddUserRequest(BaseModel):
    full_name: str
    phone_number: str
    email: str
    hashed_password: str
    role: UserRole = UserRole.PATIENT
    is_active: bool = True
