from abc import ABC
from abc import abstractmethod

from punq import Container


class IModule(ABC):

    @abstractmethod
    def configure(
        self,
        container: Container,
    ) -> None:
        raise NotImplementedError()
