from uuid import UUID
from Telesecreter_Domain.interfaces.i_user_repository import IUserRepository
from Telesecreter_Application.user.exceptions.user_exception_handlers import UserNotFoundException


class DeleteUserCommand:

    def __init__(self, user_repo: IUserRepository):
        self._user_repo = user_repo

    def execute(self, user_id: UUID) -> None:
        if self._user_repo.get_by_id(user_id) is None:
            raise UserNotFoundException(user_id)
        self._user_repo.delete(user_id)
