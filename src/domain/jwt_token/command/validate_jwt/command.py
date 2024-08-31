from dataclasses import dataclass

from infrastructure.message_bus.command_bus.command import ICommand


@dataclass(kw_only=True, slots=True)
class ValidateJWTCommand(ICommand):
    """
    Command to validate a JWT.
    """
    token: str
