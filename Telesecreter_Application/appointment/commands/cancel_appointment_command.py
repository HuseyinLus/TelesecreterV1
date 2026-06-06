from datetime import datetime
from uuid import UUID
from Telesecreter_Domain.enums.appointment_status import AppointmentStatus
from Telesecreter_Domain.interfaces.i_appointment_repository import IAppointmentRepository
from Telesecreter_Application.appointment.dtos.appointment_dto import AppointmentDTO
from Telesecreter_Application.appointment.dtos.cancel_appointment_dto import CancelAppointmentRequest
from Telesecreter_Application.appointment.exceptions.appointment_exception_handlers import AppointmentNotFoundError


class CancelAppointmentCommand:

    def __init__(self, appointment_repo: IAppointmentRepository):
        self._appointment_repo = appointment_repo

    def execute(self, appointment_id: UUID, request: CancelAppointmentRequest) -> AppointmentDTO:
        appointment = self._appointment_repo.get_by_id(appointment_id)
        if appointment is None:
            raise AppointmentNotFoundError(appointment_id)

        appointment.status = AppointmentStatus.CANCELLED
        appointment.cancelled_at = datetime.utcnow().isoformat()
        appointment.cancellation_reason = request.cancellation_reason
        self._appointment_repo.update(appointment)
        return AppointmentDTO.from_entity(appointment)
