from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class ApplicationSettings(BaseSettings):
    """
    General application settings.

    Configures from environment variables.
    """
    model_config = SettingsConfigDict(env_prefix="APP_")

    DESCRIPTION: str
    VERSION: str
    DEBUG: bool
    SECRET_KEY: str
