# Was macht gute Tabellen aus?

Hier stehen **dieselben Daten zweimal**: einmal so, wie eine Liste wächst, wenn lange niemand
aufräumt — und einmal aufgeräumt.

Es geht nicht um Regeln und nicht um Fachbegriffe, sondern um ein Gefühl dafür, **woran man
merkt, dass eine Tabelle nicht in Ordnung ist**: nämlich daran, dass einfache Wünsche plötzlich
schwierig werden. Vier davon gehen wir durch.

## Die gewachsene Liste

Ein Filmarchiv führt seinen Katalog. Angefangen hat es mit einer Tabellenkalkulation, und für
jeden neuen Film kam eine Zeile dazu. Alles steht in **einer** Tabelle — das war jahrelang bequem.

| titel | jahr | genres | regie | regie_geboren | studio | studio_stadt |
|---|---|---|---|---|---|---|
| Das Boot | 1981 | Drama, Krieg | Wolfgang Petersen | 1941 | Bavaria Film | München |
| Die unendliche Geschichte | 1984 | Fantasy, Abenteuer | Wolfgang Petersen | 1941 | Bavaria Film | München |
| Lola rennt | 1998 | Thriller, Drama | Tom Tykwer | 1965 | X-Filme | Berlin |
| Das Leben der Anderen | 2006 | Drama, Polit-Thriller | Florian H. von Donnersmarck | 1973 | Wiedemann & Berg | München |

## Wunsch 1 — „Zeig mir alle Thriller."

Die Datenbank soll die Zeilen finden, bei denen `Thriller` im Genre steht.

| Versuch | Ergebnis |
|---|---|
| genau `Thriller` | **nichts** — in der Zelle steht ja `Thriller, Drama`, nicht `Thriller` |
| Textsuche nach `…Thriller…` | **zwei** Filme — „Das Leben der Anderen" rutscht als *Polit-Thriller* mit rein |

Keiner der beiden Versuche gibt die richtige Antwort. Und die Frage „wie viele Filme habe ich je
Genre?" lässt sich überhaupt nicht stellen: Die Genres stehen zwar da, aber die Datenbank kann sie
nicht als Genres sehen. Für sie ist das ein Satz Text.

**Der Grund:** In einer Zelle stehen mehrere Werte. Damit wird aus einer Datenabfrage eine
Textsuche — und Textsuche ist raten.

## Wunsch 2 — „Bavaria Film ist nach Grünwald umgezogen."

Zwei Filme im Katalog gehören zu Bavaria Film. Also müssen **zwei** Zeilen geändert werden. Wenn
eine davon vergessen wird — eine Filterung, die eine Zeile nicht erwischt —, sieht der Katalog so
aus:

| titel | studio | studio_stadt |
|---|---|---|
| Das Boot | Bavaria Film | **Grünwald** |
| Die unendliche Geschichte | Bavaria Film | **München** |
| … | | |

Wo sitzt Bavaria Film jetzt? Die Tabelle behauptet beides, und keine der beiden Zeilen ist als die
falsche erkennbar.

**Der Grund:** Die Stadt ist eine Tatsache über *das Studio*, steht aber bei *jedem Film*. Was an
mehreren Stellen gepflegt werden muss, geht auf Dauer auseinander.

## Wunsch 3 — „Nimm ‚Das Leben der Anderen' aus dem Katalog."

Die Zeile wird gelöscht. Damit ist auch weg:

- dass es einen Regisseur namens Florian H. von Donnersmarck gibt
- dass er 1973 geboren ist
- dass es ein Studio namens Wiedemann & Berg gibt, und dass es in München sitzt

Gelöscht werden sollte ein **Film**. Verschwunden sind ein **Mensch** und eine **Firma**.

## Wunsch 4 — „Trag ein neues Studio ein."

Ein Studio, das noch keinen Film produziert hat, lässt sich gar nicht erst eintragen. Es gibt in
dieser Tabelle keine Zeile ohne Film — man müsste eine Zeile mit leerem Titel anlegen und hoffen,
dass sie später niemanden stört.

## Dieselben Daten, aufgeräumt

Der Umbau ist unspektakulär: **Jede Sache bekommt ihre eigene Tabelle.** Filme sind eine Sache,
Regisseure sind eine, Studios sind eine, Genres sind eine.

**studio**

| studio_nr | name | stadt |
|---|---|---|
| 1 | Bavaria Film | München |
| 2 | X-Filme | Berlin |
| 3 | Wiedemann & Berg | München |

