from typing import Optional
from uuid import UUID
from Telesecreter_Domain.interfaces.i_department_repository import IDoctorRepository
from Telesecreter_Domain.entities.doctor import Doctor
from Telesecreter_Infrastructure.data_access.configurations.models.doctor_model import DoctorModel
from Telesecreter_Infrastructure.data_access.repositories.repository import GenericRepository
from Telesecreter_Infrastructure.data_access.db.database import get_db


def _map(row) -> Doctor:
    return Doctor(
        id=row["id"],
        full_name=row["full_name"],
        email=row["email"],
        phone_number=row["phone_number"],
        department_id=row["department_id"],
        specialty=row["specialty"],
        is_available=bool(row["is_available"]),
        rating=row["rating"],
    )


class DoctorRepository(GenericRepository[Doctor, DoctorModel], IDoctorRepository):

    def __init__(self):
        super().__init__(DoctorModel, _map)

    def get_by_email(self, email: str) -> Optional[Doctor]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM doctors WHERE email = ?", (email,)).fetchone()
            return _map(row) if row else None

    def get_by_department(self, department_id: UUID) -> list[Doctor]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM doctors WHERE department_id = ?", (str(department_id),)).fetchall()
            return [_map(row) for row in rows]

    def get_available_doctors(self) -> list[Doctor]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM doctors WHERE is_available = 1").fetchall()
            return [_map(row) for row in rows]