from typing import Literal, cast

import uvloop
from fastapi import FastAPI
from hypercorn.asyncio import serve
from hypercorn.config import Config
from hypercorn.typing import ASGIFramework
from pydantic import BaseModel

from webadmin.settings import Settings, get_settings


class Healthz(BaseModel):
    status: Literal["OK"]


def make_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title="webadmin",
        version=settings.version,
    )

    @app.get("/healthz")
    def healthz() -> Healthz:
        return Healthz(status="OK")

    return app


def entrypoint() -> None:
    settings = get_settings()
    app = make_app(settings)
    config = Config.from_mapping(
        bind=f"{settings.BIND_HOST}:{settings.BIND_PORT}",
    )
    uvloop.run(
        serve(
            app=cast(ASGIFramework, app),
            config=config,
            mode="asgi",
        )
    )
