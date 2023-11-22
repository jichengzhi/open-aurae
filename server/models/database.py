from datetime import date
from typing import List, Optional, Dict, Any

from cassandra.cqlengine import connection
from cassandra.cqlengine.connection import execute
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.query import DoesNotExist

from entity import ReadingType
from models.corrections import Correction
from models.devices import Device
from models.readings import Reading
from models.sensors import Sensor
from models.users import User


def connect_and_sync_tables(cassandra_seed='127.0.0.1'):
    connection.setup([cassandra_seed], "aurae")
    sync_table(Reading)
    sync_table(Device)
    sync_table(Sensor)
    sync_table(User)
    sync_table(Correction)


def create_reading(reading_cols: Dict[str, Any]) -> Reading:
    return Reading.create(**reading_cols)


def get_readings(device: str,
                 start: date,
                 processed: bool,
                 end: Optional[date] = None,
                 reading_type: ReadingType = None,
                 limit: Optional[int] = None):
    if end is None:
        end = date.today()

    # TODO build index on date and reading_type
    q = Reading.objects.filter(device=device, date__gte=start, date__lte=end, processed=processed).allow_filtering()

    if type is not None:
        q = q.filter(reading_type=type)

    q = q.all()

    if limit is not None:
        q = q.limit(limit)

    result = list(q)

    # TODO let cassandra do the sorting
    result.sort(key=lambda reading: reading.time)

    return result


def get_devices_by_user_id(user_id: str):
    try:
        user = User.objects.get(id=user_id)
        return list(Device.objects.filter(id__in=user.devices))
    except DoesNotExist:
        return []


def all_devices():
    return list(Device.objects.all())


def get_reading_corrections(device: str, reading_type: str) -> List[Correction]:
    return Correction.objects.filter(device=device, reading_type=reading_type).all()


def get_device_by_id(device_id: str) -> Optional[Device]:
    try:
        return Device.get(id=device_id)
    except DoesNotExist:
        return None


def get_sensor_by_id(sensor_id: str) -> Optional[Sensor]:
    try:
        return Sensor.get(id=sensor_id)
    except DoesNotExist:
        return None


def get_sensors_by_device_id(device_id: str):
    return list(Sensor.objects.filter(device=device_id))


def delete_sensors_by_device_id(device_id: str):
    sensors = Sensor.objects(device=device_id).all()
    for sensor in sensors:
        sensor.delete()


def get_device_readings(device_id: str, start_date: date, end_date: date):
    pks = execute('SELECT DISTINCT device, date, processed from aurae.reading where device=%s allow filtering;',
                  [device_id])

    pks = [k for k in pks if start_date <= k['date'].date() <= end_date]

    readings = []

    for k in pks:
        readings += Reading.objects.filter(device=k['device'], date=k['date'], processed=k['processed']).all()

    return readings
