import enum
from functools import partial


class SensorType(enum.IntEnum):
    Battery = 0
    Temperature = 1
    Humidity = 2


def fixed_point(divisor, data, signed=True):
    val = int.from_bytes(data, 'little', signed=signed)
    return val / divisor


def percent_formatter(data):
    return int.from_bytes(data, 'little', signed=False)


def format_sensor(tag, data):
    dispatch = {SensorType.Battery: percent_formatter,
                SensorType.Temperature: partial(fixed_point, 10),
                SensorType.Humidity: percent_formatter}
    return dispatch[tag](data)


__all__ = [SensorType, format_sensor]
