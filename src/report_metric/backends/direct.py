import socket
import struct
import time

# flake8: noqa

SEND_INTERVAL = 10      # seconds
MAX_PACKET_SIZE = 1024  # bytes

TYPE_NAME = "gauge"

TYPE_HOST            = 0x0000
TYPE_TIME            = 0x0001
TYPE_PLUGIN          = 0x0002
TYPE_PLUGIN_INSTANCE = 0x0003
TYPE_TYPE            = 0x0004
TYPE_TYPE_INSTANCE   = 0x0005
TYPE_VALUES          = 0x0006
TYPE_INTERVAL        = 0x0007
LONG_INT_CODES = [TYPE_TIME, TYPE_INTERVAL]
STRING_CODES = [TYPE_HOST, TYPE_PLUGIN, TYPE_PLUGIN_INSTANCE, TYPE_TYPE, TYPE_TYPE_INSTANCE]

VALUE_COUNTER  = 0
VALUE_GAUGE    = 1
VALUE_DERIVE   = 2
VALUE_ABSOLUTE = 3
VALUE_CODES = {
    VALUE_COUNTER:  "!Q",
    VALUE_GAUGE:    "<d",
    VALUE_DERIVE:   "!q",
    VALUE_ABSOLUTE: "!Q"
}


def pack_numeric(type_code, number):
    return struct.pack("!HHq", type_code, 12, int(number))


def pack_string(type_code, string):
    return struct.pack("!HH", type_code, 5 + len(string)) + string.encode('UTF-8') + b"\0"


def pack(typeId, value):
    if typeId in LONG_INT_CODES:
        return pack_numeric(typeId, value)
    elif typeId in STRING_CODES:
        return pack_string(typeId, value)
    else:
        raise AssertionError("invalid type code " + str(id))


def pack_counters(counters):
        length = 6 + len(counters)*9
        result = []
        result.append(struct.pack("!HHH", TYPE_VALUES, length, len(counters)))
        for value in counters:
            result.append(struct.pack("<B", VALUE_GAUGE)) # this code allow to send only gauge value
        for value in counters:
            result.append(struct.pack("<d", value))
        return result


def message_start(when=None, host=socket.gethostname(), plugin_inst="", plugin_name="any", value_type=TYPE_NAME):
    return b"".join([
        pack(TYPE_HOST, host),
        pack(TYPE_TIME, when or time.time()),
        pack(TYPE_PLUGIN, plugin_name),
        pack(TYPE_PLUGIN_INSTANCE, plugin_inst),
        pack(TYPE_TYPE, value_type),
        pack(TYPE_TYPE, value_type),
        pack(TYPE_INTERVAL, SEND_INTERVAL)
    ])


# https://habrahabr.ru/post/139053/
# usage: create_message([working_set_value, peak_working_set_value], plugin_name='service_name', type_name='process_memory')
def create_message(counters, when=None, host=socket.gethostname(), plugin_inst="", plugin_name="any", type_name=TYPE_NAME):
    message = [message_start(when, host, plugin_inst, plugin_name, type_name)]
    parts = pack_counters(counters)
    message.extend(parts)
    return b"".join(message)


def send_stat(name, number, prefix=""):
    message = create_message([number], plugin_name=prefix, plugin_inst=name)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message, ("localhost", 25826))
        sock.close()
    except (socket.error, RuntimeError):
        # Swallow the error, it's only metrics
        pass
