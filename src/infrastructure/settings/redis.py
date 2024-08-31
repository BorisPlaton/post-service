from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class RedisSettings(BaseSettings):
    """
    Redis settings.

    Configures from environment variables.
    """
    model_config = SettingsConfigDict(env_prefix="REDIS_")

    HOST: str
    PORT: int
    PASSWORD: str
    DB: int
