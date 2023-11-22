""" Convert scalars into JSON appropriate values. """
from typing import Optional
import dateutil.parser
from cassandra.util import Date
from datetime import datetime, date
from ariadne import ScalarType

datetime_scalar = ScalarType("DateTime")


@datetime_scalar.serializer
def serialize_datetime(value: datetime):
    return value.isoformat()


@datetime_scalar.value_parser
def parse_datetime_value(value: str) -> Optional[datetime]:
    # dateutil is provided by python-dateutil library
    if value:
        return dateutil.parser.parse(value)
    return None


@datetime_scalar.literal_parser
def parse_datetime_literal(ast):
    value = str(ast.value)
    return parse_datetime_value(value)  # reuse logic from parse_value


date_scalar = ScalarType("Date")


@date_scalar.serializer
def serialize_date(value: Date):
    return value.date().isoformat()


@date_scalar.value_parser
def parse_date_value(value: str) -> Optional[date]:
    # dateutil is provided by python-dateutil library
    if value:
        return dateutil.parser.parse(value).date()
    return None


@date_scalar.literal_parser
def parse_date_literal(ast):
    value = str(ast.value)
    return parse_date_value(value)  # reuse logic from parse_value
