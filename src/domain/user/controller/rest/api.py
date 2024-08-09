from typing import Annotated

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import status
from punq import Container

from domain.user.controller.rest.contracts.input.login import UserLoginInput
from domain.user.controller.rest.contracts.input.register import RegisterUserInput
from domain.user.controller.rest.contracts.output.token import UserJWTOutput
from shared.fastapi_.dependency.registry import get_registry
from shared.message_bus.command_bus.bus.interface import ICommandBus


router = APIRouter(
    prefix='/user',
    tags=[tag := 'User'],
)


@router.post(
    '/register/',
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_info: Annotated[RegisterUserInput, Body(description=RegisterUserInput.__doc__)],
    registry: Annotated[Container, Depends(get_registry)],
) -> int:
    """
    Registers a new user in the system and returns its `id`.
    """
    return await registry.resolve(ICommandBus).handle(user_info.to_command())


@router.post(
    '/login/',
    status_code=status.HTTP_200_OK,
)
async def login(
    credentials: Annotated[UserLoginInput, Body(description=UserLoginInput.__doc__)],
    registry: Annotated[Container, Depends(get_registry)],
) -> UserJWTOutput:
    """
    Authenticates a client and returns a new JWT.
    """
    return UserJWTOutput(
        access_token=await registry.resolve(ICommandBus).handle(credentials.to_command()),
        token_type='Bearer',
    )
