from dataclasses import dataclass

from shared.message_bus.command_bus.config.options.base import CommandOptions


@dataclass(kw_only=True, slots=True, frozen=True)
class TransactionalOption(CommandOptions):
    is_transactional: bool
