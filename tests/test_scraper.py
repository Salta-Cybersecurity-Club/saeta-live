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


def test_bus_from_dict_v2_gps_ok():
    d = POSICIONES_V2["vehiculos"][0]
    b = Bus.from_dict(d)
    assert b.lat == pytest.approx(-24.8001)


def test_dedup_key():
    d = POSICIONES_V1["coches"][0]
    b1, b2 = Bus.from_dict(d), Bus.from_dict(dict(d))
    assert b1.key() == b2.key()


def test_velocidad_coma_decimal():
    # abr-2024: el endpoint manda "31,0" con coma en fallback
    d = dict(POSICIONES_V2["vehiculos"][0])
    d["velocidad"] = "31,0"
    b = Bus.from_dict(d)
    assert b.velocidad == pytest.approx(31.0)


def test_geo_distancia_salta():
    from saeta_live.geo import distancia_m

    # plaza 9 de julio -> terminal de ómnibus, ~1.6 km en línea recta
    d = distancia_m(-24.7885, -65.4105, -24.7733, -65.4033)
    assert d == pytest.approx(2000, abs=900)
