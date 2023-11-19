import logging
import os

from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from dotenv import dotenv_values
from paho.mqtt.client import Client

from models import readings
from models.corrections import Correction
from models.devices import Device
from models.sensors import Sensor
from models.users import User
from mqtt.subscriber import make_client


def prepare_db(cassandra_seed='127.0.0.1'):
    connection.setup([cassandra_seed], "aurae")
    sync_table(readings.PTQSReading)
    sync_table(readings.PMSReading)
    sync_table(readings.ZigbeePowerReading)
    sync_table(readings.ZigbeeContactReading)
    sync_table(readings.ZigbeeVibrationReading)
    sync_table(readings.ZigbeeTempReading)
    sync_table(readings.ZigbeeOccupancyReading)
    sync_table(Device)
    sync_table(Sensor)
    sync_table(User)
    sync_table(Correction)


if __name__ == '__main__':
    logging.basicConfig()
    logging.root.setLevel(logging.INFO)

    # suppress warning
    os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'

    config = {
        **dotenv_values(".env"),  # load shared development variables
        **dotenv_values(".env.shared"),  # load shared development variables
        **dotenv_values(".env.secret"),  # load sensitive variables
        **os.environ,  # override loaded values with environment variables
    }

    broker_addr = config['MQTT_BROKER']

    prepare_db()

    plantower_client: Client = make_client(client_id='Aurae Server - Plantower', host=broker_addr,
                                           topic='air-quality/#')
    zigbee_client: Client = make_client(client_id='Aurae Server - Zigbee', host=broker_addr, topic='zigbee/#')

    plantower_client.loop_start()
    zigbee_client.loop_start()

    input('Block!\n')

    plantower_client.loop_stop()
    zigbee_client.loop_stop()
