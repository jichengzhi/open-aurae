from typing import Dict, Type

from entity import *

Payload = Dict[str, str | float | bool]
Columns = Dict[str, str | float | datetime | bool]
ReadingClass = Type[PTQSReading |
                    PMSReading |
                    ZigbeePowerReading |
                    ZigbeeTempReading |
                    ZigbeeContactReading |
                    ZigbeeOccupancyReading |
                    ZigbeeVibrationReading]
