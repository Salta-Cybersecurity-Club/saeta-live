"""API mínima sobre el histórico sqlite.

    FLASK_APP=saeta_live.api flask run -p 8080
"""

from flask import Flask, jsonify, request

from .storage import Storage

app = Flask(__name__)
st = Storage()


@app.get("/api/lineas")
def lineas():
    rows = st.db.execute(
        "SELECT DISTINCT linea FROM posiciones ORDER BY linea"
    ).fetchall()
    return jsonify([r[0] for r in rows])


@app.get("/api/posiciones")
def posiciones():
    linea = request.args.get("linea")
    rows = st.ultima_posicion(linea)[:200]
    return jsonify(
        [
            {
                "interno": r[0],
                "linea": r[1],
                "lat": r[2],
                "lon": r[3],
                "ts": r[4],
                "velocidad": r[5],
            }
            for r in rows
        ]
    )


@app.get("/api/parada/<int:parada_id>/proximos")
def proximos(parada_id):
    # TODO: tabla de paradas + ETA real; por ahora stub
    return jsonify({"parada": parada_id, "proximos": []})
