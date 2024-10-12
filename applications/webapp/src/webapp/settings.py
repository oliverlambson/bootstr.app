from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BIND_HOST: str = "127.0.0.1"
    BIND_PORT: int = 2620
