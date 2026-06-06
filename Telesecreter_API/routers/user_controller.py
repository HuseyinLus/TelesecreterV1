from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from Telesecreter_Domain.interfaces.i_user_repository import IUserRepository
from Telesecreter_Application.user.exceptions.user_exception_handlers import UserNotFoundException
from Telesecreter_Application.user.dtos.user_dto import UserDTO
from Telesecreter_Application.user.dtos.add_user_dto import AddUserRequest
from Telesecreter_Application.user.dtos.update_user_dto import UpdateUserRequest
from Telesecreter_Application.user.queries.get_all_users_query import GetAllUsersQuery
from Telesecreter_Application.user.queries.get_user_by_id_query import GetUserByIdQuery
from Telesecreter_Application.user.commands.add_user_command import AddUserCommand
from Telesecreter_Application.user.commands.update_user_command import UpdateUserCommand
from Telesecreter_Application.user.commands.delete_user_command import DeleteUserCommand
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
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=UserDTO, status_code=201)
def add_user(request: AddUserRequest, repo: IUserRepository = Depends(get_user_repo)):
    return AddUserCommand(repo).execute(request)


@router.put("/{user_id}", response_model=UserDTO)
def update_user(user_id: UUID, request: UpdateUserRequest, repo: IUserRepository = Depends(get_user_repo)):
    try:
        return UpdateUserCommand(repo).execute(user_id, request)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: UUID, repo: IUserRepository = Depends(get_user_repo)):
    try:
        DeleteUserCommand(repo).execute(user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))