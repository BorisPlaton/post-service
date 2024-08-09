from punq import Container

from settings.config.app import ApplicationSettings
from settings.config.database import DatabaseSettings
from settings.config.ai import AISettings
from settings.config.redis import RedisSettings
from shared.module_setup.module import IModule


class SettingsModule(IModule):

    def configure(
        self,
        container: Container,
    ) -> None:
        container.register(
            service=DatabaseSettings,
            instance=DatabaseSettings(),
        )
        container.register(
            service=ApplicationSettings,
            instance=ApplicationSettings(),
        )
        container.register(
            service=AISettings,
            instance=AISettings(),
        )
        container.register(
            service=RedisSettings,
            instance=RedisSettings(),
        )
