import time

import pytest

from report_metric.backends import direct


def test_pack_host():
    assert b"\x00\x00\x00\x0elocalhost\x00" == direct.pack(direct.TYPE_HOST, 'localhost')


def test_pack_interval():
    assert b"\x00\x07\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x05" == direct.pack(direct.TYPE_INTERVAL, 5)


def test_pack_time():
    the_time = 1502320335.64  # will get converted to int, cutting off the .64
    result = direct.pack(direct.TYPE_TIME, the_time)
    assert b"\x00\x01\x00\x0c\x00\x00\x00\x00Y\x8b\x96\xcf" == result
