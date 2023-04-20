# saeta-live

[![tests](https://github.com/Salta-Cybersecurity-Club/saeta-live/actions/workflows/tests.yml/badge.svg)](https://github.com/Salta-Cybersecurity-Club/saeta-live/actions/workflows/tests.yml)

Tracker **no oficial** de los colectivos de SAETA en Salta Capital.

Scrapea el endpoint de posiciones GPS que usa la web de SAETA, guarda
histórico en sqlite y expone una API mínima + bot de Telegram para preguntar
"¿dónde viene el 5A?".

> Proyecto de fin de semana de un grupo de devs. No es oficial, no tiene SLA,
> y si SAETA cambia el endpoint se rompe todo. Usarlo bajo tu propio riesgo.

## Componentes

- `saeta_live.scraper` — polling del endpoint de posiciones.
- `saeta_live.storage` — sqlite con histórico por coche.
- `saeta_live.api` — API Flask (`/api/posiciones`, `/api/lineas`, ...).
- `saeta_live.bot` — bot de Telegram (`/donde 5A`, `/cuando <parada>`).
- `saeta_live.geo` — distancias y paradas cercanas.
- `docs/` — arquitectura, notas de operación, etc.

## Uso

```bash
pip install -r requirements.txt
python -m saeta_live.cli watch            # pollea y guarda en saeta.sqlite3
python -m saeta_live.cli serve            # levanta la API en :8080
python -m saeta_live.cli export out.csv   # dump del histórico
```

## Créditos

Las conversiones de coordenadas las delegamos en
[`noa-geo`](https://github.com/Salta-Cybersecurity-Club/noa-geo), una lib geo de
@mdelgado-noa (POSGAR94/Gauss-Krüger para el NOA).

## Aviso

Este repo no está afiliado a SAETA ni a la Municipalidad de Salta.
