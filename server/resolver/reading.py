from ariadne import ObjectType

from models.readings import Reading

reading = ObjectType("Reading")


@reading.field("timeSeconds")
def resolve_timestamp(reading: Reading, _):
    return reading.time.timestamp()
