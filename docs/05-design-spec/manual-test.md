# Manueller Test des Übersetzungs-Prompts 0.8

Status: Draft
Last reviewed: 2026-10-08

Für wen: die Person, die Prompt 0.8 von Hand in myGenAssist durchspielt, bevor der n8n-Workflow gebaut wird.

Diese Anleitung beschreibt das Testen durch einen Menschen. Was der n8n-Workflow später automatisch tun muss, steht in [resume-loop.md](resume-loop.md).

## Was getestet wird

Prompt 0.8 läuft in fünf Etappen und gibt nach jeder zwei Blöcke aus: einen Statusblock und einen State-Block. Erreicht die Verarbeitung das Schrittlimit, ist das **kein Fehler** — ein Folgeaufruf setzt dort an, wo es stehen geblieben ist.

| Etappe | Ergebnis am Ende |
| ------ | ---------------------------------------------- |
| E1 | Seitenzahl, Texterkennung, Herkunftsklassifikation |
| E2 | vollständige Übersetzung, Terminologieliste |
| E3 | `001_Translated by AI.docx` |
| E4 | `001_Translated by AI.md` |
| E5 | Qualitätsbericht und Terminologie-CSV |

Ziel des Tests: Am Ende liegen alle vier Ausgabedateien vor, und es wurde **nichts doppelt gearbeitet**.

## Zwei Varianten — und warum die Wahl wichtig ist

| Variante | Aufwand | Was sie beweist |
| --- | --- | --- |
| **A** Fortsetzung im selben Chat | gering | Nur, dass die Fortsetzungsregel greift. Der Zustand steht noch im Gesprächsverlauf. |
| **B** Fortsetzung in einem neuen Chat | höher | Den zustandslosen Aufruf — genau den Weg, den n8n später geht. |

**Variante B ist der aussagekräftige Test.** In Variante A kennt die KI den Zustand aus dem Verlauf; der Transport über den State-Block wird gar nicht beansprucht. Ein erfolgreicher Test nach Variante A kann also die späteren Automatisierung trotzdem scheitern lassen. Nutze A als Schnelltest und B als Nachweis.

## 1. Vorbereitung

Bereitlegen:

- `docs/05-design-spec/promtpts for text recogniztion/prompt.en.0.8.md`
- `test_input/001.pdf` (3 Seiten, französisch, teils handschriftlich)

Beides wird als **Datei angehängt**. Die Promptdatei nicht in das Eingabefeld kopieren — sie ist über 1000 Zeilen lang und würde das Feld sprengen.

Sichere den Chatverlauf nach jedem Schritt, zum Beispiel durch Kopieren in eine Textdatei. Bei einem Abbruch ist der State nur dort greifbar; geht der Verlauf verloren, musst du von vorn beginnen.

## 2. Erster Aufruf

Hänge `prompt.en.0.8.md` und `001.pdf` an und schicke als Nachricht:

```text
Process the attached PDF according to the attached prompt file.
```

Mehr Begleittext ist nicht nötig — der Prompt beschreibt sich selbst.

Zu erwarten ist, dass nach **jeder** Etappe ein Blockpaar erscheint, nicht erst am Ende:

```text
===AI-TRANSLATION-STATUS===
run_state: INCOMPLETE
stages_completed: E1
next_stage: E2
pages_total: 3
pages_processed: 3
handwritten_segments: 19
files_written:
===END-STATUS===
===AI-TRANSLATION-STATE===
{ ... }
===END-STATE===
```

Bleibt das Blockpaar aus, obwohl Arbeit sichtbar geleistet wurde, ist das ein Befund gegen den Prompt — notiere ihn und brich ab.

## 3. Abbruch erkennen

Ein Abbruch liegt vor, wenn **einer** dieser Fälle eintritt:

- Es erscheint die Meldung „The assistant stopped after reaching the maximum number of steps for this turn."
- Die Antwort endet, aber der letzte Statusblock zeigt `run_state: INCOMPLETE`.
- Die Antwort endet mitten im Satz oder mitten in einem Block.

Maßgeblich ist immer das **letzte vollständige** Blockpaar — vollständig heißt: beide Begrenzerzeilen sind vorhanden. Ein abgeschnittener Block zählt nicht; dann gilt das Blockpaar davor.

Erscheint überhaupt kein vollständiges Blockpaar, behandle den nächsten Aufruf wie einen Erstaufruf (Abschnitt 2).

## 4. Variante A — Fortsetzung im selben Chat

1. Suche den **letzten vollständigen** Statusblock. Lies `next_stage` ab, zum Beispiel `E4`.
2. Schicke als neue Nachricht genau diesen Text, mit der abgelesenen Etappe:

   ```text
   Continue the processing run. Resume at stage E4 as stated in the last status block. Do not repeat completed stages.
   ```

3. Hänge **keine** Dateien erneut an.
4. Wiederhole ab Schritt 1, bis `run_state: COMPLETE` und `next_stage: NONE` erscheinen.

Ersetze `E4` jedes Mal durch den aktuellen Wert aus `next_stage`.

## 5. Variante B — Fortsetzung in einem neuen Chat

Dies stellt den Aufruf nach, den n8n später macht.

1. Kopiere aus der Antwort den **letzten vollständigen** State-Block — von `===AI-TRANSLATION-STATE===` bis `===END-STATE===`, beide Zeilen eingeschlossen.
2. Öffne einen **neuen** Chat.
3. Hänge `prompt.en.0.8.md` **und** `001.pdf` erneut an.
4. Schicke als Nachricht:

   ```text
   Continue the processing run described by the processing state below.
   Resume at the stage given in next_stage. Do not repeat completed stages.

   ===AI-TRANSLATION-STATE===
   { ... hier den kopierten State einfügen ... }
   ===END-STATE===
   ```

