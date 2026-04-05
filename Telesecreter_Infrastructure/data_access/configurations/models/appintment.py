from sqlalchemy import Column, String, Date, Time, ForeignKey, Enum, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from Telesecreter_Infrastructure.data_access.configurations.common.base_model import BaseModel
from Telesecreter_Domain.enums.appointment_status import AppointmentStatus


class AppointmentModel(BaseModel):
    __tablename__ = "appointments"

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    doctor_id = Column(String, ForeignKey("doctors.id"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.PENDING, nullable=False)
    cancelled_at = Column(String, nullable=True)
    cancellation_reason = Column(String, nullable=True)

    user = relationship("UserModel", back_populates="appointments")
    doctor = relationship("DoctorModel", back_populates="appointments")

    __table_args__ = (
        Index("ix_appointment_user", "user_id"),
        Index("ix_appointment_doctor_date", "doctor_id", "date"),
        UniqueConstraint("doctor_id", "date", "start_time", name="uq_doctor_timeslot"),
    )
