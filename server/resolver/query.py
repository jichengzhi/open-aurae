import os
from dataclasses import dataclass
from datetime import date, timedelta
from enum import StrEnum
from typing import Optional, Set

import jwt
import numpy as np
from ariadne import QueryType
from graphql import GraphQLResolveInfo

from entity import ReadingType
from models import database

query = QueryType()


def included_dates(s: date, e: date):
    days = (e - s).days
    return [s + timedelta(days=i) for i in range(days + 1)]


@query.field("readings")
async def resolve_readings(
        _, __,
        device: str,
        start: date,
        processed: bool,
        end: Optional[date] = None,
        type: ReadingType = None,
        limit: Optional[int] = None,
):
    return database.get_readings(device, start, processed, end, type, limit)


@query.field("smoothedReadings")
async def resolve_smoothed(_, __, metric, start, end, device, processed, type):
    readings = database.get_readings(device, start, processed, end, type)

    if len(readings) == 0:
        return []

    y = np.array([float(getattr(x, metric)) for x in readings])

    window = 20
    smoothed = np.convolve(y, np.ones((window,)) / window, mode="valid")

    print(len(smoothed), len(readings))

    for idx, x in enumerate(readings):
        if idx >= len(smoothed):
            break
        setattr(x, metric, smoothed[idx])
    return readings


class Role(StrEnum):
    guest = 'guest'
    admin = 'admin'
    read_admin = 'read:admin'


@dataclass
class UserClaim:
    user_id: str
    permissions: Set[str]


def parse_bearer_token(token: Optional[str]) -> Optional[UserClaim]:
    if token is None or token == '':
        return None

    token_type = 'Bearer '
    token = token[len(token_type):]

    claim = jwt.decode(token, os.getenv("SECRET_KEY"),
                       audience="http://new.openaurae.org/api/",
                       options={"verify_signature": False})

    return UserClaim(user_id=claim['sub'], permissions=set(claim['permissions']))


def device_with_permission(device, editable):
    return {k: v for k, v in device.items()} | {'editable': editable}


@query.field("devices")
async def resolve_devices(_, info: GraphQLResolveInfo):
    request = info.context['request']

    user_claim = parse_bearer_token(request.headers.get("Authorization"))

    if user_claim is None:
        # TODO better to return []
        return [device_with_permission(dev, False) for dev in database.all_devices()]

    if Role.admin in user_claim.permissions:
        return [device_with_permission(dev, True) for dev in database.all_devices()]
    elif Role.read_admin in user_claim.permissions:
        user_device_ids = {dev.id for dev in database.get_devices_by_user_id(user_claim.user_id)}
        return [device_with_permission(dev, dev.id in user_device_ids) for dev in database.all_devices()]
    else:
        return [device_with_permission(dev, True)
                for dev in database.get_devices_by_user_id(user_claim.user_id)]


@query.field("device")
async def resolve_device(_, info: GraphQLResolveInfo, id: str):
    device = database.get_device_by_id(id)

    if device is None:
        return None

    request = info.context['request']

    user_claim = parse_bearer_token(request.headers.get("Authorization"))

    if user_claim is None:
        return device_with_permission(device, False)
    elif Role.admin in user_claim.permissions:
        return device_with_permission(device, True)
    else:
        user_device_ids = {dev.id for dev in database.get_devices_by_user_id(user_claim.user_id)}
        return device_with_permission(device, device.id in user_device_ids)


@query.field("readingTypes")
async def resolve_reading_types(*_):
    return [t.value for t in ReadingType]
