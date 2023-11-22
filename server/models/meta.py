from dataclasses import fields
from functools import lru_cache
from typing import Type, Set

from entity import Reading


@lru_cache
def all_reading_column_names(reading_cls: Type[Reading]) -> Set[str]:
    return {field.name for field in fields(reading_cls)}
