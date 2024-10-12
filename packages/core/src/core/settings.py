from pydantic import SecretStr
from pydantic_settings import BaseSettings
from sqlalchemy import URL
from sqlalchemy.util import immutabledict


class Settings(BaseSettings):
    DEV: bool = False
    BUILD_VERSION: str | None = None
    BUILD_SHA: str | None = None

    @property
    def version(self) -> str:
        return self.BUILD_VERSION or self.BUILD_SHA or "unknown"

    PGUSER: str
    PGPASSWORD: SecretStr
    PGDATABASE: str
    PGHOST: str
    PGPORT: int = 5432

    @property
    def db_url(self) -> URL:
        return URL(
            drivername="asyncpg",
            username=self.PGUSER,
            password=self.PGPASSWORD.get_secret_value(),
            database=self.PGDATABASE,
            host=self.PGHOST,
            port=self.PGPORT,
            query=immutabledict(),
        )
