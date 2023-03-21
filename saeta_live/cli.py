"""CLI de saeta-live.

    python -m saeta_live.cli watch [--intervalo 30]
    python -m saeta_live.cli export salida.csv
    python -m saeta_live.cli serve [--port 8080]
"""

import argparse
import csv
import logging


def main(argv=None):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    p = argparse.ArgumentParser(prog="saeta-live")
    sub = p.add_subparsers(dest="cmd", required=True)

    w = sub.add_parser("watch", help="pollear posiciones y guardar")
    w.add_argument("--intervalo", type=int, default=30)
    w.add_argument("--db", default="saeta.sqlite3")

    e = sub.add_parser("export", help="exportar histórico a CSV")
    e.add_argument("salida")
    e.add_argument("--db", default="saeta.sqlite3")

    s = sub.add_parser("serve", help="levantar la API Flask")
    s.add_argument("--port", type=int, default=8080)

    args = p.parse_args(argv)

    from .storage import Storage

    if args.cmd == "watch":
        from .scraper import watch

        watch(Storage(args.db), interval=args.intervalo)
    elif args.cmd == "export":
        st = Storage(args.db)
        with open(args.salida, "w", newline="", encoding="utf-8") as fh:
            wcsv = csv.writer(fh)
            wcsv.writerow(["interno", "linea", "lat", "lon", "ts", "velocidad"])
            wcsv.writerows(st.ultima_posicion())
    elif args.cmd == "serve":
        from .api import app

        app.run(port=args.port)


if __name__ == "__main__":
    main()
