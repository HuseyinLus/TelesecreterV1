from Telesecreter_Domain.interfaces.i_user_repository import IUserRepository
from Telesecreter_Application.user.dtos.get_user_by_phone_dto import GetUserByPhoneDTO
from Telesecreter_Application.user.exceptions.user_exception_handlers import PhoneNumberNotFoundException


class GetUserByPhoneQuery:

    def __init__(self, user_repository: IUserRepository):
        self._repository = user_repository

    def execute(self, phone_number: str) -> GetUserByPhoneDTO:
        user = self._repository.get_by_phone(phone_number)
        if user is None:
            raise PhoneNumberNotFoundException(phone_number)
        return GetUserByPhoneDTO.from_entity(user)
