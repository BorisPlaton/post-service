from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from punq import Container

from domain.jwt_token.command.validate_jwt.command import ValidateJWTCommand
from domain.jwt_token.types.jwt_payload import JWTPayloadBody
from domain.user.exception.user_with_provided_login_doesnt_exist import UserWithProvidedLoginDoesntExist
from domain.user.model import User
from domain.user.repository.user.interface import IUserRepository
from application.web.dependency import get_registry
from infrastructure.message_bus.command_bus.bus.interface import ICommandBus


bearer = HTTPBearer()


async def get_user(
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
    registry: Annotated[Container, Depends(get_registry)],
) -> User:
    """
    The dependency that enforces clients to send JWT to authenticate in the system.

    @param auth_creds:
        The authorization credentials.
    @param registry:
        The DI container.
    @return:
        The user record.
    """
    payload: JWTPayloadBody = await registry.resolve(ICommandBus).handle(
        message=ValidateJWTCommand(
            token=auth_creds.credentials,
        ),
    )

    if not (user := await registry.resolve(IUserRepository).get(id_=payload.user_id)):
        raise UserWithProvidedLoginDoesntExist()

    return user
