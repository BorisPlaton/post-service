from dataclasses import dataclass

from infrastructure.message_bus.command_bus.command import ICommand


@dataclass(kw_only=True, slots=True)
class LogInUserCommand(ICommand):
    """
    The command to log in user.
    """
    login: str
    password: str
