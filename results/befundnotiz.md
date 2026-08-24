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

### 24.08.2026 - Akt-2-Quellenvergleich und Entscheidungen

- MongoDB enthält 1.576 Nutzer, 430 Nutzer mit Likes und 270 Nutzer mit Nachrichten.
- Für V2 werden die Namen aus MongoDB übernommen. Dadurch werden sechs äußere Leerzeichen aus der Excel-Lieferung entsprechend der Kundinnenquelle entfernt.
- Bei `katharina.prommer@autluuk.kom` steht in Excel `Prommer, Katharina`, in MongoDB jedoch `Vogelsang, Katharina`. Für V2 gilt die MongoDB-Angabe als jüngerer Stammdatenstand.
- MongoDB-Telefonnummern, gerichtete Likes und gerichtete Nachrichten werden über die E-Mail-Adresse übernommen.
- Zeitstempel werden als Zeitwerte importiert; die Quelle verwendet sowohl `YYYY-MM-DD HH:MM:SS` als auch `DD.MM.YYYY HH:MM:SS`.
- Hobbys und Prioritäten stammen in V2 aus Excel und erhalten `source = 'excel'`. Der Interessenwert `mw` wird als zwei Sachverhalte (`m` und `w`) ausgegeben; die Codes selbst bleiben unverändert.
- Der V2-Checker meldet 50 verschiedene `conversation_id`; bei 48 IDs gibt es mehrere Teilnehmerpaare. Deshalb ist `conversation_id` keine eindeutige Nachrichten-ID, sondern gruppiert Nachrichten einer Unterhaltung. Der Wert bleibt als Attribut jeder Nachricht erhalten.
- Der V2-Checker meldet bei einer Person den Telefonwert `birgit.voss@gmaiil.ork`. Das ist ein auffälliger, wahrscheinlich fachlich falscher Quellwert, aber kein leerer Platzhalter. Er wird unverändert übernommen und als offene Rückfrage an die Kundin markiert; eine eigene Korrektur würde die Quelle verfälschen.
