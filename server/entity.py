import uuid
from dataclasses import dataclass
from datetime import datetime, date
from enum import StrEnum
from typing import List, Set, Literal

from pydantic import BaseModel


@dataclass
class User:
    id: str
    username: str
    password: str
    name: str
    devices: List[str]


@dataclass
class Sensor:
    device: str
    id: str
    type: str
    name: str
    comments: str
    last_record: datetime


@dataclass
class BuildingLocation:
    building_id: uuid.UUID
    floor: int
    room: str
    map_x: float
    map_y: float


@dataclass
class Device:
    id: str
    name: str
    latitude: float
    longitude: float
    building: BuildingLocation
    last_record: datetime


class ReadingType(StrEnum):
    ptqs1005 = 'ptqs1005'
    pms5003st = 'pms5003st'
    zigbee_temp = 'zigbee_temp'
    zigbee_occupancy = 'zigbee_occupancy'
    zigbee_contact = 'zigbee_contact'
    zigbee_vibration = 'zigbee_vibration'
    zigbee_power = 'zigbee_power'

    @staticmethod
    def all() -> Set[str]:
        return {enum.value for enum in ReadingType}


@dataclass
class Correction:
    device: str
    reading_type: ReadingType
    metric: str
    expression: str


class Reading(BaseModel):
    device: str
    date: date
    processed: bool
    time: datetime
    sensor_id: str
    reading_type: ReadingType


class TrackableReading(Reading):
    ip_address: str
    latitude: float
    longitude: float


class ZigbeeReading(Reading):
    battery: float
    voltage: float


class PTQSReading(TrackableReading):
    reading_type: Literal[ReadingType.ptqs1005]
    temperature: float
    humidity: float
    tvoc: float
    pm25: float
    co2: float
    ch2o: float


class PMSReading(TrackableReading):
    reading_type: Literal[ReadingType.pms5003st]
    temperature: float
    humidity: float
    pd05: float
    pd10: float
    pd25: float
    pd50: float
    pd100: float
    pd100g: float
    pm1: float
    pm10: float
    pm25: float
    cf_pm1: float
    cf_pm10: float
    cf_pm25: float
    pmv10: float
    pmv25: float
    pmv100: float
    pmv_total: float
    pmvtotal: float
    ch2o: float


class ZigbeeTempReading(ZigbeeReading):
    reading_type: Literal[ReadingType.zigbee_temp]

    temperature: float
    humidity: float


class ZigbeeOccupancyReading(ZigbeeReading):
    reading_type: Literal[ReadingType.zigbee_occupancy]
    occupancy: bool
    illuminance: float


class ZigbeeContactReading(ZigbeeReading):
    reading_type: Literal[ReadingType.zigbee_contact]
    contact: bool


class ZigbeePowerReading(ZigbeeReading):
    reading_type: Literal[ReadingType.zigbee_power]

    state: str
    power: float
    consumption: float
    temperature: float


class ZigbeeVibrationReading(ZigbeeReading):
    reading_type: Literal[ReadingType.zigbee_vibration]

    angle: float
    angle_x: float
    angle_y: float
    angle_z: float
    angle_x_absolute: float
    angle_y_absolute: float
    action: str


if __name__ == '__main__':
    class Foo(BaseModel):
        name: str | None
        age: int | None


    foo = Foo.model_validate_json('{"name": "bar", "age": null}')

    print(foo)
