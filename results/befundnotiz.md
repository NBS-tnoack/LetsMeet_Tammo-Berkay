# Befundnotiz

## Akt 1

### 24.08.2026 - Beobachtungen zur Excel-Quelle

- Die Quelle `Lets Meet DB Dump.xlsx` enthält ein Tabellenblatt `Tabelle1`.
- Das Blatt enthält 1.576 Datenzeilen und eine Kopfzeile.
- `Nachname, Vorname` ist ein zusammengesetztes Feld.
- `Straße Nr, PLZ Ort` ist ein zusammengesetztes Adressfeld mit Straße/Hausnummer, Postleitzahl und Ort.
- Bei 1.573 Adressen kommen genau zwei Kommas vor. Drei Adressen enthalten ein weiteres Komma im Ortsnamen: `Demmin, Hansestadt`.
- Die Spalte für Hobbys enthält bis zu fünf Hobby-/Prioritätsangaben in einer Zelle.
- Die Hobbyangaben verwenden `%` als Begrenzung der Priorität, zum Beispiel `Hobby %78%`.
- Interessen stehen in der Spalte `Interessiert an`.
- Die Excel-Quelle ist für Akt 1 die maßgebliche Quelle. `Lets_Meet_Hobbies.xml` und MongoDB werden in Akt 1 noch nicht übernommen.

### Entscheidungen

- Die zusammengesetzten Felder werden beim Import anhand der im Auftrag vorgegebenen Regeln in einzelne Werte aufgeteilt.
- Das Adressfeld wird an den ersten beiden Kommas getrennt; alles nach dem zweiten Komma bleibt der vollständige Ortswert.
- Für V1 werden nur die Daten importiert, die für `migration_users` benötigt werden: E-Mail, Name, Geburtsdatum und die Bestandteile der Adresse.
- Hobby- und Interessendaten werden für V1 zunächst nicht in die Pflicht-View übernommen.
- Vor dem finalen Import prüfen wir E-Mail-Adressen auf Leerwerte und Eindeutigkeit.

### Nicht übernommen

- Hobby-, Interessen-, Telefon- und Geschlechtsdaten werden in Akt 1 nicht Teil der V1-View. Sie werden erst mit dem Datenvertrag V2 relevant.
- Die Nachlieferung `Lets_Meet_Hobbies.xml` wird in Akt 1 nicht verarbeitet.

### Schutzbedarf

- Namen, Adressen, Telefonnummern, E-Mail-Adressen und Geburtsdaten sind personenbezogene Daten und besonders sorgfältig zu behandeln.
- Die Quelldatei und Datenbankzugänge werden nicht öffentlich geteilt. Zugangsdaten werden nicht in Git versioniert.
