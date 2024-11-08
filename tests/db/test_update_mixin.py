import pytest
from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from mmisp.api_schemas.galaxy_clusters import AddUpdateGalaxyElement
from mmisp.db.models.galaxy_cluster import GalaxyCluster, GalaxyElement
from mmisp.lib.galaxy_clusters import update_galaxy_cluster_elements


@pytest.mark.asyncio
async def test_galaxy_cluster_put(db, test_galaxy):
    galaxy_cluster = test_galaxy["galaxy_cluster"]
    qry = (
        select(GalaxyCluster)
        .filter(GalaxyCluster.id == galaxy_cluster.id)
        .options(selectinload(GalaxyCluster.galaxy_elements))
        .execution_options(populate_existing=True)
    )
    await db.execute(qry)

    gc_dict = galaxy_cluster.asdict()
    assert gc_dict["uuid"] == galaxy_cluster.uuid

    new_gc = gc_dict.copy()
    new_gc["value"] = f"{galaxy_cluster.value} extended"
    galaxy_cluster.put(**new_gc)

    assert galaxy_cluster.value == new_gc["value"]
    assert galaxy_cluster.value == f"{gc_dict['value']} extended"
    assert len(galaxy_cluster.galaxy_elements) == 2


@pytest.mark.asyncio
async def test_galaxy_cluster_patch(test_galaxy):
    galaxy_cluster = test_galaxy["galaxy_cluster"]

    gc_dict = galaxy_cluster.asdict()
    assert gc_dict["uuid"] == galaxy_cluster.uuid

    galaxy_cluster.patch(value=f"{gc_dict['value']} extended")

    assert galaxy_cluster.value == f"{gc_dict['value']} extended"
    assert galaxy_cluster.tag_name == gc_dict["tag_name"]

    galaxy_cluster.patch(authors=["new author"])
    assert galaxy_cluster.authors == ["new author"]


@pytest.mark.asyncio
async def test_galaxy_cluster_element_relationship(db, test_galaxy):
    galaxy_cluster = test_galaxy["galaxy_cluster"]
    qry = (
        select(GalaxyCluster)
        .filter(GalaxyCluster.id == galaxy_cluster.id)
        .options(selectinload(GalaxyCluster.galaxy_elements))
        .execution_options(populate_existing=True)
    )
    await db.execute(qry)
    new = [
        AddUpdateGalaxyElement(id=1, key="refs", value="http://test-one-one-one.example.com"),
        AddUpdateGalaxyElement(key="refs", value="http://test-new.example.com"),
    ]
    await update_galaxy_cluster_elements(db, galaxy_cluster, new)

    await db.commit()

    await db.execute(qry)
    assert len(galaxy_cluster.galaxy_elements) == 2
    for ge in galaxy_cluster.galaxy_elements:
        if ge.id == 1:
            assert ge.value == "http://test-one-one-one.example.com"
        else:
            assert ge.value == "http://test-new.example.com"

    await db.execute(delete(GalaxyElement).filter(GalaxyElement.galaxy_cluster_id == galaxy_cluster.id))
