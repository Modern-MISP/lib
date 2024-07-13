from calendar import timegm
from time import gmtime
from sqlalchemy.ext.asyncio import AsyncSession
from mmisp.db.database import Session
from mmisp.db.models.event import Event

async def publish_event(db: AsyncSession, event_id: str) -> bool:
    event = await db.get(Event, event_id)

    if not event:
        return False

    setattr(event, "published", True)
    setattr(event, "publish_timestamp", timegm(gmtime()))

    await db.commit()
    await db.refresh(event)

    return True