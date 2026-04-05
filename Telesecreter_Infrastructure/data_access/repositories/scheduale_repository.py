from uuid import UUID
from Telesecreter_Domain.interfaces.i_scheduale_repository import IScheduleRepository
from Telesecreter_Domain.entities.scheduale import DoctorSchedule
from Telesecreter_Infrastructure.data_access.configurations.models.schedual_model import DoctorScheduleModel
from Telesecreter_Infrastructure.data_access.repositories.repository import GenericRepository
from Telesecreter_Infrastructure.data_access.db.database import get_db


def _map(row) -> DoctorSchedule:
    return DoctorSchedule(
        id=row["id"],
        doctor_id=row["doctor_id"],
        day_of_week=row["day_of_week"],
        start_time=row["start_time"],
        end_time=row["end_time"],
    )


class ScheduleRepository(GenericRepository[DoctorSchedule, DoctorScheduleModel], IScheduleRepository):

    def __init__(self):
        super().__init__(DoctorScheduleModel, _map)

    def get_by_doctor(self, doctor_id: UUID) -> list[DoctorSchedule]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM doctor_schedules WHERE doctor_id = ?", (str(doctor_id),)).fetchall()
            return [_map(row) for row in rows]

    def get_by_doctor_and_day(self, doctor_id: UUID, day_of_week: int) -> list[DoctorSchedule]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM doctor_schedules WHERE doctor_id = ? AND day_of_week = ?",
                (str(doctor_id), day_of_week)
            ).fetchall()
            return [_map(row) for row in rows]