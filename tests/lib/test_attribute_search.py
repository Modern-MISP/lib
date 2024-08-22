import pytest
from icecream import ic
from sqlalchemy import select

from mmisp.db.models.attribute import Attribute
from mmisp.lib.attribute_search_filter import get_search_filters


@pytest.mark.asyncio
async def test_value_search(db, attribute):
    f = get_search_filters(value=attribute.value)
    q = select(Attribute).filter(f)
    ic(str(q))
    res = await db.execute(q)
    all_attributes = res.scalars().all()
    for x in all_attributes:
        ic(x.asdict())
    assert any(x.id == attribute.id for x in all_attributes)


@pytest.mark.asyncio
async def test_value_search_multi(db, attribute_multi):
    f = get_search_filters(value=attribute_multi.value)
    q = select(Attribute).filter(f)
    ic(str(q))
    res = await db.execute(q)
    all_attributes = res.scalars().all()
    for x in all_attributes:
        ic(x.asdict())
    assert any(x.id == attribute_multi.id for x in all_attributes)


@pytest.mark.asyncio
async def test_value_search_multi_value1(db, attribute_multi):
    f = get_search_filters(value1=attribute_multi.value1)
    q = select(Attribute).filter(f)
    ic(str(q))
    res = await db.execute(q)
    all_attributes = res.scalars().all()
    for x in all_attributes:
        ic(x.asdict())
    assert any(x.id == attribute_multi.id for x in all_attributes)


@pytest.mark.asyncio
async def test_value_search_multi_value2(db, attribute_multi):
    f = get_search_filters(value2=attribute_multi.value2)
    q = select(Attribute).filter(f)
    ic(str(q))
    res = await db.execute(q)
    all_attributes = res.scalars().all()
    for x in all_attributes:
        ic(x.asdict())
    assert any(x.id == attribute_multi.id for x in all_attributes)
