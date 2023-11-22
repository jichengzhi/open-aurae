from typing import Dict, Any

from ariadne import ObjectType

from entity import ReadingType
from models import database
from models.readings import Reading

device = ObjectType("Device")


@device.field("lastReading")
async def resolve_last_reading(device: Dict[str, Any], _, processed=True, readingTypes=None):
    if device.get('last_record', None) is None:
        return None

    reading_types = ReadingType.all() if readingTypes is None else readingTypes

    readings = list(Reading.objects.filter(device=device['id'],
                                           date=device['last_record'].date(),
                                           time=device['last_record'],
                                           processed=processed,
                                           reading_type__in=reading_types))

    if len(readings) > 0:
        return max(readings, key=lambda reading: reading.time)
    else:
        return None


@device.field("sensors")
def resolve_sensors(device: Dict[str, Any], _):
    result = database.get_sensors_by_device_id(device['id'])

    print(result)

    return result
