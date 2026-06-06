from uuid import UUID
from Telesecreter_Domain.interfaces.i_user_repository import IUserRepository
from Telesecreter_Application.user.dtos.update_user_dto import UpdateUserRequest
from Telesecreter_Application.user.dtos.user_dto import UserDTO
from Telesecreter_Application.user.exceptions.user_exception_handlers import UserNotFoundException


class UpdateUserCommand:

    def __init__(self, user_repo: IUserRepository):
        self._user_repo = user_repo

    def execute(self, user_id: UUID, request: UpdateUserRequest) -> UserDTO:
        user = self._user_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundException(user_id)

        if request.full_name is not None:
            user.full_name = request.full_name
        if request.phone_number is not None:
            user.phone_number = request.phone_number
        if request.email is not None:
            user.email = request.email
        if request.hashed_password is not None:
            user.hashed_password = request.hashed_password
        if request.role is not None:
            user.role = request.role
        if request.is_active is not None:
            user.is_active = request.is_active

        self._user_repo.update(user)
        return UserDTO.from_entity(user)
