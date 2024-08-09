from dataclasses import dataclass

from shared.message_bus.command_bus.command import ICommand


@dataclass(kw_only=True, slots=True)
class ValidateTextCommand(ICommand):
    """
    The command for validating a text.
    """
    text: str
