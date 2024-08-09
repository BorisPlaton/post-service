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

        self._container.register(
            service=ModulesConfig,
            instance=self,
        )

    def setup(self) -> None:
        for module in self._modules:
            module.configure(
                container=self._container,
            )

    @property
    def container(self) -> Container:
        return self._container

    @property
    def modules(self) -> Iterable[IModule]:
        return self._modules
