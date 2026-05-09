from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from Telesecreter_Domain.interfaces.i_user_repository import IUserRepository
from Telesecreter_Application.user.exceptions.user_exception_handlers import UserNotFoundException
from Telesecreter_Application.user.dtos.user_dto import UserDTO
from Telesecreter_Application.user.queries.get_all_users_query import GetAllUsersQuery
from Telesecreter_Application.user.queries.get_user_by_id_query import GetUserByIdQuery
from Telesecreter_API.dependencies.dependency_injection import get_user_repo

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserDTO])
def get_all_users(repo: IUserRepository = Depends(get_user_repo)):
    return GetAllUsersQuery(repo).execute()


@router.get("/{user_id}", response_model=UserDTO)
def get_user_by_id(user_id: UUID, repo: IUserRepository = Depends(get_user_repo)):
    try:
        return GetUserByIdQuery(repo).execute(user_id)
    except UserNotFoundException as e:
        return JSONResponse(status_code=404, content={"detail": str(e)})