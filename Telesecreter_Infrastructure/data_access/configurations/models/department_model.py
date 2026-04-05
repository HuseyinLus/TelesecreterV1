from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.orm import relationship
from Telesecreter_Infrastructure.data_access.configurations.common.base_model import BaseModel


class DepartmentModel(BaseModel):
    __tablename__ = "departments"

    name = Column(String, nullable=False)

    doctors = relationship("DoctorModel", back_populates="department")

    __table_args__ = (
        UniqueConstraint("name", name="uq_department_name"),
    )

    @property
    def doctor_ids(self) -> list[str]:
        return [doctor.id for doctor in self.doctors]