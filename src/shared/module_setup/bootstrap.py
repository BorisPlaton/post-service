from abc import abstractmethod
from functools import cached_property
from typing import Iterable

from punq import Container

from shared.module_setup.module import IModule


class ModulesConfig:

    def __init__(
        self,
        modules: Iterable[IModule],
        container: Container,
    ):
        self._modules = modules
        self._container = container

    @abstractmethod
    def setup(self) -> None:
        for module in self._modules:
            module.configure(
                container=self._container,
            )

    @cached_property
    @abstractmethod
    def container(self) -> Container:
        return self._container
