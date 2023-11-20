from datetime import datetime
from typing import Optional, Tuple

from models import readings
from models.meta import all_column_names
from mqtt import Columns, Payload, ReadingClass


def parse_topic(topic: str) -> Columns:
    match topic.split('/'):
        case ['zigbee', device, sensor_id, *_]:
            return {'device': device, 'sensor_id': sensor_id}
        case _:
            return {}


def parse_datetime(isodatetime: Optional[str]) -> datetime:
    if isodatetime is None:
        return datetime.now()
    else:
        return datetime.fromisoformat(isodatetime)


def parse_alias(msg_key: str) -> str:
    match msg_key:
        case 'tmp':
            return 'temperature'
        case 'rh':
            return 'humidity'
        case 'sensor':
            return 'sensor_id'
        case 'device_id':
            return 'device'
        case _:
            return msg_key


def reading_class(msg_payload: Payload) -> ReadingClass:
    match msg_payload:
        case {'sensor': 'ptqs1005'}:
            return readings.PTQSReading
        case {'sensor': 'pms5003st'}:
            return readings.PMSReading
        case {'power': _}:
            return readings.ZigbeePowerReading
        case {'tmp': _}:
            return readings.ZigbeeTempReading
        case {'contact': _}:
            return readings.ZigbeeContactReading
        case {'occupancy': _}:
            return readings.ZigbeeOccupancyReading
        case {'angle_x': _}:
            return readings.ZigbeeVibrationReading
        case _:
            raise ValueError('Cannot determine reading type from message payload')


def to_columns(msg_payload: Payload, reading_cls: ReadingClass) -> Columns:
    t = parse_datetime(msg_payload.get('time'))
    col_names = all_column_names(reading_cls)

    cols = {parse_alias(k.lower()): v for k, v in msg_payload.items()}
    cols = {k: v for k, v in cols.items() if k in col_names} | {'time': t, 'date': t.date(), 'processed': False}

    return cols


def parse_message(topic: str, payload: Payload) -> Tuple[ReadingClass, Columns]:
    payload |= parse_topic(topic)
    cls = reading_class(payload)
    return cls, to_columns(payload, cls)
