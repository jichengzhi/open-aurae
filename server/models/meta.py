from functools import lru_cache
from typing import Type, Set

from models.readings import Reading


@lru_cache
def all_column_names(reading_cls: Type[Reading]) -> Set[str]:
    def is_field(name: str):
        return not callable(getattr(reading_cls, name))

    def is_public(name: str):
        return not name.startswith('_')

    return {name for name in dir(reading_cls) if is_public(name) and is_field(name) and name != 'pk'}
