#!/usr/bin/env python3

"""
USAGE:
    - Run `python -m mmisp.db.print_changes`
"""

import asyncio
import pprint
from collections import defaultdict

from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from sqlalchemy import MetaData

import mmisp.db.all_models  # noqa

from .database import Base, sessionmanager

metadata = MetaData()


translate_table = {
    "remove_table": "table_to_be_added_in_mmisp",
    "remove_column": "column_to_be_added_in_mmisp",
    "remove_index": "index_to_be_added_in_mmisp",
    "modify_nullable": "fix_nullable_in_mmisp",
    "add_column": "column_not_in_legacy_misp",
}


def create_diff(conn) -> list:  # noqa
    mc = MigrationContext.configure(conn)
    diff = compare_metadata(mc, Base.metadata)  # type:ignore[attr-defined]
    return diff


def same_index(a, b):  # noqa
    return (
        a.table.name == b.table.name
        and [c.name for c in a.columns] == [c.name for c in b.columns]
        and a.unique == b.unique
    )


async def print_changes() -> None:
    changes = defaultdict(list)
    sessionmanager.init()
    assert sessionmanager._engine is not None
    async with sessionmanager._engine.begin() as connection:
        assert connection is not None
        diff = await connection.run_sync(create_diff)

        remove_index = [d for d in diff if d[0] == "remove_index"]
        add_index = [d for d in diff if d[0] == "add_index"]

        for r in remove_index[:]:
            for a in add_index[:]:
                if same_index(r[1], a[1]):
                    remove_index.remove(r)
                    add_index.remove(a)
                    break

        other = [d for d in diff if d[0] not in ("remove_index", "add_index")]

        diff = other + remove_index + add_index

        for elem in diff:
            if isinstance(elem, list):
                for inner_elem in elem:
                    changes[inner_elem[0]].append(inner_elem)
            else:
                changes[elem[0]].append(elem)
    #    pprint.pprint(changes, indent=2, width=20)

    # translate dict entries to avoid confusion
    for k, v in translate_table.items():
        if k in changes:
            changes[v] = changes[k]
            del changes[k]

    for k, v in changes.items():
        print("=" * 30)
        print(k)
        print("=" * 30)
        pprint.pprint(v)
    for k, v in changes.items():
        print(k, len(v))


asyncio.run(print_changes())
