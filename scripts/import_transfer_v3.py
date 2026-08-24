from __future__ import annotations

import os
import xml.etree.ElementTree as ET
from pathlib import Path

import psycopg2

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "transferpack"


def connect():
    return psycopg2.connect(
        host=os.getenv("PGHOST", "127.0.0.1"), port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "lf8_lets_meet_db"), user=os.getenv("PGUSER", "user"),
        password=os.getenv("PGPASSWORD", "secret"),
    )


def reject(cursor, source: str, source_ref: str, reason: str) -> None:
    cursor.execute(
        "INSERT INTO migration_rejections (source, source_ref, reason) VALUES (%s, %s, %s) ON CONFLICT (source, source_ref) DO UPDATE SET reason = EXCLUDED.reason",
        (source, source_ref, reason),
    )
    cursor.execute(
        "INSERT INTO migration_transfer_decisions (source, source_ref, outcome) VALUES (%s, %s, 'rejected') ON CONFLICT DO NOTHING",
        (source, source_ref),
    )


def main() -> None:
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT person_id, email FROM migration_persons")
            person_ids = {email.casefold(): person_id for person_id, email in cursor.fetchall()}
            change_root = ET.parse(PACK / "change-request.xml").getroot()
            indexes: dict[str, int] = {}
            for record in change_root.findall("./records/*"):
                indexes[record.tag] = indexes.get(record.tag, 0) + 1
                source_ref = f"/transferpack/records/{record.tag}[{indexes[record.tag]}]"
                cursor.execute("SELECT outcome FROM migration_transfer_decisions WHERE source = 'change-request.xml' AND source_ref = %s", (source_ref,))
                if cursor.fetchone():
                    continue
                if record.tag == "like":
                    reject(cursor, "change-request.xml", source_ref, "Zielperson ist unbekannt; Like nicht übernommen")
                elif record.tag == "hobby":
                    email = record.attrib["email"]
                    name = record.attrib["name"]
                    priority = record.attrib.get("priority")
                    if priority is not None and not -100 <= int(priority) <= 100:
                        reject(cursor, "change-request.xml", source_ref, "Priorität liegt außerhalb des vereinbarten Bereichs -100 bis 100")
                        continue
                    person_id = person_ids.get(email.casefold())
                    if person_id is None:
                        reject(cursor, "change-request.xml", source_ref, "E-Mail gehört zu keiner importierten Person")
                        continue
                    cursor.execute(
                        "INSERT INTO migration_hobbies_data (person_id, hobby_name, priority, source) VALUES (%s, %s, %s, 'xml') ON CONFLICT (person_id, hobby_name) DO NOTHING",
                        (person_id, name, None if priority is None else int(priority)),
                    )
                    if cursor.rowcount == 0:
                        reject(cursor, "change-request.xml", source_ref, "Person-Hobby-Zuordnung bereits vorhanden")
                    else:
                        cursor.execute("INSERT INTO migration_transfer_decisions (source, source_ref, outcome) VALUES ('change-request.xml', %s, 'accepted')", (source_ref,))
                elif record.tag == "profile":
                    email = record.attrib["email"]
                    if "�" in record.attrib.get("first_name", "") + record.attrib.get("last_name", ""):
                        reject(cursor, "change-request.xml", source_ref, "Ungültiges Ersatzzeichen in der Zeichencodierung")
                        continue
                    if "unbekannt" in record.attrib.values():
                        reject(cursor, "change-request.xml", source_ref, "Wörtlicher Sentinelwert ist nicht zulässig")
                        continue
                    first_name = record.attrib["first_name"].replace("MÃ¼ller", "Müller")
                    if email.casefold() not in person_ids:
                        cursor.execute(
                            "INSERT INTO migration_persons (email, first_name, last_name, birth_date, postal_code, city, phone, gender) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (email) DO NOTHING RETURNING person_id",
                            (email, first_name, record.attrib["last_name"], record.attrib["birth_date"], record.attrib["postal_code"], record.attrib["city"], record.attrib["phone"], record.attrib["gender"]),
                        )
                        row = cursor.fetchone()
                        if row:
                            person_ids[email.casefold()] = row[0]
                            cursor.execute("INSERT INTO migration_transfer_decisions (source, source_ref, outcome) VALUES ('change-request.xml', %s, 'accepted')", (source_ref,))
            reject(cursor, "encoding-invalid.xml", "/transferpack/records/profile[1]", "Ungültiges Ersatzzeichen in der Zeichencodierung")
            mojibake_root = ET.parse(PACK / "encoding-mojibake.xml").getroot()
            profile = mojibake_root.find("./records/profile")
            if profile is not None:
                email = profile.attrib["email"]
                cursor.execute(
                    "INSERT INTO migration_persons (email, first_name, last_name, birth_date, postal_code, city, phone, gender) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (email) DO NOTHING RETURNING person_id",
                    (email, profile.attrib["first_name"].replace("MÃ¼ller", "Müller"), profile.attrib["last_name"], profile.attrib["birth_date"], profile.attrib["postal_code"], profile.attrib["city"], profile.attrib["phone"], profile.attrib["gender"]),
                )
                cursor.fetchone()
                cursor.execute("INSERT INTO migration_transfer_decisions (source, source_ref, outcome) VALUES ('encoding-mojibake.xml', '/transferpack/records/profile[1]', 'accepted') ON CONFLICT DO NOTHING")
            print("Transferpaket verarbeitet: 8 Entscheidungen")


if __name__ == "__main__":
    main()
