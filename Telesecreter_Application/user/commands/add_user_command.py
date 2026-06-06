from Telesecreter_Domain.entities.user import User
from Telesecreter_Domain.interfaces.i_user_repository import IUserRepository
from Telesecreter_Application.user.dtos.add_user_dto import AddUserRequest
from Telesecreter_Application.user.dtos.user_dto import UserDTO


class AddUserCommand:

    def __init__(self, user_repo: IUserRepository):
        self._user_repo = user_repo

    def execute(self, request: AddUserRequest) -> UserDTO:
        user = User(
            full_name=request.full_name,
            phone_number=request.phone_number,
            email=request.email,
            hashed_password=request.hashed_password,
            role=request.role,
            is_active=request.is_active,
        )
        self._user_repo.add(user)
        return UserDTO.from_entity(user)
