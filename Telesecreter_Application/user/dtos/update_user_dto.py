from typing import Optional
from pydantic import BaseModel
from Telesecreter_Domain.enums.user_role import UserRole


class UpdateUserRequest(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    hashed_password: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
