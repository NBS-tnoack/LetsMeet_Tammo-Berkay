from __future__ import annotations

from pathlib import Path

import psycopg2

import import_act2

ROOT = Path(__file__).resolve().parents[1]
V3_SCHEMA = ROOT / "sql" / "05_schema_v3.sql"


def main() -> None:
    import_act2.main()
    with import_act2.connect_postgres() as connection:
        with connection.cursor() as cursor:
            cursor.execute(V3_SCHEMA.read_text(encoding="utf-8"))
    from import_xml_v3 import main as import_xml
    import_xml()
    print("Akt-3-Basisimport inklusive XML abgeschlossen")


if __name__ == "__main__":
    main()
