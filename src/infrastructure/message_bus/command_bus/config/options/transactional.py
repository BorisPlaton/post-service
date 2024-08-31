from dataclasses import dataclass

from infrastructure.message_bus.command_bus.config.options.base import ICommandOptions


@dataclass(kw_only=True, slots=True)
class TransactionalOption(ICommandOptions):
    is_transactional: bool = True
