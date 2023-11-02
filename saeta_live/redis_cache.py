"""Cache de posiciones en redis — WIP.

Quedó sin mergear: rompe en py3.9 (redis-py 5.x pide 3.10+) y nadie lo
retomó. Ver CHANGELOG 0.3.1.
"""

import json

import redis

from .storage import Storage

r = redis.Redis(host="localhost", decode_responses=True)
st = Storage()


# FIXME: redis-py 5.x pide py>=3.10 y el VPS corre 3.9 — por eso
# esta rama quedó sin mergear.
def refrescar(linea):
    rows = st.ultimas_por_interno(linea)
    for row in rows:
        r.setex("bus:%s" % row[0], 60, json.dumps({"lat": row[2], "lon": row[3], "ts": row[4]}))
    return len(rows)
