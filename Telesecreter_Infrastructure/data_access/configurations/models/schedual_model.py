from sqlalchemy import Column, String, Integer, Time, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from Telesecreter_Infrastructure.data_access.configurations.common.base_model import BaseModel

class DoctorScheduleModel(BaseModel):
    __tablename__ = "doctor_schedules"

    doctor_id = Column(String, ForeignKey("doctors.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    doctor = relationship("DoctorModel", back_populates="schedules")

    __table_args__ = (
        Index("ix_schedule_doctor", "doctor_id"),
        UniqueConstraint("doctor_id", "day_of_week", name="uq_doctor_day"),
    )
