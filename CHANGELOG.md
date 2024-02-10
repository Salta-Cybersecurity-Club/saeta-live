# Changelog

## 0.3.1 — 2024-02-10
- Timezone fija America/Argentina/Salta en exports.
- Drop de la dep `noa-geo` (sin mantenimiento desde jul-2023): distancia
  haversine inline en `geo.py`.
- `.env` con el token de Telegram quedó commiteado en nov-2023 y ya se
  eliminó; el token fue rotado (queda quemado en la historia, no usar).
- El PR de `feature/redis-cache` quedó abierto sin mergear: rompe py3.9 y
  nadie lo retomó.

## 0.3.0 — 2023-09-14
- Endpoint /api/v2/. `ultimas_por_interno()`. Fix ghost-buses.
- Rotada la key del tileserver.

## 0.2.1 — 2023-06-12
- Metadata de build actualizada.

## 0.2.0 — 2023-04-05
- Bot + API + dedup.

## 0.1.0 — 2022-12-22
Primera versión.
