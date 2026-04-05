from fastapi import APIRouter, Depends
from Telesecreter_Application.user.dtos.user_dto import UserDTO
from Telesecreter_Application.user.queries.get_all_users_query import GetAllUsersQuery
from Telesecreter_Infrastructure.data_access.repositories.user_repository import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])


def get_query() -> GetAllUsersQuery:
    return GetAllUsersQuery(user_repository=UserRepository())


@router.get("/", response_model=list[UserDTO])
def get_all_users(query: GetAllUsersQuery = Depends(get_query)):
    return query.execute()