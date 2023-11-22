import uuid
from dataclasses import dataclass, field
from datetime import datetime, date
from enum import StrEnum
from typing import List, Set


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


@dataclass
class Correction:
    device: str
    reading_type: str
    metric: str
    expression: str


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
class Reading:
    device: str
    date: date
    processed: bool
    time: datetime
    sensor_id: str
    reading_type: ReadingType = field(kw_only=True)


@dataclass
class TrackableReading(Reading):
    ip_address: str
    latitude: float
    longitude: float


@dataclass
class ZigbeeReading(Reading):
    battery: float
    voltage: float


@dataclass
class PTQSReading(TrackableReading):
    reading_type: str = field(kw_only=True, default=ReadingType.ptqs1005)
    temperature: float
    humidity: float
    tvoc: float
    pm25: float
    co2: float
    ch2o: float


@dataclass
class PMSReading(TrackableReading):
    reading_type: str = field(kw_only=True, default=ReadingType.pms5003st)
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


@dataclass
class ZigbeeTempReading(ZigbeeReading):
    reading_type: str = field(kw_only=True, default=ReadingType.zigbee_temp)

    temperature: float
    humidity: float


@dataclass
class ZigbeeOccupancyReading(ZigbeeReading):
    reading_type: str = field(kw_only=True, default=ReadingType.zigbee_occupancy)
    occupancy: bool
    illuminance: float


@dataclass
class ZigbeeContactReading(ZigbeeReading):
    reading_type: str = field(kw_only=True, default=ReadingType.zigbee_contact)
    contact: bool


@dataclass
class ZigbeePowerReading(ZigbeeReading):
    reading_type: str = field(kw_only=True, default=ReadingType.zigbee_power)

    state: str
    power: float
    consumption: float
    temperature: float


@dataclass
class ZigbeeVibrationReading(ZigbeeReading):
    reading_type: str = field(kw_only=True, default=ReadingType.zigbee_vibration)

    angle: float
    angle_x: float
    angle_y: float
    angle_z: float
    angle_x_absolute: float
    angle_y_absolute: float
    action: str