5. Wiederhole ab Schritt 1, bis `run_state: COMPLETE` erscheint.

Beim Kopieren beachten:

- Der State umfasst beim 3-Seiter grob 10–15 KB, weil er den vollständigen übersetzten Text enthält. Kopiere ihn **vollständig** und kürze nichts.
- Übernimm die Begrenzerzeilen **zeichengenau**. Eine Abweichung macht den State unbrauchbar, und das Ergebnis sieht dann wie ein Fehler des Prompts aus.
- Formatiere das JSON nicht um und rücke es nicht neu ein.
- Prüfe vor dem Absenden, dass das JSON mit `}` endet und nicht abgeschnitten ist.

## 6. Wann du den Test abbrichst

Diese Grenzen entsprechen den Exit conditions in [resume-loop.md](resume-loop.md):

| Fall | Vorgehen |
| --- | --- |
| Mehr als 8 Fortsetzungen für ein Dokument | Abbrechen, Verlauf sichern. |
| `stages_completed` bleibt zwei Fortsetzungen hintereinander unverändert | Abbrechen, Verlauf sichern. Die Verarbeitung macht keinen Fortschritt. |
| Kein Statusblock in der Antwort | Einmal wiederholen, dann abbrechen. |

Die letzten beiden Fälle sind **Befunde gegen den Prompt**, keine Bedienfehler. Sichere Verlauf und letzten State, damit die Ursache nachvollziehbar bleibt.

## 7. Protokollbogen

Zum Mitschreiben, damit der Testlauf auswertbar bleibt:

| Aufruf | Variante | `stages_completed` vorher | `stages_completed` nachher | neue Dateien | Beobachtung |
| ------ | -------- | ------------------------- | -------------------------- | ------------ | ----------- |
| 1 | — | — | | | |
| 2 | A / B | | | | |
| 3 | A / B | | | | |
| 4 | A / B | | | | |

## 8. Abschlussprüfung

Der Referenzlauf liegt in `test_input/Claude Opus 4.8/try 02/`. Daran messen:

**Vollständigkeit**

- Alle vier Ausgabedateien vorhanden: DOCX, MD, Qualitätsbericht, Terminologie-CSV.
- Letzter Statusblock zeigt `run_state: COMPLETE` und `next_stage: NONE`.

**Inhaltliche Konsistenz** — diese vier Zahlen müssen übereinstimmen:

- blau (#1F3FA8) eingefärbte Stellen im DOCX
- Word-Kommentare im DOCX, Autor `AI Translation`
- `[HW]`-Marker in der Markdown-Fassung
- `handwritten_segments` im Frontmatter der Markdown-Fassung

Im Referenzlauf sind das jeweils 19.

**Die wichtigste Gegenprobe: wurde doppelt gearbeitet?**

- `pages_processed` im letzten State darf keine Seite doppelt enthalten.
- Prüfe in den Antworten nach einer Fortsetzung, ob Seiten erneut gerendert oder die Übersetzung neu erstellt wurde.

Trifft das zu, hat die Fortsetzungsregel nicht gegriffen. Das ist der kritischste mögliche Befund: Die Verarbeitung käme zwar zum Ergebnis, aber die Automatisierung würde bei jedem Abbruch von vorn beginnen und wäre unwirtschaftlich.

**Budgetangabe (ab 0.8)**

Der Qualitätsbericht beginnt mit dem Block „Budgetverbrauch". Beim Handtest misst niemand — n8n gibt es noch nicht —, deshalb steht dort `nicht verfügbar`, und „Einschränkungen" wiederholt den Punkt. **Das ist der erwartete Befund, kein Fehler.**

Der eigentliche Prüfpunkt ist das Gegenteil: Steht dort eine **Zahl**, ist das ein Befund gegen den Prompt. Dann hat das Modell geschätzt oder selbst gemessen — beides ist ihm untersagt. Prüfe in diesem Fall im Antworttext, ob es einen Werkzeugaufruf zur Budgetermittlung unternommen hat, und notiere es.

Wer den Zahlenpfad trotzdem prüfen will, hängt an eine Fortsetzungsnachricht drei Zeilen an:

```text
budget_consumed: 0.42
budget_unit: EUR
budget_calls: 2
```

Erwartet: Der Bericht gibt exakt `0.42 EUR` aus — nicht gerundet, nicht umgerechnet, nicht „präzisiert" — mit dem Hinweis, dass der letzte Aufruf nicht enthalten ist. Im State-Block steht derselbe Wert mit `measured_by: "caller"`. Die Zahl erscheint **nicht** im Übersetzungsdokument, nicht auf der Präambelseite und nicht in der Markdown-Fassung.

**Dokumentation**

- Der Qualitätsbericht vermerkt unter „Einschränkungen", dass die Verarbeitung in mehreren Abschnitten erfolgte.

## 9. Was nach dem Test zu tun ist

Trage das Ergebnis in [resume-loop.md](resume-loop.md) unter „Open questions" nach. Variante B beantwortet dort eine der offenen Fragen: ob ein Aufruf ohne vorhandene Sitzung allein mit dem State-Block fortsetzen kann.

Die zweite offene Frage — ob myGenAssist über n8n Dateien zurückliefert oder nur Text — lässt sich mit diesem Test **nicht** klären. Sie bleibt offen und sollte vor dem Bau des Workflows beantwortet werden.
