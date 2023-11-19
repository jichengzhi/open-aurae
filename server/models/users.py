from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class User(Model):
    __keyspace__ = "aurae"
    id = columns.Text(primary_key=True)
    username = columns.Text()
    password = columns.Text()
    name = columns.Text()
    devices = columns.List(columns.Text())
