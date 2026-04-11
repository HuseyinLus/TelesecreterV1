from typing import Optional
from uuid import UUID

from Telesecreter_Domain.interfaces.i_doctor_repository import IDoctorRepository
from Telesecreter_Domain.entities.doctor import Doctor
from Telesecreter_Infrastructure.data_access.configurations.models.doctor_model import DoctorModel
from Telesecreter_Infrastructure.data_access.repositories.repository import GenericRepository
from Telesecreter_Infrastructure.data_access.db.database import get_db


def _map(row: DoctorModel) -> Doctor:
    return Doctor(
        id=UUID(row.id),
        full_name=row.full_name,
        email=row.email,
        phone_number=row.phone_number or "",
        department_id=row.department_id,
        specialty=row.specialty,
        is_available=row.is_available,
        ratings=row.rating,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


class DoctorRepository(GenericRepository[Doctor, DoctorModel], IDoctorRepository):

    def __init__(self):
        super().__init__(DoctorModel, _map)

    def add(self, entity: Doctor) -> Doctor:
        model = DoctorModel(
            id=str(entity.id),
            full_name=entity.full_name,
            email=entity.email,
            phone_number=entity.phone_number,
            department_id=str(entity.department_id),
            specialty=entity.specialty,
            is_available=entity.is_available,
            rating=entity.ratings,
        )
        with get_db() as session:
            session.add(model)
        return entity

    def update(self, entity: Doctor) -> Doctor:
        with get_db() as session:
            model = session.get(DoctorModel, str(entity.id))
            if model is None:
                raise ValueError(f"Doctor {entity.id} not found")
            model.full_name = entity.full_name
            model.email = entity.email
            model.phone_number = entity.phone_number
            model.department_id = str(entity.department_id)
            model.specialty = entity.specialty
            model.is_available = entity.is_available
            model.rating = entity.ratings
        return entity

    def get_by_email(self, email: str) -> Optional[Doctor]:
        with get_db() as session:
            row = session.query(DoctorModel).filter(DoctorModel.email == email).first()
            return _map(row) if row else None

    def get_by_department(self, department_id: UUID) -> list[Doctor]:
        with get_db() as session:
            rows = session.query(DoctorModel).filter(
                DoctorModel.department_id == str(department_id)
            ).all()
            return [_map(row) for row in rows]

    def get_available_doctors(self) -> list[Doctor]:
        with get_db() as session:
            rows = session.query(DoctorModel).filter(DoctorModel.is_available == True).all()
            return [_map(row) for row in rows]