from dataclasses import dataclass

from shared.message_bus.command_bus.command import ICommand


@dataclass(kw_only=True, slots=True)
class RegisterUserCommand(ICommand):
    """
    The command to register a new user.
    """
    login: str
    password: str
