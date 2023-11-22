import csv
import logging
import os
from datetime import datetime, timedelta
from io import StringIO

from ariadne import graphql
from dotenv import load_dotenv
from paho.mqtt.client import Client
from paho.mqtt.publish import single
from quart import Quart, request, jsonify, make_response

from entity import Reading
from helper import parse_iso_date_str
from models import database
from models.meta import all_reading_column_names
from mqtt.subscriber import make_client
from schema import schema

app = Quart(__name__)


@app.route('/ping')
async def ping():
    return 'pong'


@app.route('/graphql', methods=['POST'])
async def graphql_handler():
    data = await request.get_json()

    success, result = await graphql(schema, data, context_value={'request': request}, debug=app.debug)

    status_code = 200 if success else 400
    return jsonify(result), status_code


@app.route('/remove/<device>/<sensor>', methods=['DELETE'])
async def remove_sensor(sensor, device):
    host = os.getenv('MQTT_BROKER')
    single(f'zigbee/{device}/bridge/config/remove',
           payload=sensor, qos=1, hostname=host)

    return 'OK'


@app.route('/download/<device>', methods=['GET'])
async def download_device_readings(device):
    min_start = (datetime.today() - timedelta(weeks=16)).date()
    max_end = datetime.today().date()

    start_date = parse_iso_date_str(request.args.get('start'), min_start)
    end_date = parse_iso_date_str(request.args.get('end'), max_end)

    start_date = max(start_date, min_start)
    end_date = min(end_date, max_end)

    readings = database.get_device_readings(device, start_date, end_date)

    buffer = StringIO()

    writer = csv.DictWriter(buffer, fieldnames=list(all_reading_column_names(Reading)), extrasaction='ignore')

    writer.writeheader()

    for reading in readings:
        writer.writerow({k: v for k, v in reading.items()})

    filename = device.replace(":", "")

    response = await make_response(buffer.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename={filename}.csv"
    response.mimetype = "text/csv"
    return response


logging.basicConfig()
logging.root.setLevel(logging.INFO)

load_dotenv('.env')

database.connect_and_sync_tables()

broker_addr = os.environ['MQTT_BROKER']

plantower_client: Client = make_client(client_id='Aurae Server - Plantower', host=broker_addr,
                                       topic='air-quality/#')
zigbee_client: Client = make_client(client_id='Aurae Server - Zigbee', host=broker_addr, topic='zigbee/#')

plantower_client.loop_start()
zigbee_client.loop_start()
