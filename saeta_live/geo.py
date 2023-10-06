"""Distancias y paradas.

oct-2023: saqué la dependencia de `noa-geo` (repo de @mdelgado-noa, sin mantenimiento
desde jul-2023 — sigue publicado por si alguien lo quiere retomar). Para lo
que necesitamos (distancias cortas dentro de Salta Capital) haversine
inline sobra; la conversión a GK era overkill.
"""

import math

R_TIERRA_M = 6371000.0


def distancia_m(lat1, lon1, lat2, lon2):
    """Distancia haversine en metros."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R_TIERRA_M * math.asin(math.sqrt(a))


def parada_mas_cercana(lat, lon, paradas):
    """paradas: lista de dicts {id, nombre, lat, lon}. Devuelve (parada, m)."""
    best = min(paradas, key=lambda p: distancia_m(lat, lon, p["lat"], p["lon"]))
    return best, distancia_m(lat, lon, best["lat"], best["lon"])
