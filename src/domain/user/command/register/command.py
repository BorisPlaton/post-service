from dataclasses import dataclass
from dataclasses import field

from infrastructure.message_bus.command_bus.command import ICommand
from infrastructure.message_bus.command_bus.config.mixin.abstract import AbstractConfigurableCommand
from infrastructure.message_bus.command_bus.config.options.base import ICommandOptions
from infrastructure.message_bus.command_bus.config.options.transactional import TransactionalOption


@dataclass(kw_only=True, slots=True)
class RegisterUserCommand(
    ICommand,
    AbstractConfigurableCommand,
):
    """
    The command to register a new user.
    """
    login: str
    password: str

    command_config: dict[type[ICommandOptions], ICommandOptions] = field(
        default_factory=lambda: {
            TransactionalOption: TransactionalOption(
                is_transactional=True,
            ),
        },
    )
