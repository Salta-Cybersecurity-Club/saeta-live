"""Persistencia en sqlite del histórico de posiciones."""

import logging
import sqlite3
from pathlib import Path

log = logging.getLogger("saeta.storage")

SCHEMA = """
CREATE TABLE IF NOT EXISTS posiciones (
    interno   TEXT NOT NULL,
    linea     TEXT NOT NULL,
    lat       REAL NOT NULL,
    lon       REAL NOT NULL,
    ts        TEXT NOT NULL,
    velocidad REAL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS ix_pos_ts ON posiciones(ts);
CREATE INDEX IF NOT EXISTS ix_pos_linea ON posiciones(linea, ts);
"""


class Storage:
    def __init__(self, path="saeta.sqlite3"):
        self.path = Path(path)
        self.db = sqlite3.connect(self.path)
        self.db.executescript(SCHEMA)

    def guardar(self, buses):
        cur = self.db.cursor()
        n = 0
        for b in buses:
            cur.execute(
                "INSERT INTO posiciones VALUES (?,?,?,?,?,?)",
                (b.interno, b.linea, b.lat, b.lon, b.ts.isoformat(), b.velocidad),
            )
            n += 1
        self.db.commit()
        return n

    def ultima_posicion(self, linea=None):
        q = "SELECT * FROM posiciones"
        args = ()
        if linea:
            q += " WHERE linea=?"
            args = (linea.upper(),)
        q += " ORDER BY ts DESC"
        return self.db.execute(q, args).fetchall()
