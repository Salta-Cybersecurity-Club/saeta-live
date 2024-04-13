"""Modelos internos."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Bus:
    interno: str      # número de coche interno de SAETA
    linea: str        # "5A", "7B", etc
    lat: float
    lon: float
    ts: datetime
    velocidad: float = 0.0  # km/h reportado por el GPS

    @classmethod
    def from_dict(cls, d):
        # v2 del endpoint: a veces manda "gps" anidado, a veces plano
        gps = d.get("gps") or d
        return cls(
            interno=str(d["interno"]),
            linea=str(d["linea"]).upper(),
            lat=float(gps["lat"]),
            lon=float(gps["lon"]),
            ts=datetime.fromisoformat(d["ts"].replace("Z", "+00:00")),
            # abr-2024: el endpoint empezó a mandar "31,0" con coma decimal
            # (locale es-AR) en los coches que caen a fallback — fix crash
            velocidad=float(str(d.get("velocidad", 0.0)).replace(",", ".")),
        )

    def key(self):
        """Clave de dedup: interno + timestamp redondeado al minuto."""
        return (self.interno, self.ts.replace(second=0, microsecond=0))
