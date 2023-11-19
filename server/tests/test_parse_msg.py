import datetime
import unittest

from models.meta import all_column_names
from models.readings import *
from mqtt.parse import parse_topic, reading_class, to_columns, parse_message


class ParseTopicTest(unittest.TestCase):

    def test_empty_zigbee_topic(self):
        topic = 'zigbee'
        result = parse_topic(topic)

        self.assertEqual({}, result)

    def test_normal_zigbee_topic(self):
        topic = 'zigbee/dev/sens'
        result = parse_topic(topic)

        self.assertEqual(result, {'device': 'dev', 'sensor_id': 'sens'})

    def test_only_dev_zigbee_topic(self):
        topic = 'zigbee/dev'
        result = parse_topic(topic)

        self.assertEqual({}, result)

    def test_blank_device_zigbee_topic(self):
        topic = 'zigbee/'
        result = parse_topic(topic)

        self.assertEqual({}, result)

    def test_blank_sensor_zigbee_topic(self):
        topic = 'zigbee/dev/'
        result = parse_topic(topic)

        self.assertEqual({'device': 'dev', 'sensor_id': ''}, result)

    def test_redundant_zigbee_topic(self):
        topic = 'zigbee/dev/sens/foo/bar'
        result = parse_topic(topic)

        self.assertEqual({'device': 'dev', 'sensor_id': 'sens'}, result)

    def test_other_topic(self):
        topic = 'smart-home/bulb'
        result = parse_topic(topic)

        self.assertEqual({}, result)


class AllReadingColumnNamesTest(unittest.TestCase):
    reading_columns = {'date', 'device', 'processed', 'reading_type', 'time', 'sensor_id'}
    zigbee_columns = {'battery', 'voltage'}
    trackable_columns = {'ip_address', 'latitude', 'longitude'}

    def test_PTQSReading_columns(self):
        actual = all_column_names(PTQSReading)
        expected = {'temperature', 'humidity', 'tvoc', 'pm25', 'co2',
                    'ch2o'} | self.reading_columns | self.trackable_columns

        self.assertEqual(expected, actual)

    def test_PMSReading_columns(self):
        actual = all_column_names(PMSReading)
        expected = {'temperature', 'humidity', 'pd05', 'pd10', 'pd25', 'pd50', 'pd100', 'pd100g', 'pm1', 'pm10', 'pm25',
                    'cf_pm1', 'cf_pm10', 'cf_pm25', 'pmv10', 'pmv25', 'pmv100', 'pmv_total', 'pmvtotal',
                    'ch2o'} | self.reading_columns | self.trackable_columns

        self.assertEqual(expected, actual)

    def test_ZigbeeTempReading_columns(self):
        actual = all_column_names(ZigbeeTempReading)
        expected = {'temperature', 'humidity'} | self.reading_columns | self.zigbee_columns

        self.assertEqual(expected, actual)

    def test_ZigbeeOccupancyReading_columns(self):
        actual = all_column_names(ZigbeeOccupancyReading)
        expected = {'occupancy', 'illuminance'} | self.reading_columns | self.zigbee_columns

        self.assertEqual(expected, actual)

    def test_ZigbeeContactReading_columns(self):
        actual = all_column_names(ZigbeeContactReading)
        expected = {'contact'} | self.reading_columns | self.zigbee_columns

        self.assertEqual(expected, actual)

    def test_ZigbeePowerReading_columns(self):
        actual = all_column_names(ZigbeePowerReading)
        expected = {'state', 'power', 'consumption', 'temperature'} | self.reading_columns | self.zigbee_columns

        self.assertEqual(expected, actual)

    def test_ZigbeeVibrationReading_columns(self):
        actual = all_column_names(ZigbeeVibrationReading)
        expected = {'angle', 'angle_x', 'angle_y', 'angle_z', 'angle_x_absolute',
                    'angle_y_absolute', 'action'} | self.reading_columns | self.zigbee_columns

        self.assertEqual(expected, actual)


class ParseReadingClassTest(unittest.TestCase):

    def test_PTQSReading(self):
        payload = {
            'sensor': 'ptqs1005',
            'power': 23.5,
            'temperature': 22.2,
            'contact': True,
            'occupancy': False,
            'angle_x': 33.1
        }
        actual = reading_class(payload)
        self.assertEqual(PTQSReading, actual)

    def test_PMSReading(self):
        payload = {
            'sensor': 'pms5003st',
            'power': 23.5,
            'temperature': 22.2,
            'contact': True,
            'occupancy': False,
            'angle_x': 33.1
        }
        actual = reading_class(payload)
        self.assertEqual(PMSReading, actual)

    def test_ZigbeePowerReading(self):
        payload = {
            'sensor': 'foo',
            'power': 23.5,
            'temperature': 22.2,
            'contact': True,
            'occupancy': False,
            'angle_x': 33.1
        }
        actual = reading_class(payload)
        self.assertEqual(ZigbeePowerReading, actual)

    def test_ZigbeeTempReading(self):
        payload = {
            'sensor': 'foo',
            'temperature': 22.2,
            'contact': True,
            'occupancy': False,
            'angle_x': 33.1
        }
        actual = reading_class(payload)
        self.assertEqual(ZigbeeTempReading, actual)

    def test_ZigbeeContactReading(self):
        payload = {
            'sensor': 'foo',
            'contact': True,
            'occupancy': False,
            'angle_x': 33.1
        }
        actual = reading_class(payload)
        self.assertEqual(ZigbeeContactReading, actual)

    def test_ZigbeeOccupancyReading(self):
        payload = {
            'sensor': 'foo',
            'occupancy': False,
            'angle_x': 33.1
        }
        actual = reading_class(payload)
        self.assertEqual(ZigbeeOccupancyReading, actual)

    def test_ZigbeeVibrationReading(self):
        payload = {
            'sensor': 'foo',
            'angle_x': 33.1
        }
        actual = reading_class(payload)
        self.assertEqual(ZigbeeVibrationReading, actual)


