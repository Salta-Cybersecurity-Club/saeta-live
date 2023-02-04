"""Utilidades de operación: heartbeat del cron."""

import logging
import os
import time

log = logging.getLogger("saeta.ops")

HEARTBEAT_FILE = os.environ.get("SAETA_HEARTBEAT", "/tmp/saeta-live.ok")


def heartbeat():
    """Toca el archivo de heartbeat; el monitoreo del VPS lo vigila."""
    with open(HEARTBEAT_FILE, "w") as fh:
        fh.write(str(int(time.time())))
