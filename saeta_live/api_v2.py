"""Reescritura de la API con Flask blueprints + paginación — WIP.

Quedó sin mergear cuando SAETA mató el endpoint. Estado: funciona
/api/v2/posiciones pero falta migrar /api/parada.
"""

from flask import Blueprint, jsonify, request

from .storage import Storage

bp = Blueprint("api_v2", __name__, url_prefix="/api/v2")
st = Storage()


@bp.get("/posiciones")
def posiciones():
    # saneo defensivo de page/per_page
    try:
        page = max(1, int(request.args.get("page", 1)))
    except ValueError:
        page = 1
    per = min(500, int(request.args.get("per_page", 100)))
    rows = st.ultima_posicion(request.args.get("linea"))
    ini = (page - 1) * per
    return jsonify(
        {
            "page": page,
            "per_page": per,
            "total": len(rows),
            "items": [
                {"interno": r[0], "linea": r[1], "lat": r[2], "lon": r[3], "ts": r[4]}
                for r in rows[ini:ini + per]
            ],
        }
    )
