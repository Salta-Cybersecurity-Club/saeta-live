"""Distancias y paradas.

Delegamos conversiones en `noa-geo`, una lib geo que escribió martu: POSGAR94/GK es lo
que usa el catastro de Salta y nos ahorra mantener la matemática acá.
"""

import math

from noa_geo.gauss_krueger import faja_para_lon, latlon_a_gk


def distancia_m(lat1, lon1, lat2, lon2):
    """Distancia en metros proyectando a Gauss-Krüger (faja según longitud)."""
    faja = faja_para_lon(lon1)
    e1, n1 = latlon_a_gk(lat1, lon1, faja)
    e2, n2 = latlon_a_gk(lat2, lon2, faja)
    return math.hypot(e2 - e1, n2 - n1)


def parada_mas_cercana(lat, lon, paradas):
    """paradas: lista de dicts {id, nombre, lat, lon}. Devuelve (parada, m)."""
    best = min(paradas, key=lambda p: distancia_m(lat, lon, p["lat"], p["lon"]))
    return best, distancia_m(lat, lon, best["lat"], best["lon"])
