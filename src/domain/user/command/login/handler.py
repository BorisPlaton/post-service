from hashlib import sha256

from domain.jwt_token.command.issue_jwt.command import IssueJWTCommand
from domain.jwt_token.types.jwt_payload import JWTPayloadBody
from domain.user.command.login.command import LogInUserCommand
from domain.user.exception.invalid_password_provided import InvalidPasswordProvided
from domain.user.exception.user_with_provided_login_doesnt_exist import UserWithProvidedLoginDoesntExist
from domain.user.repository.user.interface import IUserRepository
from infrastructure.message_bus.command_bus.bus.interface import ICommandBus
from infrastructure.message_bus.command_bus.handler.interface import ICommandHandler


class LogInUserCommandHandler(ICommandHandler[LogInUserCommand, str]):
    """
    The command handler to log in user.

    If client is successfully logged in, it will return a JWT.
    """

    def __init__(
        self,
        user_repository: IUserRepository,
        command_bus: ICommandBus,
    ):
        """
        @param user_repository:
            The user repository that satisfies this `IUserRepository` interface.
        """
        self._user_repository = user_repository
        self._command_bus = command_bus

    async def __call__(
        self,
        message: LogInUserCommand,
    ) -> str:
        """
        Authenticates a user. If the user is successfully logged in, it will return a JWT.

        @param message:
            Contains user's credentials.
        @raise UserWithProvidedLoginDoesntExist:
            If the user doesn't exist, raises an exception.
        @raise InvalidPasswordProvided:
            If the provided user's password is invalid, raises an exception.
        @return:
            The new generated JWT.
        """
        user = await self._user_repository.get_by_login(message.login)

        if not user:
            raise UserWithProvidedLoginDoesntExist()
        elif user.password != sha256(message.password.encode()).hexdigest():
            raise InvalidPasswordProvided()

        return await self._command_bus.handle(
            message=IssueJWTCommand(
                payload=JWTPayloadBody(
                    user_id=user.id,
                )
            )
        )
