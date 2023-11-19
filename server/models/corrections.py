from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Correction(Model):
    __keyspace__ = "aurae"
    device = columns.Text(primary_key=True, partition_key=True)
    reading_type = columns.Text(primary_key=True, partition_key=True)
    metric = columns.Text(primary_key=True)
    expression = columns.Text()
