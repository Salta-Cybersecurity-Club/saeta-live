# saeta-live

> ## ⚠️ SIN MANTENIMIENTO
> **ago-2024**: SAETA cambió la API (el endpoint viejo devuelve 403 desde
> marzo y definitivamente murió). Nadie tiene tiempo de
> reversear el nuevo, así que el repo queda como archivo histórico.
> Si querés retomarlo, abrí un issue o escribinos. — @tbarrios-salta

[![tests](https://github.com/Salta-Cybersecurity-Club/saeta-live/actions/workflows/tests.yml/badge.svg)](https://github.com/Salta-Cybersecurity-Club/saeta-live/actions/workflows/tests.yml)

Tracker **no oficial** de los colectivos de SAETA en Salta Capital.

Scrapea el endpoint de posiciones GPS que usa la web de SAETA, guarda
histórico en sqlite y expone una API mínima + bot de Telegram para preguntar
"¿dónde viene el 5A?".

## Componentes

- `saeta_live.scraper` — polling del endpoint de posiciones.
- `saeta_live.storage` — sqlite con histórico por coche.
- `saeta_live.api` — API Flask (`/api/posiciones`, `/api/lineas`, ...).
- `saeta_live.bot` — bot de Telegram (`/donde 5A`, `/cuando <parada>`).
- `saeta_live.geo` — distancias haversine y paradas cercanas.
- `docs/` — arquitectura, notas de operación, etc.

## Uso

```bash
pip install -r requirements.txt
python -m saeta_live.cli watch            # pollea y guarda en saeta.sqlite3
python -m saeta_live.cli serve            # levanta la API en :8080
python -m saeta_live.cli export out.csv   # dump del histórico
```

## Créditos

Las primeras versiones delegaban las conversiones en una librería del grupo.
Hoy la distancia se calcula inline con haversine en `saeta_live/geo.py`.

## Aviso

Este repo no está afiliado a SAETA ni a la Municipalidad de Salta.
