from datetime import date
from uuid import UUID
from Telesecreter_Domain.interfaces.i_appointment_repository import IAppointmentRepository
from Telesecreter_Domain.entities.appointments import Appointment
from Telesecreter_Domain.enums.appointment_status import AppointmentStatus
from Telesecreter_Infrastructure.data_access.configurations.models.appintment import AppointmentModel
from Telesecreter_Infrastructure.data_access.repositories.repository import GenericRepository
from Telesecreter_Infrastructure.data_access.db.database import get_db


def _map(row) -> Appointment:
    return Appointment(
        id=row["id"],
        user_id=row["user_id"],
        doctor_id=row["doctor_id"],
        date=row["date"],
        start_time=row["start_time"],
        end_time=row["end_time"],
        status=AppointmentStatus(row["status"]),
        notes=row["notes"] if "notes" in row.keys() else None,
        cancelled_at=row["cancelled_at"],
        cancellation_reason=row["cancellation_reason"],
    )


class AppointmentRepository(GenericRepository[Appointment, AppointmentModel], IAppointmentRepository):

    def __init__(self):
        super().__init__(AppointmentModel, _map)

    def get_by_user(self, user_id: UUID) -> list[Appointment]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM appointments WHERE user_id = ?", (str(user_id),)).fetchall()
            return [_map(row) for row in rows]

    def get_by_doctor(self, doctor_id: UUID) -> list[Appointment]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM appointments WHERE doctor_id = ?", (str(doctor_id),)).fetchall()
            return [_map(row) for row in rows]

    def get_by_doctor_and_date(self, doctor_id: UUID, date: date) -> list[Appointment]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM appointments WHERE doctor_id = ? AND date = ?",
                (str(doctor_id), str(date))
            ).fetchall()
            return [_map(row) for row in rows]

    def get_by_status(self, status: AppointmentStatus) -> list[Appointment]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM appointments WHERE status = ?", (status.value,)).fetchall()
            return [_map(row) for row in rows]