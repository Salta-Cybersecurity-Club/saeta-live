"""Polling del endpoint de posiciones GPS de SAETA.

El endpoint es el mismo que usa la web pública de seguimiento. No tiene auth
pero rate-limitea fuerte si consultás seguido: usar intervalo >= 30s.
"""

import logging
import time

import requests

from .models import Bus

log = logging.getLogger("saeta.scraper")

ENDPOINT = "https://ws.saetasalta.com.ar/api/v1/posiciones"
TIMEOUT = 8


def fetch(linea=None, session=None):
    """Devuelve la lista de Bus activos (o [] si el endpoint falla)."""
    s = session or requests.Session()
    params = {"linea": linea} if linea else {}
    try:
        r = s.get(ENDPOINT, params=params, timeout=TIMEOUT)
        r.raise_for_status()
        # el endpoint a veces responde latin-1 aunque dice utf-8
        r.encoding = r.apparent_encoding
    except requests.RequestException as e:
        log.warning("endpoint caido: %s", e)
        return []
    payload = r.json()
    return [Bus.from_dict(c) for c in payload.get("coches", [])]


def watch(storage, interval=30, lineas=None):
    """Loop infinito: pollea y guarda posiciones."""
    log.info("watch iniciado, intervalo %ss", interval)
    while True:
        buses = fetch()
        n = storage.guardar(buses)
        log.debug("guardadas %d posiciones", n)
        time.sleep(interval)
