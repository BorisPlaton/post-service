from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class GeminiSettings(BaseSettings):
    """
    Gemini settings.

    Configures from environment variables.
    """
    model_config = SettingsConfigDict(env_prefix="GEMINI_")

    API_KEY: str
