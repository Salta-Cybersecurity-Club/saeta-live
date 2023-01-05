"""Bot de Telegram: /donde <linea> y /cuando <parada_id>.

python-telegram-bot 13.x (la v20 rompe todo, ya fue: quedamos en 13.15).
"""

import logging
import os

from telegram.ext import CommandHandler, Updater

from .geo import distancia_m
from .storage import Storage

log = logging.getLogger("saeta.bot")

PARADAS = []  # se carga de data/paradas.json en main()


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


def main():
    token = os.environ["TELEGRAM_TOKEN"]
    up = Updater(token)
    up.dispatcher.add_handler(CommandHandler("donde", donde))
    log.info("bot escuchando")
    up.start_polling()
    up.idle()
