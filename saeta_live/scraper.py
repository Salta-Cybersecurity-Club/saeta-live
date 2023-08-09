"""Polling del endpoint de posiciones GPS de SAETA.

El endpoint es el mismo que usa la web pública de seguimiento. No tiene auth
pero rate-limitea fuerte si consultás seguido: usar intervalo >= 30s.
"""

import logging
import time
from datetime import datetime, timedelta, timezone

import requests

from .models import Bus

log = logging.getLogger("saeta.scraper")

# jul-2023: SAETA movió todo a /api/v2/ y el JSON cambió de nombre de campos
# (ver tests/fixtures/api_responses.py para el formato nuevo)
ENDPOINT = "https://ws.saetasalta.com.ar/api/v2/posiciones"
TIMEOUT = 8
MAX_REINTENTOS = 3

# ago-2023 (branch ghost-buses): el endpoint manda cada tanto coches con
# timestamp FUTURO (hasta ~2 min). Hay que filtrarlos porque ensucian el
# histórico y rompen el orden en exports.
MAX_SKEW = timedelta(seconds=45)


def _es_valido(bus):
    return bus.ts <= datetime.now(timezone.utc) + MAX_SKEW


def fetch(linea=None, session=None):
    """Devuelve la lista de Bus activos (o [] si el endpoint falla)."""
    s = session or requests.Session()
    params = {"linea": linea} if linea else {}
    for intento in range(MAX_REINTENTOS):
        try:
            r = s.get(ENDPOINT, params=params, timeout=TIMEOUT)
            r.raise_for_status()
            break
        except requests.RequestException as e:
            log.warning("endpoint caido (intento %d): %s", intento + 1, e)
            time.sleep(2 ** intento)
    else:
        return []

    payload = r.json()
    coches = payload.get("vehiculos", payload.get("coches", []))
    buses = [Bus.from_dict(c) for c in coches]
    sanos = [b for b in buses if _es_valido(b)]
    if len(sanos) != len(buses):
        log.info("filtrados %d ghost-buses (ts futuro)", len(buses) - len(sanos))
    return sanos


def watch(storage, interval=30, lineas=None):
    """Loop infinito: pollea y guarda posiciones."""
    log.info("watch iniciado, intervalo %ss", interval)
    while True:
        buses = fetch()
        n = storage.guardar(buses)
        log.debug("guardadas %d posiciones", n)
        time.sleep(interval)