class ToColumnsTest(unittest.TestCase):

    def test_temperature_alias(self):
        payload = {
            'TMP': 'foo'
        }

        cols = to_columns(payload, PTQSReading)

        self.assertFalse('TMP' in cols)
        self.assertTrue('temperature' in cols)
        self.assertEqual('foo', cols['temperature'])

    def test_humidity_alias(self):
        payload = {
            'RH': 'foo'
        }

        cols = to_columns(payload, PTQSReading)

        self.assertFalse('RH' in cols)
        self.assertTrue('humidity' in cols)
        self.assertEqual('foo', cols['humidity'])

    def test_sensor_alias(self):
        payload = {
            'SENSOR': 'foo'
        }

        cols = to_columns(payload, PTQSReading)

        self.assertFalse('SENSOR' in cols)
        self.assertTrue('sensor_id' in cols)
        self.assertEqual('foo', cols['sensor_id'])

    def test_device_alias(self):
        payload = {
            'DEVICE_ID': 'foo'
        }

        cols = to_columns(payload, PTQSReading)

        self.assertNotIn('DEVICE_ID', cols)
        self.assertIn('device', cols)
        self.assertEqual('foo', cols['device'])

    def test_isodatetime(self):
        payload = {
            'time': '2023-11-19T14:05:59Z'
        }

        cols = to_columns(payload, PTQSReading)

        self.assertEqual(datetime.date(2023, 11, 19), cols['date'])
        self.assertEqual(datetime.datetime(2023, 11, 19, 14, 5, 59, tzinfo=datetime.timezone.utc), cols['time'])

    def test_processed(self):
        payload = {}

        cols = to_columns(payload, PTQSReading)

        self.assertFalse(cols['processed'])

    def test_redundant_keys(self):
        payload = {
            'not_exist': '!!!'
        }

        cols = to_columns(payload, PTQSReading)

        self.assertNotIn('not_exist', cols)

    def test_PTQSReading(self):
        tmp = 1.2
        rh = 2.3
        co2 = 3.4
        ch2o = 4.5
        sensor = 'ptqs1005'
        device_id = 'dev'
        ip_address = '127.0.0.1'
        latitude = 45.1
        longitude = 56.8
        time = datetime.datetime.now()

        payload = {
            'not_exist': '!!!',
            'tmp': tmp,
            'rh': rh,
            'co2': co2,
            'ch2o': ch2o,
            'device_id': device_id,
            'sensor': sensor,
            'ip_address': ip_address,
            'latitude': latitude,
            'longitude': longitude,
            'time': time.isoformat()
        }

        cols = to_columns(payload, PTQSReading)

        expected = {
            'temperature': tmp,
            'humidity': rh,
            'co2': co2,
            'ch2o': ch2o,
            'device': device_id,
            'sensor_id': sensor,
            'ip_address': ip_address,
            'latitude': latitude,
            'longitude': longitude,
            'processed': False,
            'time': time,
            'date': time.date()
        }

        self.assertEqual(expected, cols)


class ParseMessageTest(unittest.TestCase):

    def test_PTQSReading(self):
        topic = 'foo'
        tmp = 1.2
        rh = 2.3
        co2 = 3.4
        ch2o = 4.5
        sensor = 'ptqs1005'
        device_id = 'dev'
        ip_address = '127.0.0.1'
        latitude = 45.1
        longitude = 56.8
        time = datetime.datetime.now()

        payload = {
            'not_exist': '!!!',
            'tmp': tmp,
            'rh': rh,
            'co2': co2,
            'ch2o': ch2o,
            'device_id': device_id,
            'sensor': sensor,
            'ip_address': ip_address,
            'latitude': latitude,
            'longitude': longitude,
            'time': time.isoformat()
        }

        expected = {
            'temperature': tmp,
            'humidity': rh,
            'co2': co2,
            'ch2o': ch2o,
            'device': device_id,
            'sensor_id': sensor,
            'ip_address': ip_address,
            'latitude': latitude,
            'longitude': longitude,
            'processed': False,
            'time': time,
            'date': time.date()
        }

        cls, cols = parse_message(topic, payload)

        self.assertEqual(PTQSReading, cls)
        self.assertEqual(expected, cols)

    def test_ZigbeeContactReading(self):
        topic = 'zigbee/dev/sensor'
        battery = 1.2
        voltage = 2.3
        contact = False
        time = datetime.datetime.now()

        payload = {
            'not_exist': '!!!',
            'battery': battery,
            'voltage': voltage,
            'contact': contact,
            'time': time.isoformat()
        }

        expected = {
            'contact': contact,
            'battery': battery,
            'voltage': voltage,
            'device': 'dev',
            'sensor_id': 'sensor',
            'processed': False,
            'time': time,
            'date': time.date()
        }

        cls, cols = parse_message(topic, payload)

        self.assertEqual(ZigbeeContactReading, cls)
        self.assertEqual(expected, cols)


if __name__ == '__main__':
    unittest.main()
