from entity import *
from helper import parse_iso_datetime_str
from models.meta import all_reading_column_names
from mqtt import Columns, Payload, ReadingClass


def parse_topic(topic: str) -> Columns:
    match topic.split('/'):
        case ['zigbee', device, sensor_id, *_]:
            return {'device': device, 'sensor_id': sensor_id}
        case _:
            return {}


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
            return PTQSReading
        case {'sensor': 'pms5003st'}:
            return PMSReading
        case {'power': _}:
            return ZigbeePowerReading
        case {'tmp': _}:
            return ZigbeeTempReading
        case {'contact': _}:
            return ZigbeeContactReading
        case {'occupancy': _}:
            return ZigbeeOccupancyReading
        case {'angle_x': _}:
            return ZigbeeVibrationReading
        case _:
            raise ValueError('Cannot determine reading type from message payload')


reading_types = {
    PTQSReading: ReadingType.ptqs1005,
    PMSReading: ReadingType.pms5003st,
    ZigbeePowerReading: ReadingType.zigbee_power,
    ZigbeeTempReading: ReadingType.zigbee_temp,
    ZigbeeContactReading: ReadingType.zigbee_contact,
    ZigbeeOccupancyReading: ReadingType.zigbee_occupancy,
    ZigbeeVibrationReading: ReadingType.zigbee_vibration,
}


def to_columns(msg_payload: Payload, reading_cls: ReadingClass) -> Columns:
    time = parse_iso_datetime_str(msg_payload.get('time'), datetime.now())
    col_names = all_reading_column_names(reading_cls)

    cols = {parse_alias(k.lower()): v for k, v in msg_payload.items()}
    cols = {k: v for k, v in cols.items() if k in col_names} | {'time': time, 'date': time.date(), 'processed': False,
                                                                'reading_type': reading_types[reading_cls].value}

    return cols


def parse_message(topic: str, payload: Payload) -> Columns:
    payload |= parse_topic(topic)
    cls = reading_class(payload)
    return to_columns(payload, cls)
