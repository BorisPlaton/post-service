from abc import ABC

from infrastructure.message_bus.command_bus.config.mixin.interface import IConfigurableCommand
from infrastructure.message_bus.command_bus.config.options.base import ICommandOptions


class AbstractConfigurableCommand[T: ICommandOptions](
    IConfigurableCommand[T],
    ABC,
):

    def add_config(
        self,
        config: T,
    ) -> None:
        self.command_config[config.__class__] = config

    def update_config(
        self,
        config: type[T],
        **kwargs,
    ) -> None:
        command_config = self.command_config[config]
        for option, value in kwargs.items():
            setattr(command_config, option, value)
