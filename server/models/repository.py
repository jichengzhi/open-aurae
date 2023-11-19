from typing import List

from models.corrections import Correction
from models.devices import Device


def get_reading_corrections(device: str, reading_type: str) -> List[Correction]:
    return Correction.objects.filter(device=device, reading_type=reading_type).all()


def get_device_by_id(device_id: str) -> Device:
    return Device.get(id=device_id)
