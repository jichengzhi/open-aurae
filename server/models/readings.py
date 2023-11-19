from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Reading(Model):
    __keyspace__ = "aurae"
    __abstract__ = True

    device = columns.Text(primary_key=True, partition_key=True)
    date = columns.Date(primary_key=True, partition_key=True)
    processed = columns.Boolean(primary_key=True, partition_key=True)
    time = columns.DateTime(primary_key=True, clustering_order="DESC")
    reading_type = columns.Text(primary_key=True, discriminator_column=True)

    sensor_id = columns.Text()


class TrackableReading(Reading):
    __abstract__ = True

    ip_address = columns.Text()
    latitude = columns.Decimal()
    longitude = columns.Decimal()


class ZigbeeReading(Reading):
    __abstract__ = True

    battery = columns.Decimal()
    voltage = columns.Decimal()


class PTQSReading(TrackableReading):
    __discriminator_value__ = "ptqs1005"

    temperature = columns.Decimal()
    humidity = columns.Decimal()
    tvoc = columns.Decimal()
    pm25 = columns.Decimal()
    co2 = columns.Decimal()
    ch2o = columns.Decimal()


class PMSReading(TrackableReading):
    __discriminator_value__ = "pms5003st"

    temperature = columns.Decimal()
    humidity = columns.Decimal()
    pd05 = columns.Decimal()
    pd10 = columns.Decimal()
    pd25 = columns.Decimal()
    pd50 = columns.Decimal()
    pd100 = columns.Decimal()
    pd100g = columns.Decimal()
    pm1 = columns.Decimal()
    pm10 = columns.Decimal()
    pm25 = columns.Decimal()
    cf_pm1 = columns.Decimal()
    cf_pm10 = columns.Decimal()
    cf_pm25 = columns.Decimal()
    pmv10 = columns.Decimal()
    pmv25 = columns.Decimal()
    pmv100 = columns.Decimal()
    pmv_total = columns.Decimal()
    pmvtotal = columns.Decimal()
    ch2o = columns.Decimal()


class ZigbeeTempReading(ZigbeeReading):
    __discriminator_value__ = "zigbee_temp"

    temperature = columns.Decimal()
    humidity = columns.Decimal()


class ZigbeeOccupancyReading(ZigbeeReading):
    __discriminator_value__ = "zigbee_occupancy"

    occupancy = columns.Boolean()
    illuminance = columns.Decimal()


class ZigbeeContactReading(ZigbeeReading):
    __discriminator_value__ = "zigbee_contact"

    contact = columns.Boolean()


class ZigbeePowerReading(ZigbeeReading):
    __discriminator_value__ = "zigbee_power"

    state = columns.Text()
    power = columns.Decimal()
    consumption = columns.Decimal()
    temperature = columns.Decimal()


class ZigbeeVibrationReading(ZigbeeReading):
    __discriminator_value__ = "zigbee_vibration"

    angle = columns.Decimal()
    angle_x = columns.Decimal()
    angle_y = columns.Decimal()
    angle_z = columns.Decimal()
    angle_x_absolute = columns.Decimal()
    angle_y_absolute = columns.Decimal()
    action = columns.Text()
