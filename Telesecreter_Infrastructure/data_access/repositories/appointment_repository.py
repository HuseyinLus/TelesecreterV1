from datetime import date, time
from uuid import UUID

from Telesecreter_Domain.interfaces.i_appointment_repository import IAppointmentRepository
from Telesecreter_Domain.entities.appointments import Appointment
from Telesecreter_Domain.enums.appointment_status import AppointmentStatus
from Telesecreter_Infrastructure.data_access.configurations.models.appintment import AppointmentModel
from Telesecreter_Infrastructure.data_access.repositories.repository import GenericRepository
from Telesecreter_Infrastructure.data_access.db.database import get_db


def _map(row: AppointmentModel) -> Appointment:
    return Appointment(
        id=UUID(row.id),
        user_id=UUID(row.user_id),
        doctor_id=UUID(row.doctor_id),
        date=row.date,
        start_time=row.start_time,
        end_time=row.end_time,
        status=row.status,
        cancelled_at=row.cancelled_at,
        cancellation_reason=row.cancellation_reason,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


class AppointmentRepository(GenericRepository[Appointment, AppointmentModel], IAppointmentRepository):

    def __init__(self):
        super().__init__(AppointmentModel, _map)

    def add(self, entity: Appointment) -> Appointment:
        model = AppointmentModel(
            id=str(entity.id),
            user_id=str(entity.user_id),
            doctor_id=str(entity.doctor_id),
            date=entity.date,
            start_time=entity.start_time,
            end_time=entity.end_time,
            status=entity.status,
            cancelled_at=entity.cancelled_at,
            cancellation_reason=entity.cancellation_reason,
        )
        with get_db() as session:
            session.add(model)
        return entity

    def update(self, entity: Appointment) -> Appointment:
        with get_db() as session:
            model = session.get(AppointmentModel, str(entity.id))
            if model is None:
                raise ValueError(f"Appointment {entity.id} not found")
            model.date = entity.date
            model.start_time = entity.start_time
            model.end_time = entity.end_time
            model.status = entity.status
            model.cancelled_at = entity.cancelled_at
            model.cancellation_reason = entity.cancellation_reason
        return entity

    def get_by_user(self, user_id: UUID) -> list[Appointment]:
        with get_db() as session:
            rows = session.query(AppointmentModel).filter(
                AppointmentModel.user_id == str(user_id)
            ).all()
            return [_map(row) for row in rows]

    def get_by_doctor(self, doctor_id: UUID) -> list[Appointment]:
        with get_db() as session:
            rows = session.query(AppointmentModel).filter(
                AppointmentModel.doctor_id == str(doctor_id)
            ).all()
            return [_map(row) for row in rows]

    def get_by_doctor_and_date(self, doctor_id: UUID, date: date) -> list[Appointment]:
        with get_db() as session:
            rows = session.query(AppointmentModel).filter(
                AppointmentModel.doctor_id == str(doctor_id),
                AppointmentModel.date == date,
            ).all()
            return [_map(row) for row in rows]

    def get_by_status(self, status: AppointmentStatus) -> list[Appointment]:
        with get_db() as session:
            rows = session.query(AppointmentModel).filter(
                AppointmentModel.status == status
            ).all()
            return [_map(row) for row in rows]

    def exists_by_doctor_date_time(self, doctor_id: UUID, appt_date: date, start_time: time) -> bool:
        with get_db() as session:
            return session.query(AppointmentModel).filter(
                AppointmentModel.doctor_id == str(doctor_id),
                AppointmentModel.date == appt_date,
                AppointmentModel.start_time == start_time,
            ).first() is not None