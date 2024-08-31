from abc import ABC
from abc import abstractmethod
from functools import cached_property

from redis import Redis


class IRedisClient(ABC):

    @cached_property
    @abstractmethod
    def client(self) -> Redis: ...
