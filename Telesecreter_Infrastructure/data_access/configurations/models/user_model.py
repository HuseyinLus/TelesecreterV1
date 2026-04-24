from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.orm import relationship
from Telesecreter_Infrastructure.data_access.configurations.common.base_model import BaseModel
from Telesecreter_Domain.enums.user_role import UserRole


class UserModel(BaseModel):
    __tablename__ = "users"

    full_name       = Column(String, nullable=False)
    phone_number    = Column(String, unique=True, nullable=False)
    email           = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role            = Column(Enum(UserRole, values_callable=lambda x: [e.value for e in x]), nullable=False, default=UserRole.PATIENT)
    is_active       = Column(Boolean, default=True, nullable=False)

    appointments = relationship("AppointmentModel", back_populates="user")