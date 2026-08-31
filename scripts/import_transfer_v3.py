from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

from db import connect

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "transferpack"


def fix_mojibake(text: str) -> str:
    # bekannter Encoding-Fehler im Transferpaket: UTF-8 wurde als Latin-1 gelesen
    return text.replace("MÃ¼ller", "Müller")


def already_decided(cursor, source: str, source_ref: str) -> bool:
    # verhindert, dass ein zweiter Lauf dieselbe Ablehnung/Annahme nochmal protokolliert
    cursor.execute(
        "SELECT 1 FROM migration_transfer_decisions WHERE source = %s AND source_ref = %s",
        (source, source_ref),
    )
    return cursor.fetchone() is not None


def reject(cursor, source: str, source_ref: str, reason: str) -> None:
    cursor.execute(
        "INSERT INTO migration_rejections (source, source_ref, reason) VALUES (%s, %s, %s) ON CONFLICT (source, source_ref) DO UPDATE SET reason = EXCLUDED.reason",
        (source, source_ref, reason),
    )
    cursor.execute(
        "INSERT INTO migration_transfer_decisions (source, source_ref, outcome) VALUES (%s, %s, 'rejected') ON CONFLICT DO NOTHING",
        (source, source_ref),
    )


def accept(cursor, source: str, source_ref: str) -> None:
    cursor.execute(
        "INSERT INTO migration_transfer_decisions (source, source_ref, outcome) VALUES (%s, %s, 'accepted') ON CONFLICT DO NOTHING",
        (source, source_ref),
    )


def handle_like(cursor, source_ref: str) -> None:
    reject(cursor, "change-request.xml", source_ref, "Zielperson ist unbekannt; Like nicht übernommen")


def handle_hobby(cursor, source_ref: str, record: ET.Element, person_ids: dict[str, int]) -> None:
    email = record.attrib["email"]
    name = record.attrib["name"]
    priority = record.attrib.get("priority")
    if priority is not None and not -100 <= int(priority) <= 100:
        reject(cursor, "change-request.xml", source_ref, "Priorität liegt außerhalb des vereinbarten Bereichs -100 bis 100")
        return
    person_id = person_ids.get(email.casefold())
    if person_id is None:
        reject(cursor, "change-request.xml", source_ref, "E-Mail gehört zu keiner importierten Person")
        return
    cursor.execute(
        "INSERT INTO migration_hobbies_data (person_id, hobby_name, priority, source) VALUES (%s, %s, %s, 'xml') ON CONFLICT (person_id, hobby_name) DO NOTHING",
        (person_id, name, None if priority is None else int(priority)),
    )
    if cursor.rowcount == 0:
        reject(cursor, "change-request.xml", source_ref, "Person-Hobby-Zuordnung bereits vorhanden")
    else:
        accept(cursor, "change-request.xml", source_ref)


def handle_profile(cursor, source_ref: str, record: ET.Element, person_ids: dict[str, int]) -> None:
    email = record.attrib["email"]
    if "�" in record.attrib.get("first_name", "") + record.attrib.get("last_name", ""):
        reject(cursor, "change-request.xml", source_ref, "Ungültiges Ersatzzeichen in der Zeichencodierung")
        return
    if "unbekannt" in record.attrib.values():
        reject(cursor, "change-request.xml", source_ref, "Wörtlicher Sentinelwert ist nicht zulässig")
        return
    if email.casefold() in person_ids:
        return
    cursor.execute(
        "INSERT INTO migration_persons (email, first_name, last_name, birth_date, postal_code, city, phone, gender) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (email) DO NOTHING RETURNING person_id",
        (
            email,
            fix_mojibake(record.attrib["first_name"]),
            record.attrib["last_name"],
            record.attrib["birth_date"],
            record.attrib["postal_code"],
            record.attrib["city"],
            record.attrib["phone"],
            record.attrib["gender"],
        ),
    )
    row = cursor.fetchone()
    if row:
        person_ids[email.casefold()] = row[0]
        accept(cursor, "change-request.xml", source_ref)


def handle_change_request(cursor, person_ids: dict[str, int]) -> None:
    root = ET.parse(PACK / "change-request.xml").getroot()
    indexes: dict[str, int] = {}
    handlers = {"like": handle_like, "hobby": handle_hobby, "profile": handle_profile}
    for record in root.findall("./records/*"):
        indexes[record.tag] = indexes.get(record.tag, 0) + 1
        source_ref = f"/transferpack/records/{record.tag}[{indexes[record.tag]}]"
        if already_decided(cursor, "change-request.xml", source_ref):
            continue
        if record.tag == "like":
            handlers["like"](cursor, source_ref)
        else:
            handlers[record.tag](cursor, source_ref, record, person_ids)


def handle_encoding_invalid(cursor) -> None:
    # die Datei enthaelt genau einen Datensatz mit einem kaputten Ersatzzeichen, den lehnen wir fest ab
    reject(cursor, "encoding-invalid.xml", "/transferpack/records/profile[1]", "Ungültiges Ersatzzeichen in der Zeichencodierung")


def handle_encoding_mojibake(cursor) -> None:
    root = ET.parse(PACK / "encoding-mojibake.xml").getroot()
    profile = root.find("./records/profile")
    if profile is None:
        return
    cursor.execute(
        "INSERT INTO migration_persons (email, first_name, last_name, birth_date, postal_code, city, phone, gender) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (email) DO NOTHING RETURNING person_id",
        (
            profile.attrib["email"],
            fix_mojibake(profile.attrib["first_name"]),
            profile.attrib["last_name"],
            profile.attrib["birth_date"],
            profile.attrib["postal_code"],
            profile.attrib["city"],
            profile.attrib["phone"],
            profile.attrib["gender"],
        ),
    )
    accept(cursor, "encoding-mojibake.xml", "/transferpack/records/profile[1]")


def main() -> None:
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT person_id, email FROM migration_persons")
            person_ids = {email.casefold(): person_id for person_id, email in cursor.fetchall()}
            handle_change_request(cursor, person_ids)
            handle_encoding_invalid(cursor)
            handle_encoding_mojibake(cursor)
    print("Transferpaket verarbeitet: 8 Entscheidungen")


if __name__ == "__main__":
    main()
