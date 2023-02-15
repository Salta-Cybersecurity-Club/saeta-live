import pytest

from saeta_live.models import Bus
from tests.fixtures.api_responses import POSICIONES_V1, POSICIONES_V2


def test_bus_from_dict_v1():
    d = POSICIONES_V1["coches"][0]
    b = Bus.from_dict(d)
    assert b.interno == "204"
    assert b.linea == "5A"
    assert b.lat == pytest.approx(-24.7911)


def test_bus_from_dict_v2_gps_none():
    d = POSICIONES_V2["vehiculos"][1]
    b = Bus.from_dict(d)
    assert b.interno == "098"
    assert b.lat == pytest.approx(-24.7590)


def test_dedup_key():
    d = POSICIONES_V1["coches"][0]
    b1, b2 = Bus.from_dict(d), Bus.from_dict(dict(d))
    assert b1.key() == b2.key()
