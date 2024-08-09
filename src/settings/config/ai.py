from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class AISettings(BaseSettings):
    """
    AI settings.

    Configures from environment variables.
    """
    model_config = SettingsConfigDict(env_prefix="AI_")

    API_KEY: str
