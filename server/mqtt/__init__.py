from datetime import datetime
from typing import Dict, Type

from models.readings import Reading

Payload = Dict[str, str | float | bool]
Columns = Dict[str, str | float | datetime | bool]
ReadingClass = Type[Reading]
