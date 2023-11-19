from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.usertype import UserType


class BuildingLocation(UserType):
    __keyspace__ = "aurae"
    building_id = columns.UUID()
    floor = columns.Integer()
    room = columns.Text()
    map_x = columns.Decimal()
    map_y = columns.Decimal()


class Device(Model):
    __keyspace__ = "aurae"
    id = columns.Text(primary_key=True)
    name = columns.Text()
    latitude = columns.Decimal()
    longitude = columns.Decimal()
    building = columns.UserDefinedType(BuildingLocation)
    last_record = columns.DateTime()


class Building(Model):
    __keyspace__ = "aurae"
    id = columns.UUID(primary_key=True)
    name = columns.Text()
