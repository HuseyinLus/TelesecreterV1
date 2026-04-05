from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from Telesecretary.Infrastructure.data_access.configurations.database import get_session
from Telesecretary.Infrastructure.data_access.configurations.unit_of_work import UnitOfWork

from Telesecretary.Application.users.commands.register_user_command import RegisterUserCommand, RegisterUserCommandHandler
from Telesecretary.Application.users.queries.get_user_query import GetUserQuery, GetUserQueryHandler
from Telesecretary.Application.users.dtos.user_dto import UserDTO

router = APIRouter(prefix="/users", tags=["Users"])

async def get_uow(session: AsyncSession = Depends(get_session)):
    """Dependency injection helper to provide the UnitOfWork"""
    return UnitOfWork(session)

@router.post("/", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
async def register_user_endpoint(command: RegisterUserCommand, uow: UnitOfWork = Depends(get_uow)):
    """
    Registers a new user in the system using the Command pattern.
    """
    try:
        handler = RegisterUserCommandHandler(uow)
        user = await handler.handle(command)
        return UserDTO.model_validate(user)
        
    except ValueError as e:
        # e.g., "A user with this email already exists"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{user_id}", response_model=UserDTO)
async def get_user_endpoint(user_id: UUID, uow: UnitOfWork = Depends(get_uow)):
    """
    Retrieves a user by their unique ID using the Query pattern.
    """
    query = GetUserQuery(user_id=user_id)
    handler = GetUserQueryHandler(uow)
    
    user = await handler.handle(query)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    return UserDTO.model_validate(user)
