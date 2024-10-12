from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from that_depends import BaseContainer
from that_depends.providers import (
    ContextResource,
    Singleton,
)

from core.settings import Settings


def create_db_engine(settings: Settings) -> AsyncEngine:
    return create_async_engine(settings.db_url)


async def create_session(
    sessionmaker: async_sessionmaker,
) -> AsyncIterator[AsyncSession]:
    async with sessionmaker() as session:
        yield session


class Deps(BaseContainer):
    settings: Singleton[Settings] = Singleton(Settings)  # pyright: ignore[reportCallIssue]
    db_engine: Singleton[AsyncEngine] = Singleton(
        create_db_engine, settings=settings.cast
    )
    sessionmaker: Singleton[async_sessionmaker] = Singleton(
        async_sessionmaker,
        bind=db_engine.cast,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    session: ContextResource[AsyncSession] = ContextResource(
        create_session,
        sessionmaker=sessionmaker.cast,
    )
