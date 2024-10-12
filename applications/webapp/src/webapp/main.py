from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import cast

import uvloop
from core.di import Deps as CoreDeps
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from hypercorn.asyncio import serve
from hypercorn.config import Config
from hypercorn.typing import ASGIFramework
from that_depends.providers.context_resources import DIContextMiddleware

from webapp.di import Deps
from webapp.routers.root import router as root_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    try:
        yield
    finally:
        await Deps.tear_down()
        await CoreDeps.tear_down()


def make_app(static_dir: Path, version: str) -> FastAPI:
    app = FastAPI(
        title="webapp",
        version=version,
    )
    app.add_middleware(DIContextMiddleware)
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    app.include_router(root_router, prefix="")
    return app


def entrypoint() -> None:
    settings = Deps.settings.sync_resolve()
    core_settings = Deps.core_settings.sync_resolve()
    static_dir = Deps.static_dir.sync_resolve()
    app = make_app(static_dir=static_dir, version=core_settings.version)
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