**regie**

| regie_nr | name | geboren |
|---|---|---|
| 1 | Wolfgang Petersen | 1941 |
| 2 | Tom Tykwer | 1965 |
| 3 | Florian H. von Donnersmarck | 1973 |

**film** — statt der Namen stehen hier die Nummern aus den beiden Tabellen oben

| film_nr | titel | jahr | regie_nr | studio_nr |
|---|---|---|---|---|
| 1 | Das Boot | 1981 | 1 | 1 |
| 2 | Die unendliche Geschichte | 1984 | 1 | 1 |
| 3 | Lola rennt | 1998 | 2 | 2 |
| 4 | Das Leben der Anderen | 2006 | 3 | 3 |

**genre**

| genre_nr | name |
|---|---|
| 1 | Drama |
| 2 | Krieg |
| 3 | Fantasy |
| 4 | Abenteuer |
| 5 | Thriller |
| 6 | Polit-Thriller |

**film_genre** — eine Zeile je Zuordnung, statt einer Aufzählung in einer Zelle

| film_nr | genre_nr |
|---|---|
| 1 | 1 |
| 1 | 2 |
| 2 | 3 |
| 2 | 4 |
| 3 | 5 |
| 3 | 1 |
| 4 | 1 |
| 4 | 6 |

Verbunden wird über **Nummern statt über wiederholte Namen**. „Bavaria Film" steht genau einmal
im ganzen System — in `studio`, Zeile 1. Alle Filme dieses Studios tragen nur noch die `1`.

`film_genre` gibt es, weil ein Film mehrere Genres haben kann und ein Genre in mehreren Filmen
vorkommt. So etwas passt in keine Spalte, dafür braucht es eine eigene Tabelle.

## Dieselben vier Wünsche, noch einmal

| Wunsch | jetzt |
|---|---|
| „Zeig mir alle Thriller" | eine Abfrage auf `genre.name = 'Thriller'` — genau ein Treffer, kein Polit-Thriller dabei. Auch „wie viele je Genre" ist jetzt eine gewöhnliche Zählung. |
| „Bavaria Film zieht um" | **eine** Zeile ändern, in `studio`. Ein Widerspruch ist gar nicht möglich, weil die Stadt nur an einer Stelle steht. |
| „Nimm den Film raus" | eine Zeile aus `film` weniger. Donnersmarck steht weiter in `regie`, Wiedemann & Berg weiter in `studio`. |
| „Trag ein neues Studio ein" | eine Zeile in `studio`, fertig — ganz ohne Film. |

## „Aber dann sehe ich doch nicht mehr alles auf einmal!"

Doch. Die breite Ansicht ist nicht verloren, sie wird nur **bei Bedarf zusammengesetzt** — dafür
ist eine Datenbank da. Aus den fünf Tabellen oben lässt sich die ursprüngliche Liste jederzeit
wieder herstellen, Zeile für Zeile identisch.

Umgekehrt geht es nicht: Aus der gewachsenen Liste bekommt man den gelöschten Regisseur nicht
zurück, und die verlorene Wahrheit über den Firmensitz auch nicht.

**Aufteilen kostet die Übersicht nicht. Es kostet nur einmal Nachdenken.**

## Woran man ein gutes Tabellensystem erkennt

Kein Regelwerk — nur das, was du gerade gesehen hast:

- **Jede Tabelle beschreibt genau eine Sache.** Filme, Studios, Regie und Genres sind vier Sachen,
  also vier Tabellen.
- **In jeder Zelle steht ein Wert**, keine Aufzählung. Sonst suchst du im Text statt in Daten.
- **Jede Tatsache steht genau einmal.** Steht sie an zwei Stellen, werden die beiden früher oder
  später verschieden sein.
- **Zusammengehalten wird über Schlüssel**, nicht über wiederholte Namen.
- **Nichts verschwindet als Nebenwirkung.** Löscht man einen Film, soll kein Mensch mit
  verschwinden.

Wenn du bei deinem eigenen Modell unsicher bist, hilft meist eine einzige Frage:
**Über welche Sache ist dieser Wert eigentlich eine Aussage?** Und dann: Steht er auch dort?

---

Dass dieses Aufräumen einen Namen hat, Regeln und Stufen — das ist ein eigenes Thema und kommt
später dran. Nachschlagen kannst du es jederzeit in [`normalization.md`](./normalization.md).
