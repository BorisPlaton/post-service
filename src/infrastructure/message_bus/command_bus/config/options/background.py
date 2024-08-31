from dataclasses import dataclass

from infrastructure.message_bus.command_bus.config.options.base import ICommandOptions


@dataclass(kw_only=True, slots=True)
class BackgroundExecutionOption(ICommandOptions):
    is_background: bool = True
    enqueue_in: int = 60 * 60
