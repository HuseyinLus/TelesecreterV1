from fastapi import APIRouter, Depends

from Telesecreter_Domain.interfaces.i_scheduale_repository import IScheduleRepository
from Telesecreter_Application.scheduale.queries.get_all_scheduales_query import GetAllSchedualesQuery
from Telesecreter_Application.scheduale.dtos import scheduale_dto
from Telesecreter_API.dependencies.dependency_injection import get_schedule_repo

router = APIRouter(prefix="/scheduales", tags=["Scheduales"])

@router.get("/", response_model=list[scheduale_dto.SchedualeDTO])
def get_all_scheduales(repo: IScheduleRepository = Depends(get_schedule_repo)):
    return GetAllSchedualesQuery(repo).execute()
