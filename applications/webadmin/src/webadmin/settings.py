from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BIND_HOST: str = "127.0.0.1"
    BIND_PORT: int = 2621
    BUILD_VERSION: str | None = None
    BUILD_SHA: str | None = None

    @property
    def version(self) -> str:
        return self.BUILD_VERSION or self.BUILD_SHA or "unknown"


def get_settings() -> Settings:
    return Settings()
