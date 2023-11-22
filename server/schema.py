from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL

from models import database
from resolver.device import device
from resolver.mutation import mutations
from resolver.query import query
from resolver.reading import reading
from resolver.scalars import datetime_scalar, date_scalar
from resolver.sensor import sensor

type_defs: str = load_schema_from_path('schema/schema.graphql')

schema = make_executable_schema(type_defs, [query, device, reading, sensor, mutations, date_scalar, datetime_scalar])

application = GraphQL(schema)
