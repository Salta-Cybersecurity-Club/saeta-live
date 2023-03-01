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
    velocidad REAL DEFAULT 0,
    UNIQUE(interno, ts)
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
        """Inserta posiciones, deduplicando por (interno, minuto)."""
        cur = self.db.cursor()
        n = 0
        for b in buses:
            try:
                cur.execute(
                    "INSERT INTO posiciones VALUES (?,?,?,?,?,?)",
                    (b.interno, b.linea, b.lat, b.lon, b.ts.isoformat(), b.velocidad),
                )
                n += 1
            except sqlite3.IntegrityError:
                pass  # duplicado exacto, lo salteamos
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

    def ultimas_por_interno(self, linea):
        """Última posición conocida de cada coche de una línea."""
        return self.db.execute(
            """
            SELECT p.* FROM posiciones p
            JOIN (SELECT interno, MAX(ts) ts FROM posiciones
                  WHERE linea=? GROUP BY interno) u
              ON p.interno=u.interno AND p.ts=u.ts
            """,
            (linea.upper(),),
        ).fetchall()
