import json
import logging
from json import JSONDecodeError
from logging import Logger
from typing import List, Optional

from paho.mqtt.client import MQTTMessage, Client
from sympy import sympify

from models.corrections import Correction
from models.database import create_reading, get_reading_corrections
from models.devices import Device
from models.readings import Reading
from models.sensors import Sensor
from mqtt import Columns, Payload
from mqtt.parse import parse_message


def calc_metric(correction: Correction, cols: Columns) -> float:
    # TODO substitute null?
    formula = sympify(correction.expression)
    return float(formula.subs(cols.items()).evalf())


def calc_metrics(corrections: List[Correction], cols: Columns) -> Columns:
    metrics = {correction.metric: calc_metric(correction, cols) for correction in corrections}
    return cols | metrics | {'processed': True}


def deserialize_json(json_str: str) -> Optional[Payload]:
    try:
        return json.loads(json_str)
    except JSONDecodeError:
        return None


def handle_reading_message(client: Client, logger: Logger, message: MQTTMessage) -> None:
    payload: Payload = deserialize_json(message.payload)

    if payload is None:
        logger.error('[Reading] payload is not JSON: %s', message.payload)
        return

    cols = parse_message(message.topic, payload)

    logger.info('[Reading] received reading %s', cols)

    reading: Reading = create_reading(cols)

    corrections: List[Correction] = get_reading_corrections(device=reading.device, reading_type=reading.reading_type)
    cols = calc_metrics(corrections, cols)

    create_reading(cols)

    logger.info(
        '[Reading] insert raw and processed records {"reading_type":"%s","topic":"%s","device":"%s","time":"%s"}',
        reading.reading_type, message.topic, reading.device, reading.time)

    Device(id=reading.device).if_exists().update(last_record=reading.time)

    Sensor(id=reading.sensor_id).if_exists().update(last_record=reading.time)


def make_client(client_id: str, topic: str, host='127.0.0.1', port=1883) -> Client:
    client = Client(client_id, False)

    client.on_message = handle_reading_message
    client.connect(host, port)
    client.subscribe(topic)
    client.user_data_set(logging.getLogger(client_id))

    return client
