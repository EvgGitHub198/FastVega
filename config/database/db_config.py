from typing import Optional

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


from decouple import config


class ConfigDataBase:
    POSTGRES_USER = config('POSTGRES_USER', default='')
    POSTGRES_PASSWORD = config('POSTGRES_PASSWORD', default='')
    POSTGRES_HOST = config('POSTGRES_HOST', default='')
    POSTGRES_PORT = config('POSTGRES_PORT', default='')
    POSTGRES_DB = config('POSTGRES_DB', default='')
    DB_ECHO_LOG = config('DB_ECHO_LOG', default='', cast=bool)

    @property
    def database_url(self) -> Optional[PostgresDsn]:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings_db = ConfigDataBase()