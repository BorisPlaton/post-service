from hashlib import sha256

from domain.user.command.register.command import RegisterUserCommand
from domain.user.exception.login_already_exist import LoginAlreadyExist
from domain.user.model.user import User
from domain.user.repository.user.interface import IUserRepository
from shared.message_bus.command_bus.handler.handler import ICommandHandler


class RegisterUserCommandHandler(ICommandHandler[int, RegisterUserCommand]):
    """
    The command handler for the register user command.

    Creates a new user in the system.
    """

    def __init__(
        self,
        user_repository: IUserRepository,
    ):
        """
        @param user_repository:
            The user repository that satisfies this `IUserRepository` interface.
        """
        self._user_repository = user_repository

    async def __call__(
        self,
        message: RegisterUserCommand,
    ) -> int:
        """
        Registers a new user in the system. The user with this login must be unique.
        Otherwise, exception is risen.

        @param message:
            Contains user's login and password.
        @raise LoginAlreadyExist:
            If the user already exists with provided login, then raises exception.
        @return:
            The id of the new created user.
        """
        if await self._user_repository.get_by_login(message.login):
            raise LoginAlreadyExist()

        user = User.create(
            login=message.login,
            password=sha256(message.password.encode()).hexdigest(),
        )
        await self._user_repository.create(entity=user)
        return user.id
