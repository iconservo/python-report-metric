import pytest

from report_metric.backends import direct


def test_pack_host():
    assert b"\x00\x00\x00\x0elocalhost\x00" == direct.pack(direct.TYPE_HOST, 'localhost')


def test_pack_interval():
    assert b"\x00\x07\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x05" == direct.pack(direct.TYPE_INTERVAL, 5)
