from Telesecreter_Domain.interfaces.i_user_repository import IUserRepository
from Telesecreter_Application.user.dtos.user_dto import UserDTO


class GetAllUsersQuery:

    def __init__(self, user_repository: IUserRepository):
        self._repository = user_repository

    def execute(self) -> list[UserDTO]:
        users = self._repository.get_all()
        return [UserDTO.from_entity(user) for user in users]