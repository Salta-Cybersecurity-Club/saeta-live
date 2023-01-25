"""Bot de Telegram: /donde <linea> y /cuando <parada_id>.

python-telegram-bot 13.x (la v20 rompe todo, ya fue: quedamos en 13.15).
"""

import json
import logging
import os
from pathlib import Path

from telegram.ext import CommandHandler, Updater

from .geo import distancia_m
from .storage import Storage

log = logging.getLogger("saeta.bot")

PARADAS_FILE = Path(__file__).parent.parent / "data" / "paradas.json"


def _paradas():
    if PARADAS_FILE.exists():
        return json.loads(PARADAS_FILE.read_text(encoding="utf-8"))
    return []


def donde(update, context):
    if not context.args:
        update.message.reply_text("usá: /donde <linea> — ej: /donde 5A")
        return
    linea = context.args[0].upper()
    st = Storage()
    rows = st.ultimas_por_interno(linea)
    if not rows:
        update.message.reply_text("no tengo posiciones de la %s todavía" % linea)
        return
    msg = "línea %s — %d coches activos\n" % (linea, len(rows))
    for r in rows[:5]:
        msg += "  interno %s — %.5f, %.5f (%s)\n" % (r[0], r[2], r[3], r[4][:16])
    update.message.reply_text(msg)


def cuando(update, context):
    if not context.args:
        update.message.reply_text("usá: /cuando <parada_id> — ej: /cuando 2")
        return
    try:
        pid = int(context.args[0])
    except ValueError:
        update.message.reply_text("parada inválida")
        return
    parada = next((p for p in _paradas() if p["id"] == pid), None)
    if not parada:
        update.message.reply_text("no conozco la parada %d" % pid)
        return
    st = Storage()
    mejor = None
    for linea in parada["lineas"]:
        for r in st.ultimas_por_interno(linea):
            d = distancia_m(parada["lat"], parada["lon"], r[2], r[3])
            if mejor is None or d < mejor[0]:
                mejor = (d, r[0], linea)
    if not mejor:
        update.message.reply_text("sin coches activos cerca de %s" % parada["nombre"])
        return
    update.message.reply_text(
        "el coche más cercano a %s es el interno %s (línea %s) a ~%d m"
        % (parada["nombre"], mejor[1], mejor[2], mejor[0])
    )


def main():
    token = os.environ["TELEGRAM_TOKEN"]
    up = Updater(token)
    up.dispatcher.add_handler(CommandHandler("donde", donde))
    up.dispatcher.add_handler(CommandHandler("cuando", cuando))
    log.info("bot escuchando")
    up.start_polling()
    up.idle()
