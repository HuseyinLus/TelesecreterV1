from uuid import UUID

from Telesecreter_Domain.interfaces.i_scheduale_repository import IScheduleRepository
from Telesecreter_Domain.entities.scheduale import DoctorSchedule
from Telesecreter_Infrastructure.data_access.configurations.models.schedual_model import DoctorScheduleModel
from Telesecreter_Infrastructure.data_access.repositories.repository import GenericRepository
from Telesecreter_Infrastructure.data_access.db.database import get_db


def _map(row: DoctorScheduleModel) -> DoctorSchedule:
    return DoctorSchedule(
        id=UUID(row.id),
        doctor_id=UUID(row.doctor_id),
        day_of_week=row.day_of_week,
        start_time=row.start_time,
        end_time=row.end_time,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


class ScheduleRepository(GenericRepository[DoctorSchedule, DoctorScheduleModel], IScheduleRepository):

    def __init__(self):
        super().__init__(DoctorScheduleModel, _map)

    def add(self, entity: DoctorSchedule) -> DoctorSchedule:
        model = DoctorScheduleModel(
            id=str(entity.id),
            doctor_id=str(entity.doctor_id),
            day_of_week=entity.day_of_week,
            start_time=entity.start_time,
            end_time=entity.end_time,
        )
        with get_db() as session:
            session.add(model)
        return entity

    def update(self, entity: DoctorSchedule) -> DoctorSchedule:
        with get_db() as session:
            model = session.get(DoctorScheduleModel, str(entity.id))
            if model is None:
                raise ValueError(f"DoctorSchedule {entity.id} not found")
            model.day_of_week = entity.day_of_week
            model.start_time = entity.start_time
            model.end_time = entity.end_time
        return entity

    def get_by_doctor(self, doctor_id: UUID) -> list[DoctorSchedule]:
        with get_db() as session:
            rows = session.query(DoctorScheduleModel).filter(
                DoctorScheduleModel.doctor_id == str(doctor_id)
            ).all()
            return [_map(row) for row in rows]

    def get_by_doctor_and_day(self, doctor_id: UUID, day_of_week: int) -> list[DoctorSchedule]:
        with get_db() as session:
            rows = session.query(DoctorScheduleModel).filter(
                DoctorScheduleModel.doctor_id == str(doctor_id),
                DoctorScheduleModel.day_of_week == day_of_week,
            ).all()
            return [_map(row) for row in rows]