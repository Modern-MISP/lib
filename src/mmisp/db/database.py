import asyncio
import contextlib
import logging
import os
import time
from collections.abc import AsyncIterator
from contextvars import ContextVar
from typing import ClassVar, Self, TypeAlias, TypedDict

from alembic.config import Config as AlembicConfig
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import MetaData
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeMeta, Mapped, declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

from mmisp.db.config import config

logger = logging.getLogger(__name__)


def _build_alembic_config() -> AlembicConfig:
    """Build an Alembic Config pointing to the bundled migrations directory.

    All configuration is set programmatically — no alembic.ini file required.
    """
    migrations_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "migrations"))

    cfg = AlembicConfig()
    cfg.set_main_option("script_location", migrations_dir)
    cfg.set_main_option("sqlalchemy.url", "")
    return cfg


async def _check_migration_status(engine: AsyncEngine) -> None:
    """Check if the database is on the latest Alembic revision.

    Logs a warning if pending migrations exist. Never raises.
    """
    try:
        cfg = _build_alembic_config()
        script = ScriptDirectory.from_config(cfg)
        expected_heads = set(script.get_heads())

        def _get_current_heads(connection: object) -> set[str]:
            ctx = MigrationContext.configure(connection)  # type: ignore[arg-type]
            return set(ctx.get_current_heads())

        async with engine.connect() as conn:
            current_heads = await conn.run_sync(_get_current_heads)

        if current_heads != expected_heads:
            logger.warning(
                "Database is not up to date. "
                "Current heads: %s, expected: %s. "
                "Run 'mmisp-db db-upgrade' to apply pending migrations.",
                current_heads,
                expected_heads,
            )
    except Exception as exc:
        logger.warning("Could not check migration status: %s", exc)


Session: TypeAlias = AsyncSession

# , poolclass=NullPool)
# async_session = sessionmaker(autoflush=False, expire_on_commit=False, class_=AsyncSession, bind=engine)

# Base = declarative_base()


def generate_typeddict_for_model(model_cls: type) -> type[TypedDict]:
    hints = model_cls.__annotations__
    #    get_type_hints(model_cls, include_extras=True)
    fields = {}
    for attr, typ in hints.items():
        if getattr(typ, "__origin__", None) is Mapped:
            inner_type = typ.__args__[0]
            fields[attr] = inner_type
    td = TypedDict(str(model_cls.__name__) + "Dict", fields)
    return td


class AutoDictMeta(DeclarativeMeta):
    def __new__(mcs, name, bases, namespace):  # noqa
        cls = super().__new__(mcs, name, bases, namespace)
        if "__tablename__" in namespace:  # Only real tables
            td = generate_typeddict_for_model(cls)
            cls.__annotations__["DictType"] = ClassVar[td]  # Store for typing
        return cls


_naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

Base = declarative_base(metaclass=AutoDictMeta, metadata=MetaData(naming_convention=_naming_convention))

_no_database: str = "DatabaseSessionManager is not initialized"

dry_run: ContextVar[bool] = ContextVar("dry_run", default=False)


class DatabaseSessionManager:
    def __init__(self: Self, db_url: str = config.DATABASE_URL) -> None:
        self._engine: AsyncEngine | None = None
        self._sessionmaker: sessionmaker | None = None

        self._url = make_url(db_url)

    def init(self: Self, nullpool: bool = False) -> None:
        retries = 0
        while retries < config.MAX_RETRIES:
            try:
                if nullpool:
                    self._engine = create_async_engine(
                        self._url, echo=False, hide_parameters=not (config.DEBUG), poolclass=NullPool
                    )
                else:
                    self._engine = create_async_engine(
                        self._url, echo=False, hide_parameters=not (config.DEBUG), pool_recycle=3600
                    )
                break
            except OperationalError as e:
                retries += 1
                print(f"Attempt {retries} failed: {e}")
                time.sleep(config.RETRY_SLEEP)
        self._sessionmaker = sessionmaker(
            autocommit=False, autoflush=False, expire_on_commit=False, bind=self._engine, class_=AsyncSession
        )

        # Check migration status (non-blocking warning only)
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(_check_migration_status(self._engine))
        except RuntimeError:
            # No running event loop — create one
            asyncio.run(_check_migration_status(self._engine))

    async def close(self: Self) -> None:
        if self._engine is None:
            raise Exception(_no_database)
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self: Self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception(_no_database)

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self: Self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception(_no_database)

        session = self._sessionmaker()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    # Used for testing
    async def create_all(self: Self, engine: AsyncEngine | None = None) -> None:
        if engine is None:
            engine = self._engine

        retries = 0
        while retries < config.MAX_RETRIES:
            try:
                async with engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)
                break
            except OperationalError as e:
                retries += 1
                print(f"Attempt {retries} failed: {e}")
                time.sleep(config.RETRY_SLEEP)

    async def drop_all(self: Self, engine: AsyncEngine | None = None) -> None:
        if engine is None:
            engine = self._engine
        assert engine is not None
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)  # type:ignore[attr-defined]


async def get_db() -> AsyncIterator[Session]:
    async with sessionmanager.session() as session:
        yield session
        if dry_run.get():
            await session.rollback()


async def create_all_models() -> None:
    await sessionmanager.create_all()


sessionmanager = None
if config.CONNECTION_INIT:
    sessionmanager = DatabaseSessionManager()
    sessionmanager.init()
