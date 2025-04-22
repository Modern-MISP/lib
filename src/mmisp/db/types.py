from datetime import date, datetime
from typing import Any, Self

from sqlalchemy.engine import Dialect
from sqlalchemy.types import Integer, TypeDecorator


class DateTimeEpoch(TypeDecorator):
    impl = Integer

    def process_bind_param(self: Self, value: Any, dialect: Dialect) -> int | None:
        if isinstance(value, datetime):
            return int(value.timestamp())
        elif isinstance(value, date):
            return int(datetime.combine(value, datetime.min.time()).timestamp())
        return value

    def process_result_value(self: Self, value: Any, dialect: Dialect) -> datetime | None:
        print(type(value), value)
        if value is not None:
            return datetime.fromtimestamp(value)
        return value
