from fastapi import APIRouter, Depends

from Telesecreter_Domain.interfaces.i_user_repository import IUserRepository
from Telesecreter_Application.user.dtos.user_dto import UserDTO
from Telesecreter_Application.user.queries.get_all_users_query import GetAllUsersQuery
from Telesecreter_API.dependencies.dependency_injection import get_user_repo

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserDTO])
def get_all_users(repo: IUserRepository = Depends(get_user_repo)):
    return GetAllUsersQuery(repo).execute()