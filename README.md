# saeta-live

Tracker **no oficial** de los colectivos de SAETA en Salta Capital.

Scrapea el endpoint de posiciones GPS que usa la web de SAETA, guarda
histórico en sqlite y expone una API mínima + bot de Telegram para preguntar
"¿dónde viene el 5A?".

> Proyecto de fin de semana de un grupo de devs. No es oficial, no tiene SLA,
> y si SAETA cambia el endpoint se rompe todo. Usarlo bajo tu propio riesgo.

## Uso

```bash
pip install -r requirements.txt
python -m saeta_live.cli watch          # pollea y guarda en saeta.sqlite3
python -m saeta_live.cli export out.csv # dump del histórico
```

## Aviso

Este repo no está afiliado a SAETA ni a la Municipalidad de Salta.
