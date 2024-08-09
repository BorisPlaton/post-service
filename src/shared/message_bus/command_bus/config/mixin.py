from abc import ABC
from abc import abstractmethod
from functools import cached_property

from shared.message_bus.command_bus.config.options.base import ICommandOptions


class IConfigurableCommand(ABC):

    @abstractmethod
    @cached_property
    def config[T: ICommandOptions](self) -> dict[type[T], T]:
        raise NotImplementedError()
