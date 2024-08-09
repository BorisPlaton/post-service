from dataclasses import dataclass

from shared.message_bus.command_bus.config.options.base import ICommandOptions


@dataclass(kw_only=True, slots=True, frozen=True)
class TransactionalOption(ICommandOptions):
    is_transactional: bool
