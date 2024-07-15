from punq import Container

from settings.config.app import ApplicationSettings
from settings.config.database import DatabaseSettings
from settings.config.gemini import GeminiSettings
from shared.module_setup.module import IModule


class SettingsModule(IModule):

    def configure(
        self,
        container: Container,
    ) -> None:
        container.register(
            DatabaseSettings,
            instance=DatabaseSettings(),
        )
        container.register(
            ApplicationSettings,
            instance=ApplicationSettings(),
        )
        container.register(
            GeminiSettings,
            instance=GeminiSettings(),
        )
