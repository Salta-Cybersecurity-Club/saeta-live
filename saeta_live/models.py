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
        return cls(
            interno=str(d["interno"]),
            linea=str(d["linea"]).upper(),
            lat=float(d["lat"]),
            lon=float(d["lon"]),
            ts=datetime.fromisoformat(d["ts"].replace("Z", "+00:00")),
            velocidad=float(d.get("velocidad", 0.0)),
        )

    def key(self):
        """Clave de dedup: interno + timestamp redondeado al minuto."""
        return (self.interno, self.ts.replace(second=0, microsecond=0))
