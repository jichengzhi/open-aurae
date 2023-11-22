from enum import StrEnum

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Reading(Model):
    __keyspace__ = "aurae"

    device = columns.Text(primary_key=True, partition_key=True)
    date = columns.Date(primary_key=True, partition_key=True)
    processed = columns.Boolean(primary_key=True, partition_key=True)
    time = columns.DateTime(primary_key=True, clustering_order="DESC")
    reading_type = columns.Text(primary_key=True)

    sensor_id = columns.Text()

    ip_address = columns.Text()
    latitude = columns.Decimal()
    longitude = columns.Decimal()

    battery = columns.Decimal()
    voltage = columns.Decimal()

    temperature = columns.Decimal()
    humidity = columns.Decimal()
    tvoc = columns.Decimal()
    co2 = columns.Decimal()

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
    occupancy = columns.Boolean()
    illuminance = columns.Decimal()
    contact = columns.Boolean()
    state = columns.Text()
    power = columns.Decimal()
    consumption = columns.Decimal()
    angle = columns.Decimal()
    angle_x = columns.Decimal()
    angle_y = columns.Decimal()
    angle_z = columns.Decimal()
    angle_x_absolute = columns.Decimal()
    angle_y_absolute = columns.Decimal()
    action = columns.Text()
