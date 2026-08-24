from __future__ import annotations

import os
import xml.etree.ElementTree as ET
from pathlib import Path

import psycopg2

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Lets_Meet_Hobbies.xml"


def connect():
    return psycopg2.connect(
        host=os.getenv("PGHOST", "127.0.0.1"), port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "lf8_lets_meet_db"), user=os.getenv("PGUSER", "user"),
        password=os.getenv("PGPASSWORD", "secret"),
    )


def read_xml() -> list[tuple[str, str, str]]:
    root = ET.parse(SOURCE).getroot()
    records = []
    for user in root.findall("user"):
        email = user.findtext("email")
        if not email:
            records.append(("xml", "user-without-email", "E-Mail fehlt"))
            continue
        hobbies = user.findall("./hobbies/hobby")
        for index, hobby in enumerate(hobbies, start=1):
            name = hobby.text or ""
            source_ref = f"{email}#hobby-{index}"
            if name == "":
                records.append(("xml", source_ref, "Hobbyname ist leer"))
            else:
                records.append((email.casefold(), name, source_ref))
    return records


def main() -> None:
    records = read_xml()
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT person_id, email FROM migration_persons")
            person_ids = {email.casefold(): person_id for person_id, email in cursor.fetchall()}
            for first, second, third in records:
                if first == "xml":
                    cursor.execute(
                        "INSERT INTO migration_rejections (source, source_ref, reason) VALUES (%s, %s, %s) ON CONFLICT (source, source_ref) DO UPDATE SET reason = EXCLUDED.reason",
                        (first, second, third),
                    )
                    continue
                email, hobby_name, source_ref = first, second, third
                person_id = person_ids.get(email)
                if person_id is None:
                    cursor.execute(
                        "INSERT INTO migration_rejections (source, source_ref, reason) VALUES (%s, %s, %s) ON CONFLICT (source, source_ref) DO UPDATE SET reason = EXCLUDED.reason",
                        ("xml", source_ref, "E-Mail gehört zu keiner importierten Person"),
                    )
                    continue
                cursor.execute(
                    """
                    INSERT INTO migration_hobbies_data (person_id, hobby_name, priority, source)
                    VALUES (%s, %s, NULL, 'xml')
                    ON CONFLICT (person_id, hobby_name) DO NOTHING
                    """,
                    (person_id, hobby_name),
                )
    print(f"XML-Import verarbeitet: {len(records)} Datensätze")


if __name__ == "__main__":
    main()
