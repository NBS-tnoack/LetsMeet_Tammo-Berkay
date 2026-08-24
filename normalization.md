# **Normalisierung: 1. bis 3. Normalform**

Normalisierung heißt: Tabellen so aufteilen, dass jede Tabelle genau ein Thema beschreibt und
kein Wert doppelt gepflegt werden muss. Die Normalformen bauen aufeinander auf — die 2. Normalform
setzt die 1. voraus, die 3. setzt die 2. voraus.

**Wenn ihr nur einen Satz mitnehmt, dann diesen:**

> Jede Spalte beschreibt **direkt** das, was der Primärschlüssel beschreibt, und nichts anderes.
> Jede Zelle enthält genau **einen einzelnen Wert**.

Alles Weitere unten ist die genaue Ausformulierung davon — zum Nachschlagen, wenn ein konkreter
Fall unklar ist.

**Grundlage vorweg:** Jede Zeile einer Tabelle wird durch einen **Primärschlüssel** eindeutig
identifiziert. Er kann aus einer Spalte bestehen oder aus mehreren — dann heißt er
**zusammengesetzter Primärschlüssel**. Alle Spalten, die nicht zum Primärschlüssel gehören,
heißen **Nicht-Schlüssel-Spalten**.

---

## **1. Normalform (1NF) — Atomarität**

**Regel:** Jede Zelle enthält genau **einen einzelnen Wert** — keine Listen, keine Kombinationen.

### Verstoß

| Artikelnummer | Lagerbestand | Farben             |
|---------------|--------------|--------------------|
| A001          | 50           | rot, blau, grün    |

**Problem:** Die Spalte „Farben“ enthält mehrere Werte in einer Zelle. Man kann nicht nach einer
einzelnen Farbe filtern, ohne im Text zu suchen.

**Lösung:** Die Mehrfachwerte kommen in eine eigene Tabelle, eine Zeile je Wert.

**Artikel:**

| Artikelnummer | Lagerbestand |
|---------------|--------------|
| A001          | 50           |

**Artikelfarben:**

| Artikelnummer | Farbe  |
|---------------|--------|
| A001          | rot    |
| A001          | blau   |
| A001          | grün   |

---

## **2. Normalform (2NF) — Abhängigkeit vom vollständigen Schlüssel**

**Regel:** Die Tabelle ist in 1NF, **und** jede Nicht-Schlüssel-Spalte hängt vom **gesamten**
Primärschlüssel ab — nicht nur von einem Teil davon.

Diese Regel wird erst bei einem **zusammengesetzten** Primärschlüssel interessant. Bei einem
Primärschlüssel aus einer einzigen Spalte ist sie automatisch erfüllt.

### Verstoß

**Bestellposition** — Primärschlüssel ist die Kombination (Bestellnummer, Artikelnummer):

| Bestellnummer | Artikelnummer | Menge | Artikelbezeichnung |
|---------------|---------------|-------|--------------------|
| 123           | A001          | 3     | Schraube M4        |
| 123           | A002          | 1     | Mutter M4          |
| 124           | A001          | 7     | Schraube M4        |

**Problem:** „Menge“ hängt tatsächlich von beidem ab — welcher Artikel in welcher Bestellung.
„Artikelbezeichnung“ hängt dagegen **nur von der Artikelnummer** ab, also nur von einem Teil des
Schlüssels. Folge: „Schraube M4“ steht mehrfach in der Tabelle und muss bei einer Umbenennung
überall gleichzeitig geändert werden.

**Lösung:** Die Spalte, die nur von einem Schlüsselteil abhängt, wandert in die Tabelle dieses
Schlüsselteils.

**Bestellposition:**

| Bestellnummer | Artikelnummer | Menge |
|---------------|---------------|-------|
| 123           | A001          | 3     |
| 123           | A002          | 1     |
| 124           | A001          | 7     |

**Artikel:**

| Artikelnummer | Artikelbezeichnung |
|---------------|--------------------|
| A001          | Schraube M4        |
| A002          | Mutter M4          |

**Merke:** „Menge“ bleibt in der Bestellposition, weil sie wirklich zur Verbindung der beiden
gehört. Eine solche Spalte heißt **Beziehungsattribut** — sie beschreibt nicht eine der beiden
Seiten, sondern deren Zusammentreffen. Beziehungsattribute sind kein Fehler; sie gehören genau
dorthin.

---

## **3. Normalform (3NF) — keine Abhängigkeiten zwischen Nicht-Schlüssel-Spalten**

**Regel:** Die Tabelle ist in 2NF, **und** keine Nicht-Schlüssel-Spalte hängt von einer anderen
Nicht-Schlüssel-Spalte ab. Solche indirekten Abhängigkeiten heißen **transitiv**: A bestimmt B,
und B bestimmt C.

### Verstoß 1

| Bestellnummer | Kundennummer | Kundenname  | Kundenadresse |
|---------------|--------------|-------------|---------------|
| 123           | K001         | Max Muster  | Musterstraße 1|

**Problem:** „Kundenname“ und „Kundenadresse“ hängen nicht von der Bestellnummer ab, sondern von
der Kundennummer — und die ist selbst nur eine Nicht-Schlüssel-Spalte.

**Lösung:** „Kundennummer“, „Kundenname“ und „Kundenadresse“ kommen in eine eigene Tabelle
„Kunden“; in der Bestellung bleibt die Kundennummer als Fremdschlüssel.

### Verstoß 2

| Artikelnummer | Lagerbestand | Lieferant      | Lieferant-Adresse |
|---------------|--------------|----------------|--------------------|
| A001          | 50           | Firma XY       | XY-Straße 10       |

**Problem:** „Lieferant-Adresse“ hängt vom Lieferanten ab, nicht von der Artikelnummer.

**Lösung:** „Lieferant“ und „Lieferant-Adresse“ kommen in eine eigene Tabelle „Lieferanten“.

---

## **Prüft eure Tabellen damit durch**

Drei Fragen, die ihr an jede eurer Tabellen stellen könnt:

1. Gibt es **Zellen mit mehreren Werten** — Listen, Aufzählungen, „a, b, c“ in einem Feld?
   → Aufteilen, bis jede Zelle einen Wert enthält.
2. Besteht der Primärschlüssel aus **mehreren Spalten**, und gibt es Spalten, die nur von
   *einem Teil* davon abhängen? → Diese Spalten wandern in die Tabelle dieses Schlüsselteils.
3. Gibt es **Abhängigkeiten zwischen Nicht-Schlüssel-Spalten** — eine Spalte, die eine andere
   Spalte beschreibt statt den Schlüssel? → Beide in eine eigene Tabelle, Fremdschlüssel bleibt.

Eine Frage hilft fast immer weiter: **Über welche Sache ist dieser Wert eigentlich eine
Aussage?** Steht er nicht in der Tabelle dieser Sache, gehört er dorthin.

## **Kurzformel**

*Alles hängt vom Schlüssel ab, vom ganzen Schlüssel und von nichts als dem Schlüssel.*
