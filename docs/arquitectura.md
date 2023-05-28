# Arquitectura

```
endpoint SAETA -> scraper.py -> sqlite -> API / bot / export CSV
```

## Dependencias externas

- `noa-geo` — conversión POSGAR94/Gauss-Krüger en versiones antiguas.
- `python-telegram-bot` 13.15 — no migrar a v20 sin reescribir bot.py.
- `flask` — API.
