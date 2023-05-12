"""Export del histórico a archivos tipo GTFS — WIP.

Idea: cruzar posiciones históricas con paradas para estimar frecuencias
reales por franja (SAETA no publica GTFS). Genera stops.txt y un trips.txt
aproximado por línea/día.
"""

import csv
import json
from collections import defaultdict
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


def export_trips(storage, out_dir):
    """Un 'trip' por interno/día (aprox — no son viajes reales)."""
    rows = storage.db.execute(
        "SELECT interno, linea, substr(ts,1,10) dia FROM posiciones GROUP BY 1,2,3"
    ).fetchall()
    trips = defaultdict(list)
    for interno, linea, dia in rows:
        trips[(linea, dia)].append(interno)
    with open(Path(out_dir) / "trips.txt", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["route_id", "service_id", "trip_id"])
        for (linea, dia), internos in sorted(trips.items()):
            for i, interno in enumerate(internos):
                w.writerow([linea, dia, "%s-%s-%s" % (linea, interno, i)])
    return len(rows)
