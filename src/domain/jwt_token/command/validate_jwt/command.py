from dataclasses import dataclass

from shared.message_bus.command_bus.interface.command import ICommand


@dataclass(kw_only=True, slots=True)
class ValidateJWTCommand(ICommand):
    """
    Command to validate a JWT.
    """
    token: str
