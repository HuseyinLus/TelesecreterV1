from uuid import UUID
from Telesecreter_Domain.interfaces.i_user_repository import IUserRepository
from Telesecreter_Application.user.dtos.user_dto import UserDTO
from Telesecreter_Domain.exceptions.user_not_found_exception import UserNotFoundException


class GetUserByIdQuery:

    def __init__(self, user_repository: IUserRepository):
        self._repository = user_repository

    def execute(self, user_id: UUID) -> UserDTO:
        user = self._repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundException(user_id)
        return UserDTO.from_entity(user)
