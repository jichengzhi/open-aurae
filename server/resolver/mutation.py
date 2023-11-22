import uuid
from typing import Dict, Any

from ariadne import MutationType

from models import database
from models.devices import Device
from models.sensors import Sensor
from models.users import User

mutations = MutationType()


@mutations.field("createUser")
def resolve_create_user(_, __, id: str, devices):
    user = User.create(id=id, devices=devices)
    return user


@mutations.field("createReading")
def resolve_create_reading(_, __, data: Dict[str, Any]):
    reading = database.create_reading(**data)
    return reading


def _upsert_sensor(device: str, data: Dict[str, Any]):
    if "id" not in data:
        data["id"] = str(uuid.uuid4())
    data["device"] = device
    return Sensor.create(**data)


@mutations.field("upsertDevice")
def resolve_upsert_device(_, __, data: Dict[str, Any]):
    if "sensors" in data:
        database.delete_sensors_by_device_id(data['device'])

        for sensor in data["sensors"]:
            _upsert_sensor(data["id"], sensor)

        del data["sensors"]

    existing: Device = Device.filter(id=data['id']).first()

    if existing is not None:
        new = {}
        d = existing._as_dict()
        del d['last_record']
        new.update(d)
        new.update(data)
        data = new

    device = Device.create(**data)
    return device


@mutations.field("deleteDevice")
def resolve_delete_device(_, __, id: str):
    device = database.get_device_by_id(id)

    if device is not None:
        device.delete()
