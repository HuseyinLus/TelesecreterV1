from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from Telesecreter_Domain.interfaces.i_scheduale_repository import IScheduleRepository
from Telesecreter_Application.scheduale.dtos.scheduale_dto import SchedualeDTO
from Telesecreter_Application.scheduale.dtos.add_schedule_dto import AddScheduleRequest
from Telesecreter_Application.scheduale.dtos.update_schedule_dto import UpdateScheduleRequest
from Telesecreter_Application.scheduale.queries.get_all_scheduales_query import GetAllSchedualesQuery
from Telesecreter_Application.scheduale.commands.add_schedule_command import AddScheduleCommand
from Telesecreter_Application.scheduale.commands.update_schedule_command import UpdateScheduleCommand, ScheduleNotFoundException
from Telesecreter_Application.scheduale.commands.delete_schedule_command import DeleteScheduleCommand
from Telesecreter_Application.doctor.queries.get_doctor_availability_query import GetDoctorAvailabilityQuery
from Telesecreter_Application.doctor.Exceptions.doctor_exception_handlers import PastDateError
from Telesecreter_API.dependencies.dependency_injection import get_schedule_repo

router = APIRouter(prefix="/scheduales", tags=["Scheduales"])


@router.get("/", response_model=list[SchedualeDTO])
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


@router.post("/", response_model=SchedualeDTO, status_code=201)
def add_schedule(request: AddScheduleRequest, repo: IScheduleRepository = Depends(get_schedule_repo)):
    try:
        return AddScheduleCommand(repo).execute(request)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="A schedule for this doctor on that day already exists.")


@router.put("/{schedule_id}", response_model=SchedualeDTO)
def update_schedule(schedule_id: UUID, request: UpdateScheduleRequest, repo: IScheduleRepository = Depends(get_schedule_repo)):
    try:
        return UpdateScheduleCommand(repo).execute(schedule_id, request)
    except ScheduleNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{schedule_id}", status_code=204)
def delete_schedule(schedule_id: UUID, repo: IScheduleRepository = Depends(get_schedule_repo)):
    try:
        DeleteScheduleCommand(repo).execute(schedule_id)
    except ScheduleNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
