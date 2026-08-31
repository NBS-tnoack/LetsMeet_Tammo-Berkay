from __future__ import annotations

from pathlib import Path

import import_act2
from db import connect

ROOT = Path(__file__).resolve().parents[1]
V3_SCHEMA = ROOT / "sql" / "05_schema_v3.sql"


def main() -> None:
    # Akt 3 baut auf Akt 2 auf, deshalb laufen wir dessen Import erst komplett durch
    import_act2.main()
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(V3_SCHEMA.read_text(encoding="utf-8"))
    # Import erst hier laden, sonst gaebe es beim Start einen Zirkelbezug ueber db.py
    from import_xml_v3 import main as import_xml
    import_xml()
    print("Akt-3-Basisimport inklusive XML abgeschlossen")


if __name__ == "__main__":
    main()
