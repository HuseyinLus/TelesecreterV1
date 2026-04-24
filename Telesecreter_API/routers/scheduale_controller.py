from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from Telesecreter_Domain.interfaces.i_scheduale_repository import IScheduleRepository
from Telesecreter_Application.scheduale.queries.get_all_scheduales_query import GetAllSchedualesQuery
from Telesecreter_Application.scheduale.dtos import scheduale_dto
from Telesecreter_Application.doctor.queries.get_doctor_availability_query import GetDoctorAvailabilityQuery
from Telesecreter_Application.doctor.Exceptions.doctor_exception_handlers import PastDateError
from Telesecreter_API.dependencies.dependency_injection import get_schedule_repo

router = APIRouter(prefix="/scheduales", tags=["Scheduales"])


@router.get("/", response_model=list[scheduale_dto.SchedualeDTO])
def get_all_scheduales(repo: IScheduleRepository = Depends(get_schedule_repo)):
    return GetAllSchedualesQuery(repo).execute()


@router.get("/{doctor_id}/availability")
def get_doctor_availability(
    doctor_id: UUID,
    date_str: str,
    schedule_repo: IScheduleRepository = Depends(get_schedule_repo),
):
    try:
        available = GetDoctorAvailabilityQuery(schedule_repo).execute(doctor_id, date_str)
        return {"available": available}
    except PastDateError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use MM.DD (e.g. 04.15)")
