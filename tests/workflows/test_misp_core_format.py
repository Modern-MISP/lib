from typing import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from mmisp.db.models.attribute import Attribute
from mmisp.db.models.event import Event
from mmisp.db.models.organisation import Organisation
from mmisp.db.models.sighting import Sighting
from mmisp.workflows.misp_core_format import attribute_to_misp_core_format, event_after_save_new_to_core_format


@pytest.mark.asyncio
async def test_attribute_normalize(db: AsyncSession, attribute: Attribute) -> None:
    result = await attribute_to_misp_core_format(db, attribute)

    assert result["Event"]["Attribute"][0]["id"] == "23"
    assert result["Event"]["id"] == "1"
    assert len(result["Event"]["Attribute"][0]["Sighting"]) == 2
    assert result["Event"]["Attribute"][0]["value"] == "1abcdefghijkl"

    assert result["Event"]["Attribute"][0]["Sighting"][0]["id"] == 23
    assert result["Event"]["Attribute"][0]["Sighting"][0]["Organisation"]["name"] == "Bar"
    assert result["Event"]["Attribute"][0]["Sighting"][1]["id"] == 24
    assert result["Event"]["Attribute"][0]["Sighting"][1]["Organisation"]["name"] == "Foo"


@pytest.mark.asyncio
async def test_attribute_normalize_no_sightings(db: AsyncSession, attribute: Attribute) -> None:
    result = await attribute_to_misp_core_format(db, attribute, with_sightings=False)

    assert result["Event"]["Attribute"][0]["id"] == "23"
    assert result["Event"]["id"] == "1"
    assert "Sighting" not in result["Event"]["Attribute"][0]


@pytest.mark.asyncio
async def test_event_after_save(db: AsyncSession, event: Event) -> None:
    result = await event_after_save_new_to_core_format(db, event)

    assert result["Event"]["id"] == "1"
    assert result["Event"]["User"]["email"] == "admin@admin.test"


@pytest_asyncio.fixture
async def attribute(db: AsyncSession, event: Event) -> AsyncGenerator[Attribute, None]:
    orgc = Organisation(
        id=2,
        name="Bar",
        uuid="14f9be37-fc01-47bc-acd9-d7241c8b1941",
        description="Blub",
        type="broke",
        nationality="swiss",
        sector="foo",
        contacts="",
        landingpage="",
    )
    db.add(orgc)
    attr = Attribute(
        id=23,
        uuid="4a041cf7-f53f-4dcc-a354-ae64715e5eaa",
        event_id=event.id,
        object_id=0,
        object_relation=None,
        category="Financial fraud",
        type="btc",
        value1="1abcdefghijkl",
        value2="",
        to_ids=False,
        timestamp=1721131511,
        sharing_group_id=0,
        distribution=5,
        comment="",
        deleted=False,
        disable_correlation=False,
        first_seen=None,
        last_seen=None,
    )
    db.add(attr)
    sighting = Sighting(
        id=23,
        uuid="7de0a199-ed84-4a78-ba6c-2eeddd044965",
        attribute_id=23,
        event_id=event.id,
        org_id=2,
        date_sighting=1717943390,
        source="",
        type=0,
    )
    db.add(sighting)
    sighting2 = Sighting(
        id=24,
        uuid="1253d195-99e0-465d-a14f-92f26ff83432",
        attribute_id=23,
        event_id=event.id,
        org_id=1,
        date_sighting=1717943391,
        source="",
        type=0,
    )
    db.add(sighting2)
    yield attr
    await db.delete(orgc)
    await db.delete(sighting2)
    await db.delete(sighting)
    await db.delete(attr)
    await db.commit()
