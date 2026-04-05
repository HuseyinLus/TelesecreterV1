from sqlalchemy import Column, String, Boolean, Float
from sqlalchemy.orm import relationship
from Telesecreter_Infrastructure.data_access.configurations.common.base_model import BaseModel


class DoctorModel(BaseModel):
    __tablename__ = "doctors"

    full_name    = Column(String, nullable=False)
    email        = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=True, default="")
    specialty    = Column(String, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    rating       = Column(Float, nullable=True, default=None)

    department   = relationship("DepartmentModel", back_populates="doctors")
    appointments = relationship("AppointmentModel", back_populates="doctor")
    schedules    = relationship("DoctorScheduleModel", back_populates="doctor")