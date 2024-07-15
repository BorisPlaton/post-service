from abc import ABC
from abc import abstractmethod


class IAIClient(ABC):

    @abstractmethod
    def send(
        self,
        message: str,
    ) -> str:
        raise NotImplementedError()
