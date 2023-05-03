"""Export del histórico a archivos tipo GTFS — WIP.

Idea: cruzar posiciones históricas con paradas para estimar frecuencias
reales por franja (SAETA no publica GTFS). Por ahora genera stops.txt
desde data/paradas.json.
"""

import csv
import json
from pathlib import Path

PARADAS = Path(__file__).parent.parent / "data" / "paradas.json"


def export_stops(out_dir):
    paradas = json.loads(PARADAS.read_text(encoding="utf-8"))
    with open(Path(out_dir) / "stops.txt", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["stop_id", "stop_name", "stop_lat", "stop_lon"])
        for p in paradas:
            w.writerow([p["id"], p["nombre"], p["lat"], p["lon"]])
    return len(paradas)
