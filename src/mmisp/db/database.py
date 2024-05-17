import contextlib
from typing import AsyncIterator, Self, TypeAlias

from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from mmisp.db.config import config

Session: TypeAlias = AsyncSession

# , poolclass=NullPool)
# async_session = sessionmaker(autoflush=False, expire_on_commit=False, class_=AsyncSession, bind=engine)

Base = declarative_base()


class DatabaseSessionManager:
    def __init__(self: Self) -> None:
        self._engine: AsyncEngine | None = None
        self._sessionmaker: sessionmaker | None = None

        self._url = make_url(config.DATABASE_URL)

    def init(self: Self) -> None:
        if config.DEBUG:
            self._engine = create_async_engine(self._url, echo=True)
        else:
            self._engine = create_async_engine(self._url)
        self._sessionmaker = sessionmaker(
            autocommit=False, expire_on_commit=False, bind=self._engine, class_=AsyncSession
        )

    async def close(self: Self) -> None:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self: Self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self: Self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    # Used for testing
    async def create_all(self: Self, engine: AsyncEngine | None = None) -> None:
        if engine is None:
            engine = self._engine
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self: Self, engine: AsyncEngine | None = None) -> None:
        if engine is None:
            engine = self._engine
        await engine.run_sync(Base.metadata.drop_all)


async def get_db() -> Session:
    async with sessionmanager.session() as session:
        yield session


async def create_all_models() -> None:
    await sessionmanager.create_all()


sessionmanager = DatabaseSessionManager()
