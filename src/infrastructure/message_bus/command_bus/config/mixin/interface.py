from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass

from infrastructure.message_bus.command_bus.config.options.base import ICommandOptions


@dataclass(kw_only=True, slots=True)
class IConfigurableCommand[T: ICommandOptions](ABC):

    @property
    @abstractmethod
    def command_config(self) -> dict[type[T], T]:
        raise NotImplementedError()

    @abstractmethod
    def add_config(
        self,
        config: T,
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    def update_config(
        self,
        config: T,
        **kwargs,
    ) -> None:
        raise NotImplementedError()
