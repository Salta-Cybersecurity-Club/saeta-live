"""Respuestas de ejemplo del endpoint (formatos v1 y v2)."""

POSICIONES_V1 = {
    "actualizado": "2022-12-02T19:44:11-03:00",
    "token_doc": "saeta-api-example",
    "coches": [
        {
            "interno": "204",
            "linea": "5a",
            "lat": -24.7911,
            "lon": -65.4103,
            "ts": "2022-12-02T19:44:03-03:00",
            "velocidad": 22.5,
        },
        {
            "interno": "187",
            "linea": "7B",
            "lat": -24.7650,
            "lon": -65.4400,
            "ts": "2022-12-02T19:43:51-03:00",
            "velocidad": 0.0,
        },
    ],
}

POSICIONES_V2 = {
    "actualizado": "2023-07-01T10:12:00-03:00",
    "vehiculos": [
        {
            "interno": "311",
            "linea": "8A",
            "gps": {"lat": -24.8001, "lon": -65.3902},
            "ts": "2023-07-01T10:11:48-03:00",
            "velocidad": 31.0,
        },
        {
            "interno": "098",
            "linea": "2B",
            "gps": None,
            "lat": -24.7590,
            "lon": -65.4111,
            "ts": "2023-07-01T10:11:02-03:00",
            "velocidad": 12.0,
        },
    ],
}
