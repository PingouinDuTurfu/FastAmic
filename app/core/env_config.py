from pathlib import Path

from pydantic_settings import BaseSettings

ENV_FILE = ".env"

class Settings(BaseSettings):
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE_MAIN: str
    MYSQL_DATABASE_AUX: str
    MYSQL_DATABASE_NOTIFICATIONS: str
    MYSQL_POOL_SIZE_MIN: int
    MYSQL_POOL_SIZE_MAX: int
    MYSQL_RETRY_LIMIT: int
    MYSQL_RETRY_DELAY_SECONDS: int

    RMQ_HOST: str
    RMQ_PORT: int
    RMQ_USER: str
    RMQ_PASSWORD: str
    RMQ_VHOST: str

    ELASTIC_LOGS_URL: str
    ELASTIC_BULK_SIZE: int
    ELASTIC_FLUSH_INTERVAL: int

    class Config:
        env_file = ENV_FILE

env_file = Path(ENV_FILE)

if not env_file.is_file():
    raise FileNotFoundError(f".env file not found at {env_file.resolve()}")

settings = Settings()