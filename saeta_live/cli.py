"""CLI de saeta-live.

    python -m saeta_live.cli watch [--intervalo 30]
"""

import argparse
import logging


def main(argv=None):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    p = argparse.ArgumentParser(prog="saeta-live")
    sub = p.add_subparsers(dest="cmd", required=True)

    w = sub.add_parser("watch", help="pollear posiciones y guardar")
    w.add_argument("--intervalo", type=int, default=30)
    w.add_argument("--db", default="saeta.sqlite3")

    args = p.parse_args(argv)

    from .scraper import watch
    from .storage import Storage

    watch(Storage(args.db), interval=args.intervalo)


if __name__ == "__main__":
    main()
