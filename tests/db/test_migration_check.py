# tests/db/test_migration_check.py
import logging
import os
from unittest.mock import patch

import pytest
import pytest_asyncio
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from mmisp.db.database import _check_migration_status


@pytest_asyncio.fixture
async def sqlite_engine(tmp_path):
    """A fresh SQLite engine with no tables — simulates a brand new DB."""
    db_path = tmp_path / "test.db"
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{db_path}",
        poolclass=NullPool,
    )
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def migrated_engine(tmp_path):
    """SQLite engine with alembic_version set to the current head via stamp."""
    from alembic.config import Config
    from alembic.runtime.migration import MigrationContext
    from alembic.script import ScriptDirectory

    db_path = tmp_path / "migrated.db"

    base_path = os.path.dirname(os.path.abspath(__file__))
    migrations_dir = os.path.abspath(os.path.join(base_path, "../../src/mmisp/db/migrations"))

    cfg = Config()
    cfg.set_main_option("script_location", migrations_dir)
    cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")

    # Stamp the DB at head using a sync connection (no DDL run, just marks version)
    script = ScriptDirectory.from_config(cfg)
    sync_engine = sqlalchemy.create_engine(f"sqlite:///{db_path}")
    with sync_engine.connect() as conn:
        ctx = MigrationContext.configure(conn)
        ctx.stamp(script, "head")
        conn.commit()
    sync_engine.dispose()

    engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}", poolclass=NullPool)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def outdated_engine(tmp_path):
    """SQLite engine with alembic_version set to a fake old revision."""
    db_path = tmp_path / "outdated.db"
    sync_url = f"sqlite:///{db_path}"
    sync_engine = sqlalchemy.create_engine(sync_url)
    with sync_engine.connect() as conn:
        conn.execute(sqlalchemy.text("CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL)"))
        conn.execute(sqlalchemy.text("INSERT INTO alembic_version (version_num) VALUES ('deadbeef0000')"))
        conn.commit()
    sync_engine.dispose()

    engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}", poolclass=NullPool)
    yield engine
    await engine.dispose()


@pytest.mark.asyncio
async def test_up_to_date_db_no_warning(migrated_engine, caplog):
    """A DB at the current head should not produce any warnings."""
    with caplog.at_level(logging.WARNING, logger="mmisp.db.database"):
        await _check_migration_status(migrated_engine)
    assert "not up to date" not in caplog.text


@pytest.mark.asyncio
async def test_outdated_db_logs_warning(outdated_engine, caplog):
    """A DB with a stale revision should log a warning."""
    with caplog.at_level(logging.WARNING, logger="mmisp.db.database"):
        await _check_migration_status(outdated_engine)
    assert "not up to date" in caplog.text
    assert "mmisp-db db-upgrade" in caplog.text


@pytest.mark.asyncio
async def test_fresh_db_no_alembic_version_logs_warning(sqlite_engine, caplog):
    """A brand new DB with no alembic_version table should log a warning."""
    with caplog.at_level(logging.WARNING, logger="mmisp.db.database"):
        await _check_migration_status(sqlite_engine)
    assert "not up to date" in caplog.text
    assert "mmisp-db db-upgrade" in caplog.text


@pytest.mark.asyncio
async def test_bad_alembic_config_logs_warning(sqlite_engine, caplog):
    """If the Alembic config cannot be found, log a warning but don't raise."""
    with patch(
        "mmisp.db.database._build_alembic_config",
        side_effect=FileNotFoundError("alembic.ini not found"),
    ):
        with caplog.at_level(logging.WARNING, logger="mmisp.db.database"):
            await _check_migration_status(sqlite_engine)
    assert "Could not check migration status" in caplog.text
