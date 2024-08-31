from functools import cached_property

from redis import Redis

from infrastructure.settings.redis import RedisSettings
from infrastructure.redis_.client.interface import IRedisClient


class RedisClient(IRedisClient):

    def __init__(
        self,
        settings: RedisSettings,
    ):
        self._settings = settings

    @cached_property
    def client(self) -> Redis:
        return Redis(
            host=self._settings.HOST,
            port=self._settings.PORT,
            password=self._settings.PASSWORD,
            db=self._settings.DB,
        )
