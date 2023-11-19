from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Sensor(Model):
    __keyspace__ = "aurae"
    device = columns.Text(index=True)
    id = columns.Text(primary_key=True)
    type = columns.Text()
    name = columns.Text()
    comments = columns.Text()
    last_record = columns.DateTime()
