from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

from db import connect

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Lets_Meet_Hobbies.xml"


def read_xml() -> tuple[list[tuple[str, str]], list[tuple[str, str, str]]]:
    # zwei Listen statt einer: Ablehnungen stehen schon fest, Hobbys erst nach dem Personen-Abgleich
    root = ET.parse(SOURCE).getroot()
    rejections: list[tuple[str, str]] = []
    hobby_records: list[tuple[str, str, str]] = []
    for user in root.findall("user"):
        email = user.findtext("email")
        if not email:
            rejections.append(("user-without-email", "E-Mail fehlt"))
            continue
        for index, hobby in enumerate(user.findall("./hobbies/hobby"), start=1):
            name = hobby.text or ""
            source_ref = f"{email}#hobby-{index}"
            if name == "":
                rejections.append((source_ref, "Hobbyname ist leer"))
            else:
                hobby_records.append((email.casefold(), name, source_ref))
    return rejections, hobby_records


def main() -> None:
    rejections, hobby_records = read_xml()
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT person_id, email FROM migration_persons")
            person_ids = {email.casefold(): person_id for person_id, email in cursor.fetchall()}

            for source_ref, reason in rejections:
                cursor.execute(
                    "INSERT INTO migration_rejections (source, source_ref, reason) VALUES ('xml', %s, %s) ON CONFLICT (source, source_ref) DO UPDATE SET reason = EXCLUDED.reason",
                    (source_ref, reason),
                )

            for email, hobby_name, source_ref in hobby_records:
                person_id = person_ids.get(email)
                if person_id is None:
                    cursor.execute(
                        "INSERT INTO migration_rejections (source, source_ref, reason) VALUES ('xml', %s, %s) ON CONFLICT (source, source_ref) DO UPDATE SET reason = EXCLUDED.reason",
                        (source_ref, "E-Mail gehört zu keiner importierten Person"),
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
    print(f"XML-Import verarbeitet: {len(rejections) + len(hobby_records)} Datensätze")


if __name__ == "__main__":
    main()
