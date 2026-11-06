# Veeva Vault Email Intake - Fragen & Antworten

Protokoll der Fragen zum Veeva Vault "Email to Vault" / Email Intake.
Antworten basieren auf der offiziellen Veeva Vault Platform Help
(General Release). Stand: 2026-10-27. Fragen 4 und 5 beziehen
zusaetzlich die Limited-Release-Doku zu 26R3 ein; das ist dort
jeweils gekennzeichnet.

Englische Fassung: [Veeva Email Intake QA (EN).md](<Veeva Email Intake QA (EN).md>)

---

## Frage 1 - Wer darf Emails an den Intake senden?

**Frage:** Wer kann Emails an den Intake senden? Koennen das beliebige
Personen sein oder muss die Emailadresse dem Vault als erlaubte
Absenderadresse bekannt sein?

**Antwort:**

Das ist konfigurierbar. Jede *Inbound Email Address* (Admin >
Configuration > Inbound Email Addresses) hat ein Pflichtfeld
**Allowed Senders**. Vault nimmt eine Mail nur an, wenn die
Absenderadresse zur gewaehlten Gruppe passt - sonst wird sie
abgewiesen bzw. als *Email*-Record im Status *Bounced* / *Failed*
abgelegt.

Optionen fuer **Allowed Senders**:

| Option | Wer darf senden |
| --- | --- |
| All Users & Persons in this Vault | Jede Adresse, die an einem *User*- oder *Person*-Record haengt |
| All Users in this Vault | Nur Adressen an *User*-Records |
| Specific Groups | Nur *User*-Adressen aus 1-5 ausgewaehlten *Allowed Sender Groups* |
| Anyone | Beliebige Absender (in der Doku nur indirekt erwaehnt, bei Email Processor User) |

Praktische Konsequenzen:

- Default-Erwartung: Der Absender muss Vault bekannt sein (als *User*
  oder *Person*). Voellig beliebige Externe gehen nur mit der
  Einstellung "Anyone".
- Externe ohne Vault-Login kann man ueber *Person*-Records
  beruecksichtigen, ohne ihnen eine Lizenz zu geben.
- Bei "Anyone" oder "All Users & Persons" kann ein **Email Processor
  User** hinterlegt werden - unter diesem User laeuft die
  Verarbeitung, wenn der Absender kein Vault-User ist. Das Audit Trail
  weist die Aktionen dann diesem User zu.
- **Always Run as Email Processor User** erzwingt diesen User auch
  dann, wenn der Absender ein Vault-User ist.
- **Authenticate Sender** (optional, empfohlen) prueft SPF und DKIM,
  verhindert also Absender-Spoofing. Abschalten ist nur bei
  bestimmten Application-Processors moeglich und ist riskant.
- Empfohlener Weg fuer Firmenadressen: Auto-Forwarding / Redirect von
  einer Adresse der eigenen Domain auf die
  `<name>@<subdomain>.veevavault.com`-Adresse. Die meisten
  Enterprise-Mailsysteme erhalten dabei den Originalabsender, sodass
  die Allowed-Sender-Pruefung weiter gegen die echte Person laeuft.

Nebenbedingungen, die mit dranhaengen:

- Max. 250 Inbound Email Addresses pro Vault.
- Max. 40 MB pro Mail inkl. Anhaenge (gilt fuer .EML, nicht .MSG).
- Testmail mit Betreff `Email to Vault Test` erzeugt nur einen
  *Email*-Record, ohne den Processor laufen zu lassen.

Quellen:

- Configuring Email to Vault -
  https://platform.veevavault.help/en/gr/74285/
- Email Processing -
  https://platform.veevavault.help/en/gr/74665/

---

## Frage 2 - Complaints von unbekannten Absendern empfangen

**Frage:** Wir wollen Complaints empfangen und verarbeiten. Daher sind
uns die Absenderadressen nicht bekannt. Wie kann man solche Emails
empfangen?

**Antwort:**

Genau dafuer gibt es in Vault QMS die Funktion **Complaint Email
Ingestion**. Der Weg besteht aus zwei Teilen: Absenderfreigabe oeffnen
und den QMS-Processor *Create Complaint* konfigurieren.

### 0. Was "Complaint Email Ingestion" ueberhaupt ist

Kein eigenes Produkt und kein Zukauf, sondern eine
**Standardfunktion von Vault QMS**, die in IQMS bereits enthalten ist
und nur konfiguriert werden muss. Sie besteht aus drei Teilen:

1. **Ein Vault-eigenes Postfach.** Vault erhaelt eine echte
   Mailadresse der Form `complaints@<subdomain>.veevavault.com` - die
   *Inbound Email Address*. Diese Adresse gibt man nach aussen, oder
   man leitet eine Bayer-Adresse dorthin weiter.
2. **Ein Email Processor namens `Create Complaint`.** Ein Email
   Processor ist in Vault die Logik, die bestimmt, was mit einer
   eingehenden Mail geschieht. Veeva liefert mehrere mit: der
   generische *Create Document from Email* macht ein unklassifiziertes
   Dokument daraus, der QMS-spezifische *Create Complaint* legt
   stattdessen einen *Complaint*- bzw. *Complaint Intake*-Record an.
   Pro Postfach wird ein Processor gewaehlt.
3. **Eine Zuordnung Mail -> Objektfelder.** Der Processor zerlegt die
   Mail und schreibt Absender, Betreff, Datum, Body und Anhaenge in
   definierte Felder des Records (siehe Mapping-Tabelle unten). Die
   Original-Mail als `.EML` und alle Anhaenge landen in der
   Attachments-Section.

Ablauf in einem Satz: Ein Kunde schreibt an
`complaints@...veevavault.com`, Vault nimmt die Mail an,
*Create Complaint* erzeugt daraus automatisch einen Record mit allen
Daten und Anhaengen, und ein Bearbeiter sieht ihn in seiner
Triage-Liste - ohne manuelles Abtippen oder Hochladen.

Warum das die gestellte Frage beantwortet: Der generische Weg setzt
voraus, dass der Absender Vault bekannt ist. Complaint Email Ingestion
ist die von Veeva vorgesehene Ausnahme, gebaut fuer Meldungen von
aussen. Daher gibt es dort den *Email Processor User* (jemand muss den
Record anlegen, wenn der Absender kein Vault-User ist), die
Thread-Erkennung (Rueckfragen und Antworten gehoeren zum selben Fall)
und die *Complaint Intake*-Stufe (ungeprueftes zuerst triagieren).

Abgrenzung: Ohne diese Funktion liessen sich Mails zwar ebenfalls
empfangen, es entstuenden aber nur unklassifizierte Dokumente - kein
Complaint-Record, keine Feldbefuellung, kein QMS-Prozess. Alles
Weitere muesste selbst gebaut werden.

### 1. Absenderfreigabe oeffnen

An der *Inbound Email Address*:

- **Allowed Senders** = *Anyone*. Damit entfaellt die Pruefung gegen
  *User*/*Person*-Records, beliebige Complainants koennen senden.
- **Email Processor User** ist dann Pflicht in der Praxis: unter
  diesem Service-User laeuft die Verarbeitung und wird auditiert,
  weil der Absender kein Vault-User ist. Er braucht *Read* auf
  *Email*, *Person*, *Complaint*, *Complaint Intake*, *Quality Event*
  sowie Create/Edit auf dem Zielobjekt.
- **Authenticate Sender** (SPF/DKIM) aktiviert lassen. Bei offenem
  Postfach ist das der einzige Spoofing-Schutz. Veeva erlaubt das
  Abschalten nur bei bestimmten Application-Processors und warnt
  ausdruecklich davor.
- Alternative, falls "Anyone" organisatorisch nicht gewollt ist: eine
  Bayer-Adresse (z. B. `complaints@bayer.com`) als oeffentliche
  Kontaktadresse betreiben und per **Auto-Forwarding** an die
  `...@<subdomain>.veevavault.com`-Adresse weiterleiten. Der
  Originalabsender bleibt erhalten; die Zugangskontrolle liegt dann
  beim Bayer-Mailsystem (Spam-/Malware-Filter) statt bei Vault.
  Achtung: Weiterleitung kann SPF/DKIM brechen - dann muss das
  Forwarding SRS/ARC-faehig sein oder *Authenticate Sender* scheitert.

### 2. Complaint Email Ingestion konfigurieren

- Pro Complaint-Typ eine eigene *Inbound Email Address* anlegen und
  dort den Email Processor **Create Complaint** waehlen.
- Zu jeder Adresse eine **Inbound Email Address Configuration**
  (Admin > Configuration > Inbound Email Address Configurations)
  anlegen mit: Label, Status (Inactive = es werden keine Complaints
  erzeugt), Inbound Email Address, Zielobjekt (*Complaint*,
  *Complaint Intake* oder *Quality Event*) und Object Type.
- **Email Thread Detection**: *Match on Message ID* (Default) oder
  *Match on Root Message ID*. Antworten des Melders erzeugen damit
  keinen neuen Record, sondern haengen am bestehenden.
- Optional abschaltbar: Body-/Text-Parsing und Email-/
  Attachment-Parsing.
- Die Section bzw. das Feld **Email Body** muss ins Page Layout des
  *Complaint Email* Object Types aufgenommen werden.

### 3. Empfehlung fuer unbekannte Absender: Complaint Intake

Bei oeffentlichem Postfach sollte das Zielobjekt **Complaint Intake**
sein, nicht direkt *Complaint*. *Complaint Intake* ist genau als
Triage-Stufe gedacht: potenzielle Complaints werden erfasst und erst
nach Pruefung zu echten *Complaint*-Records promoted. Das faengt Spam
und Fehlsendungen ab, bevor sie im regulierten Complaint-Prozess
landen.

### Automatische Feldbefuellung

| Email | Feld auf Complaint / Complaint Intake |
| --- | --- |
| Original Sender | `initial_reporter_details__v` |
| From-Adresse | `sender_email_address__v` |
| Sendedatum | `initial_report_date__v` |
| Betreff | `title__v` (Standard 150 Zeichen) |
| Body | `email_body__v` (Anzeige, bis 32.000 Zeichen) |
| Body als Text | `email_text__v` |
| Anhaenge | Attachments-Section, Original als .EML + Dateien |
| Metadaten | `initial_contact_method__v` = `email__v`, `vault_email_inbox_address__v`, `message_id__v`, `root_message_id__v` |

### 4. Schritt-fuer-Schritt-Anleitung der Konfiguration

Reihenfolge einhalten: die Datenobjekte muessen stehen, bevor das
Postfach sie referenzieren kann. Alle Schritte laufen in Vault unter
**Admin**, zuerst in DEV/Sandbox, dann per Migration nach QA/PROD.

**Schritt 1 - Complaint-Datenmodell klaeren.**
Feststellen, ob das Vault das eigenstaendige *Complaint*-Objekt oder
*Quality Event* mit Object Type *Complaint* nutzt. Alle folgenden
Schritte haengen an dieser Entscheidung. Bei Unklarheit:
Admin > Configuration > Objects pruefen.

**Schritt 2 - Objekt *Complaint Intake* aktivieren und einrichten.**
(Empfohlene Triage-Stufe fuer unbekannte Absender.)

1. **Object Type aktivieren** - *Complaint Intake* fuer Pharma, bzw.
   *MedTech Complaint Intake* fuer MedTech.

   "Aktivieren" heisst hier **nicht anlegen**: beide Object Types
   sind als Teil des QMS-Standarddatenmodells bereits vorhanden,
   stehen aber auf Status *Inactive*. Solange ein Object Type
   inaktiv ist, koennen weder Benutzer noch der Email Processor
   Records dieses Typs erzeugen. Klickpfad:

   1. **Admin > Configuration > Objects > Complaint Intake**.
   2. Register **Object Types** oeffnen. Ist dieses Register nicht
      vorhanden, sind Object Types am Objekt noch nicht
      eingeschaltet: Register **Details > Edit >** Checkbox
      **Enable Object Types** setzen **> Save**. Vault legt dann
      automatisch den Basistyp an und blendet das Register ein.
   3. Den gewuenschten Object Type ueber sein Label oeffnen.
   4. **Edit** klicken, **Status** auf *Active* setzen, **Save**.

   Falls der benoetigte Object Type wider Erwarten fehlt, laesst er
   sich im selben Register ueber **Create** anlegen (Label, Plural
   Label, optional Name/Description, Status). Pro Objekt sind
   maximal 50 Object Types moeglich.

2. **Objektfelder aktivieren und dem Object Type zuweisen** - alle
   Felder, die der Ziel-Complaint-Object-Type als Pflichtfelder
   verlangt. Sonst scheitert spaeter *Promote to Complaint*.

   Auch hier zwei verschiedene Dinge:

   - *Feld aktiv schalten*: Admin > Configuration > Objects >
     [Objekt] > **Fields**, Feld oeffnen, **Edit**, Status auf
     *Active*, **Save**.
   - *Feld dem Object Type zuordnen*: Register **Object Types >**
     Actions-Menue **> Edit Object Type Fields**. Vault zeigt eine
     Matrix aus Object Types und Feldern; die passenden Checkboxen
     setzen und **Save**.

   Hinweise dazu: Pflichtfelder auf Objektebene gelten automatisch
   fuer alle Object Types und sind dort nicht abwaehlbar. Neu
   angelegte Felder sind zunaechst nur dem Basistyp zugeordnet und
   muessen manuell zugewiesen werden.

3. Page Layout fuer den Object Type anlegen.
4. **Wichtig:** die Spezial-Section oder das Feld **Email Body** ins
   Layout aufnehmen. Ohne das ist der Mailinhalt im Record nicht
   sichtbar.
5. Layout um die Related-Object-Sections ergaenzen: erzeugte
   *Complaints*, *Reported Products*, optional *Complaint Contacts*
   und *Complaint Intake Follow-Ups*.
6. Optional: eigenen Tab fuer *Complaint Intake* anlegen, damit die
   Triage-Liste schnell erreichbar ist.
7. Quality Teams fuer *Complaint Intake* konfigurieren.

**Schritt 3 - Ziel-Complaint-Objekt vorbereiten.**
Auf dem Layout von *Complaint* bzw. *Quality Event Complaint* das
Feld **Complaint Intake** einblenden. Nur wenn diese Referenz
befuellt ist, zeigt der Complaint spaeter Contacts, Follow-Ups und
deren Attachments an.

**Schritt 4 - Service-User fuer die Verarbeitung anlegen.**
Einen dedizierten *Email Processor User* anlegen (kein persoenlicher
Account). Benoetigte Rechte laut aktueller Doku
**[26R3-Abgleich 2026-11-05 - praezisiert, vorher nur generisch
"Complaint"/"Quality Event" genannt]**:

- *Read* auf *Email*.
- Bei Zielobjekt *Complaint Intake*: zusaetzlich *Read* auf
  *Complaint Intake Email* und *Complaint Intake Sent Notif*, sowie
  *Edit* und *Create* auf *Complaint Intake*.
- Bei Zielobjekt *Complaint* (bzw. *Quality Event* Object Type
  *Complaint*): zusaetzlich *Read* auf *Complaint Email* und
  *Complaint Sent Notification*, sowie *Edit* und *Create* auf dem
  jeweiligen Zielobjekt/Object Type.
- *Complaint Intake Email* / *Complaint Email* sind die
  Object-Type-spezifischen Varianten des generischen *Email*-Records
  fuer die jeweilige Ingestion; *Complaint Intake Sent Notif* /
  *Complaint Sent Notification* sind die Tracked-Email-Records fuer
  ausgehende Benachrichtigungen (separat von *Complaint Intake
  Followup Sent Notif*, siehe Frage 5).

**Schritt 5 - Inbound Email Address anlegen.**
Admin > Configuration > Inbound Email Addresses > **Create**,
pro Complaint-Typ eine eigene Adresse:

1. **Name** und **Label** vergeben.
2. **Email Address**: nur der lokale Teil; vollstaendig wird daraus
   `<name>@<vault-subdomain>.veevavault.com`.
3. **Email Processor**: *Create Complaint*.
4. **Allowed Senders**: *Anyone* (das ist der Kern der Loesung fuer
   unbekannte Absender).
5. **Email Processor User**: der Service-User aus Schritt 4.
6. **Always Run as Email Processor User** aktivieren, damit die
   Verarbeitung auch bei zufaellig bekannten Absendern einheitlich
   unter dem Service-User laeuft.
7. **Authenticate Sender** aktiviert lassen (SPF/DKIM).
8. **Send Bounce Notification** bewusst entscheiden - bei
   oeffentlichem Postfach antwortet Vault sonst an beliebige
   Adressen.

**Schritt 6 - Erstes Postfach testen, bevor es weitergeht.**
Die *erste* Inbound Email Address eines Vaults braucht mehrere
Stunden, bis sie aktiv ist. Testmail mit dem exakten Betreff
`Email to Vault Test` senden: Vault legt nur einen *Email*-Record an
und startet den Processor nicht. Erscheint der Record, ist die
Adresse betriebsbereit. Weitere Adressen sind sofort nutzbar.

**Schritt 7 - Inbound Email Address Configuration anlegen.**
Admin > Configuration > Inbound Email Address Configurations >
**Create**, eine pro Adresse:

1. **Label** vergeben.
2. **Status**: zunaechst *Inactive* - solange erzeugt Vault keine
   Records. Erst nach dem Ende-zu-Ende-Test auf *Active* setzen.
3. **Inbound Email Address** waehlen (die Liste zeigt nur Adressen,
   die noch keiner anderen Configuration zugeordnet sind; der
   Processor wird automatisch uebernommen).
4. **Object**: *Complaint Intake* (Empfehlung), alternativ
   *Complaint* oder *Quality Event*.
5. **Object Type** waehlen - dieser Typ wird je Mail erzeugt.
6. **Email Thread Detection**: *Match on Message ID* (Default) oder
   *Match on Root Message ID*, wenn der ganze Thread auf einen Fall
   laufen soll.
7. Parsing-Optionen nur setzen, wenn Body bzw. Anhaenge bewusst
   nicht uebernommen werden sollen - fuer Complaints normalerweise
   beides eingeschaltet lassen.
8. **Save**.

**Schritt 8 - Promote to Complaint konfigurieren.**
Auf dem Lifecycle des *Complaint Intake* die Action
*Promote to Complaint* einrichten - als User Action, Entry Action
oder Workflow-Schritt:

- **Object Type** des zu erzeugenden *Complaint* waehlen.
- **Split by Batch** optional (Default aus): erzeugt je
  Produkt/Batch-Kombination einen eigenen Complaint.
- **Copy Attachments** optional (Default an).
- Die Action laeuft **nur einmal** pro Intake-Record; ein zweiter
  Aufruf erzeugt einen Systemfehler.
- Vor Ausfuehrung muessen alle Pflichtfelder des *Complaint* auf
  Intake und *Reported Product* befuellt sein.

**Schritt 9 - Ende-zu-Ende testen.**
Configuration auf *Active* setzen und von einer externen Adresse
(bewusst eine, die Vault nicht kennt) eine Mail mit Anhang senden.
Pruefen: Intake-Record entsteht, Felder sind befuellt, .EML und
Anhaenge liegen in der Attachments-Section, eine Antwort auf dieselbe
Mail erzeugt keinen zweiten Record, *Promote to Complaint* erzeugt
den Complaint.

**Schritt 10 - Nach QA/PROD migrieren.**
Konfiguration ueber VPK/Migration Package uebertragen.
**Die Email-Adresse ist pro Vault verschieden**
(`<name>@<subdomain>.veevavault.com`) - in jeder Umgebung muss die
Adresse neu angelegt und die extern kommunizierte Adresse bzw. das
Auto-Forwarding entsprechend gesetzt werden.

### Grenzen und Fehlerverhalten

- Max. 40 MB pro Mail inkl. Anhaenge.
- Max. 50 Attachments pro Record; darueber hinaus gehende Anhaenge
  werden verworfen und der Absender bekommt eine Warnung.
- Gleicher Dateiname mit anderem Inhalt erzeugt eine neue
  Attachment-Version.
- Body > 32.000 Zeichen wird im Feld gekuerzt; vollstaendig nur im
  .EML-Anhang.
- Fehler: Benachrichtigung an den Absender ueber
  `qms_email_processing_failed__v`, bei Teilerfolg
  `qms_email_processing_warning__v`. Bei oeffentlichem Postfach
  bedeutet das: Vault antwortet an potenziell beliebige Adressen -
  vorher pruefen, ob das erwuenscht ist.
- Verschluesselte Mails unterstuetzt der generische *Create Document
  from Email* Processor nicht.

Quellen:

- Configuring Complaint Email Ingestion (QMS) -
  https://quality.veevavault.help/en/gr/61887102/
- Working with Complaint Email Ingestion (QMS) -
  https://quality.veevavault.help/en/gr/61887103/
- Configuring Complaint Intake & Promote to Complaint (QMS) -
  https://quality.veevavault.help/en/gr/928400/
- Using Complaint Intake & Promote to Complaint (QMS) -
  https://quality.veevavault.help/en/gr/28400/
- Setting Up Object Types -
  https://platform.veevavault.help/en/gr/32857/

---

## Frage 3 - Nachfrage-Email aus dem Complaint Intake heraus

**Frage:** Kann ich aus dem Vault heraus auf einen Complaint Intake
eine Nachfrage-Email an den Absender versenden? Es kann passieren,
dass nicht alle relevanten Daten vorhanden sind und daher eine
Nachfrage gestellt werden muss.

**Antwort:**

Ja. Die Funktion heisst **Quality External Notifications** mit der
Action *Send External Notification*, und *Complaint Intake* ist
ausdruecklich eines der unterstuetzten Objekte. Veeva nennt genau
diesen Anwendungsfall als Beispiel: Korrespondenz an Reporter oder
Complainant im Complaint- und Complaint-Intake-Prozess.

### Wichtige Abgrenzung: nicht Complaint Intake Follow-Up

Naheliegend, aber falsch: Das Objekt *Complaint Intake Follow-Up*
klingt nach dem Nachfrage-Mechanismus, **verschickt aber keine
Emails**. Es dient ausschliesslich der manuellen Dokumentation:
Der Bearbeiter fragt ueber einen beliebigen Kanal nach und haelt
die Anfrage anschliessend als Follow-Up-Record fest. Laut Veeva
soll External-Notification-Unterstuetzung fuer dieses Objekt erst in
einem kuenftigen Release kommen.

Daraus folgt eine Warnung fuer die Konfiguration: Einige Felder des
Objekts *Complaint Intake Follow-Up* sind bereits vorhanden, aber
fuer ein kuenftiges Release gedacht und duerfen noch nicht benutzt
werden - u. a. *Email Body Custom Text*, *Email Sent?*,
*Email Subject Custom Text*, *From*, *Reply To*,
*Send Email on Create?*, *Complaint Contacts*, *Email Template*.
Veeva empfiehlt, sie per Berechtigung auszublenden. Ebenso den Wert
*Auto* im Feld *Retry?*.

Der sendende Mechanismus ist also External Notifications; das
Follow-Up-Objekt ist nur die Dokumentationsspur daneben.

> **Update (Stand 2026-10-27):** Dieser Abschnitt beschreibt den
> General Release. Mit **26R3 Limited Release** (Feature
> *Complaint Intake Follow-Up: Email Collaboration*) gilt das
> Gegenteil: *Complaint Intake Follow-Up* wird dann zum zentralen
> Korrespondenzobjekt mit echtem Zwei-Wege-Email-Versand. Siehe
> [Frage 4](#frage-4---templates-fuer-rueckantworten-ausfuellen-review-vor-versand)
> und [Frage 5](#frage-5---sind-antworten-auf-eine-rueckfrage-einem-intake-zuordbar).

### Voraussetzung: Complaint Contacts statt Person

Fuer *Complaint Intake* gilt eine Besonderheit, die oft uebersehen
wird:

| Objekt | Person | Complaint Contact |
| --- | --- | --- |
| Complaint Intake | nicht unterstuetzt | **Pflicht** |
| Complaint / Quality Event Complaint | optional | optional |
| Complaint Intake Follow-Up (kuenftig) | nicht unterstuetzt | Pflicht |
| alle anderen Objekte | Pflicht | nicht unterstuetzt |

Der Empfaenger einer Nachfrage aus einem Intake ist also **immer ein
*Complaint Contact*-Record**, nie ein *Person*-Record. Das passt zum
Szenario unbekannter Absender: Der Melder muss nicht als *Person* im
Vault angelegt werden.

Damit ein Contact tatsaechlich angeschrieben werden kann, muessen
drei Felder stimmen:

- *Consent to Contact* = **Yes**
- *Email* = gueltige Adresse
- *Status* = **Active**

Weitere Regeln: Pro Intake ist nur **ein** Contact vom Object Type
*Initial Reporter* moeglich. *First Name* oder *Last Name* ist
Pflicht. Klammern oder eine Emailadresse im Namensfeld verhindern den
Versand - das ist eine dokumentierte Falle.

**[26R3-Abgleich 2026-11-05 - beantwortet eine bis dahin offene
Frage]** Ob der Contact automatisch aus der eingegangenen Mail
entsteht, war zum General-Release-Stand nicht dokumentiert. Mit dem
26R3-Limited-Release-Feature **Complaint Email Ingestion:
Auto-Create Complaint Contacts** ist das jetzt klar beantwortet: Ja,
wenn konfiguriert. An der *Inbound Email Address Configuration* fuer
das Zielobjekt *Complaint Intake* gibt es dafuer zwei Checkboxen:

- **Create Initial Reporter Contact from sender email**: legt einen
  *Complaint Contact* vom Object Type *Initial Reporter* aus dem
  Original-Absender an, falls fuer den Intake noch keiner existiert.
- **Create additional Complaint Contacts from To/CC emails**: legt
  fuer jede weitere Adresse in To/CC einen *Complaint Contact* vom
  Object Type *Email Contact* an.

Voraussetzung am Objekt *Complaint Contact*: der Object Type
*Email Contact* muss aktiviert sein (Admin > Configuration > Objects
> Complaint Contact > Object Types). Ohne 26R3-LR-Feature bzw. ohne
Aktivierung bleibt es beim General-Release-Verhalten: Der
*Create Complaint* Processor befuellt nur
`initial_reporter_details__v` und `sender_email_address__v` als
Textfelder auf dem Intake-Record, die Erzeugung des strukturierten
*Complaint Contact*-Records ist dann eine manuelle bzw.
Action-Trigger-Aufgabe. **In DEV verifizieren, welcher Modus aktiv
ist**, sonst wird der Nachfrageversand im Betrieb zum manuellen
Schritt. Zur Vereinfachung lassen sich Action Triggers konfigurieren,
die Contacts aus einem *Master Complaint Contact* befuellen.

### Konfiguration in Kurzform

1. **Action anlegen:** Am Objekt *Complaint Intake*
   **Actions > Create > Send External Notification > Continue >
   Save**. Dabei die Option *Available in All Lifecycle States*
   **nicht** setzen - die Action funktioniert damit nicht korrekt.
   Optional ebenso *Create Distribution Group Memberships* anlegen.
2. **Layout ergaenzen:** Section *Notification Recipients* und eine
   Related-Object-Section *Complaint Contacts* auf das
   Intake-Layout. Optional *Sent Notification* als Related Object,
   um versendete Nachrichten am Record zu sehen.
3. **Object Message Template anlegen** fuer den Nachfragetext.
   Besonderheit: Im Token den Praefix `Object` manuell durch
   `Custom` ersetzen, also `${Object.name__v}` ->
   `${Custom.name__v}`. `name__v` ist bei `Custom`-Tokens auf 40
   Zeichen begrenzt, Formelfelder werden nicht unterstuetzt.
4. **Quality External Notification anlegen:**
   Admin > Configuration > Quality External Notifications >
   **Create**, Objekt *Complaint Intake* waehlen.
5. **Notification Template hinzufuegen:** Hier statt des Feldes
   *Recipients* die **Complaint Contact Types** waehlen - also
   z. B. *Initial Reporter*. Das ist der Punkt, an dem die Nachfrage
   an den Melder adressiert wird.
6. **Action im Lifecycle verankern:** *Send External Notification*
   als User Action an einem Status wie "Nachfrage offen", oder als
   Entry/Event Action, wenn die Nachfrage automatisch gehen soll.

### Ablauf im Betrieb

Der Bearbeiter oeffnet den Intake-Record, fuehrt
**Send External Notification** aus, waehlt das Nachfrage-Template,
passt ggf. die Empfaenger an (das Feld heisst bei Complaint Contacts
*Complaint Contacts* statt *Additional Recipients*), kann die Mail
unter *Preview Email* vorab ansehen und sendet.

### Der entscheidende Punkt: die Antwort kommt zurueck in den Record

Antwortet der Melder auf die Nachfrage, erkennt der Email Processor
anhand von Message ID bzw. Root Message ID, dass bereits ein Record
existiert. Vault legt dann **keinen** neuen Intake an, sondern haengt
die Antwort an den bestehenden Record. Der Kreis schliesst sich also
automatisch - Voraussetzung ist die in Frage 2, Schritt 7
konfigurierte *Email Thread Detection*.

### Weitere nuetzliche Optionen

- **Tracked Emails:** Bei *Complaint* und *Complaint Intake* verfolgt
  Vault den Zustellstatus und legt ihn in *Email*- und
  *Quality Event Sent Notification*-Records ab - auswertbar fuer ein
  Mahnwesen bei ausbleibender Antwort. **[26R3-Abgleich 2026-11-05]**
  Fuer Versand/Empfang speziell ueber *Complaint Intake Follow-Up*
  gibt es dafuer ein eigenes Tracking-Objekt: *Complaint Intake
  Followup Sent Notif* (der *Complaint Intake Follow-Up Email
  Processor* braucht dafuer *Read*-Recht darauf, siehe Frage 5).
- **Reply To:** Feld aufs Layout nehmen, damit Antworten an die
  richtige Person gehen. Achtung: Manche Mailclients ignorieren
  Reply-To.
- **From:** Absender der Nachfrage steuerbar, setzt konfigurierte und
  verifizierte *Outbound Email Domains* sowie
  *From Email Address Persons* voraus - fuer eine Bayer-Absenderadresse
  statt `veevavault.com` relevant.
- **Communication Language:** Feld aktivierbar, dann Nachfragen in
  der Sprache des Melders; erfordert Templates in allen Sprachen
  (Bulk Translation ueber Admin > Settings > Language & Region
  Settings).
- **Do Not Include Headers and Footers:** bei Complaint-Object-Types
  abwaehlbar, falls die Vault-Standardkopfzeile nach aussen nicht
  erwuenscht ist.
- **Dokumente mitsenden:** als Link in einen externen Viewer oder als
  echter Anhang (Letzteres erfordert ein Application Setting).

### Einschraenkung beim automatischen Versand

Ist *Send External Notification* als Entry- oder Event-Action
konfiguriert und ein Empfaenger wird uebersprungen (fehlende Email,
inaktiv, *Consent to Contact* leer oder *No*), laeuft die Action fuer
die uebrigen Empfaenger weiter - **fuer die uebersprungenen entsteht
aber kein Sent-Notification-Record**. Es gibt dann also keine Spur,
dass jemand nicht erreicht wurde. Bei Pflichtnachfragen daher besser
mit einer User Action plus Pruefung arbeiten.

Quellen:

- Configuring External Notifications (QMS) -
  https://quality.veevavault.help/en/gr/77672/
- Using External Notifications (QMS) -
  https://quality.veevavault.help/en/gr/77669/
- Configuring Complaint Intake & Promote to Complaint (QMS) -
  https://quality.veevavault.help/en/gr/928400/
- Working with Complaint Email Ingestion (QMS) -
  https://quality.veevavault.help/en/gr/61887103/
- Configuring Email to Vault -
  https://platform.veevavault.help/en/gr/74285/

---

## Frage 4 - Templates fuer Rueckantworten, ausfuellen, Review vor Versand

**Frage:** Kann man Rueckantworten vorformulieren, sprich Templates
hinterlegen, diese ausfuellen, die Email aber zunaechst in einen
Review geben?

**Antwort in einem Satz:** Templates ja, Ausfuellen je nach Release,
ein echter Vier-Augen-Review der konkreten Email ist **nicht
Standardfunktion** - er muss ueber den Lifecycle oder ueber ein
freigegebenes Vault-Dokument gebaut werden.

Die drei Teile der Frage trennen sich sauber:

| Teilfrage | Antwort |
| --- | --- |
| Templates hinterlegen | Ja, Standard (Object Message Templates je Notification Template), beliebig viele, mehrsprachig |
| Template ausfuellen | Automatisch per Token immer; **freier Text** nur aus *Complaint Intake Follow-Up* heraus und erst ab 26R3 LR |
| Review vor Versand | Nur Selbstkontrolle (*Preview Email*). Kein Freigabeschritt auf der Email; nur indirekt ueber Lifecycle oder Dokument |

### 1. Templates hinterlegen - ja, Standard

Der Nachfragetext liegt als *Object Message Template* und wird in
einem *Notification Template* innerhalb der *Quality External
Notification* referenziert. Pro Objekt lassen sich beliebig viele
Templates anlegen; bei der User Action werden mehrere zur Auswahl
gestellt, der Bearbeiter waehlt beim Senden aus. Uebersetzungen
laufen ueber *Communication Language* und Bulk Translation.

Die Templates koennen Tokens enthalten (Praefix `Custom` statt
`Object`), also Feldwerte des Records einsetzen - Name des Melders,
Complaint-Nummer, Produkt. Das ist das "Ausfuellen" im
automatisierten Sinn.

### 2. Freien Text ergaenzen - abhaengig vom Release

Hier liegt die eigentliche Einschraenkung:

- **General Release (26R2, aktuell produktiv):** Der Bearbeiter kann
  im *Send External Notification*-Dialog **Empfaenger und Dokumente**
  anpassen, aber **nicht Betreff oder Body**. Der Mailtext ist genau
  das, was das Template nach Token-Ersetzung ergibt. Individuelle
  Rueckfragen ("bitte Chargennummer und ein Foto der Beschaedigung")
  muessen also entweder als eigenes Template vorliegen oder ueber ein
  Feld am Record eingegeben werden, das per Token ins Template
  gezogen wird. Letzteres ist der uebliche Workaround.
- **Ab 26R3 Limited Release (Feature *Complaint Intake Follow-Up:
  Email Collaboration*, geliefert mit 26R2.3):** Aus einem
  *Complaint Intake Follow-Up*-Record heraus oeffnet die Action
  einen Dialog, in dem der Bearbeiter **Betreff und Body frei
  eingeben** kann, waehrend der Boilerplate-Text des gewaehlten
  Templates erhalten bleibt. Zusaetzlich To/CC/BCC und Dokumente.
  Das ist die Funktion, die der Frage fachlich am naechsten kommt.

Damit aendert sich auch die Aussage aus Frage 3: *Complaint Intake
Follow-Up* ist **nicht mehr** nur Dokumentationsobjekt. Ab 26R3 LR
ist es das eigentliche Korrespondenzobjekt mit Zwei-Wege-Email.

### 3. Review vor Versand - nicht als Standardfunktion

Es gibt in Vault QMS **keinen Status "Email im Review"** und keine
Freigabe auf der einzelnen Nachricht. Was es gibt:

- **Preview Email** (26R2): Checkbox *Allow user to preview email?*
  an der *Send External Notification* **User Action** (nur dort, nicht
  bei Entry/Event Action). Der Dialog zeigt dann die vollstaendige
  HTML-Fassung mit aufgeloesten Tokens und ggf. uebersetztem Template.
  Das ist eine **Selbstkontrolle des Senders**, kein zweites
  Augenpaar. Bekannte Grenzen: Links und Dokument-Tokens werden in
  der Vorschau teils nicht korrekt dargestellt, im Versand aber
  schon.

Wer einen echten Review braucht, hat drei gangbare Wege:

**Weg A - Freigabe ueber den Lifecycle (leichtgewichtig).**
*Send External Notification* wird als **User Action nur in einem
bestimmten Status** verfuegbar gemacht, z. B.
*Nachfrage freigegeben*. Davor liegt ein Workflow-Schritt
"Nachfrage pruefen" auf dem *Complaint Intake* bzw. *Complaint
Intake Follow-Up*. Der Reviewer sieht den geplanten Text - bei
Freitextvariante im Feld *Latest Email Body Text* bzw. im
Entwurfsfeld, bei Template-Variante im Template selbst - und setzt
den Status weiter. Erst danach taucht die Action auf.
Einschraenkung: Was der Bearbeiter ab 26R3 im Dialog tippt, geht
ungeprueft raus. Der Lifecycle sichert den Zeitpunkt und die
Template-Auswahl, nicht den Freitext.

**Weg B - Geprueftes Dokument mitsenden (regulatorisch sauber).**
Der inhaltliche Teil wird als **Vault-Dokument** (Korrespondenzbrief,
Fragebogen) erstellt und durchlaeuft den normalen Document-Lifecycle
mit Review und Approval. Die Email selbst bleibt ein kurzes,
unveraenderliches Anschreiben aus dem Template; das freigegebene
Dokument geht als Link in einen externen Viewer oder - ab 26R2 - als
echter Anhang mit (Application Setting *Enable Document Attachments
on External Notifications*, max. 5 Anhaenge, 15.360 KB gesamt).
Das ist der von Veeva vorgesehene Weg fuer Inhalte, die eine Freigabe
brauchen, und der einzige mit sauberem Approval-Audit-Trail.

**Weg C - Kombination.** Lifecycle-Gate fuer den Versandzeitpunkt,
freigegebenes Dokument fuer den pruefpflichtigen Inhalt, Template
fuer den Rahmen. Fuer einen regulierten Complaint-Prozess die
realistische Zielarchitektur.

### Konsequenz fuer das Projekt

Wenn "Review vor Versand" eine harte Anforderung ist, darf der
Nachfragetext nicht frei im Dialog entstehen. Entweder er ist
vollstaendig im Template vorformuliert (dann reviewt man das
Template einmalig als Konfigurationsobjekt, nicht jede Mail), oder
der pruefpflichtige Teil wandert in ein freigegebenes Dokument.
Das ist als `FR-` bzw. als ADR zu fixieren, bevor die
Lifecycle-Konfiguration gebaut wird.

Quellen:

- Configuring External Notifications (QMS) -
  https://quality.veevavault.help/en/gr/77672/
- Using External Notifications (QMS) -
  https://quality.veevavault.help/en/gr/77669/
- Configuring Complaint Intake Follow-Up (QMS), Limited Release -
  https://quality.veevavault.help/en/lr/1227595/
- Working with Complaint Intake Follow-Up (QMS), Limited Release -
  https://quality.veevavault.help/en/lr/1227594/
- What's New in 26R2 (External Notifications: Preview Email;
  Support for Email Document Attachments) -
  https://rn.veevavault.help/en/gr/whats-new-in-26r2/
- New in 26R3 Limited Release (Complaint Intake Follow-Up:
  Email Collaboration) - https://rn.veevavault.help/en/lr/new-in-26r3/

---

## Frage 5 - Sind Antworten auf eine Rueckfrage einem Intake zuordbar?

**Frage:** Sind die Antworten auf eine Rueckfrage konkret einem
Complaint-Intake-Objekt zuordbar?

**Antwort:** Ja. Die Zuordnung laeuft automatisch ueber die
Email-Header (Message ID / Root Message ID), nicht ueber Textsuche
oder manuelle Verknuepfung. Es gibt zwei Ausbaustufen mit
unterschiedlicher Granularitaet.

### Stufe 1 - Zuordnung zum Complaint Intake (General Release)

Der *Create Complaint* Email Processor prueft bei jeder eingehenden
Mail **Message ID und References im Header**. Findet er einen
bestehenden *Complaint*- oder *Complaint Intake*-Record aus diesem
Thread, legt er **keinen neuen Record** an, sondern haengt die
Antwort an den bestehenden. Das gilt ausdruecklich auch fuer
Antworten auf eine aus Vault versendete External Notification.

Gesteuert wird das ueber *Email Thread Detection* an der
*Inbound Email Address Configuration*:

- *Match on Message ID* (Default) - Zuordnung ueber die einzelne
  Nachricht.
- *Match on Root Message ID* - Zuordnung ueber den ganzen Thread.
  Gibt es mehrere Records mit derselben Root Message ID, nimmt Vault
  den **zuletzt erzeugten**.

Granularitaet dieser Stufe: Die Antwort landet am richtigen
**Intake**. Welche konkrete Rueckfrage beantwortet wurde, ist daraus
nicht maschinell ablesbar.

### Stufe 2 - Zuordnung zur einzelnen Rueckfrage (26R3 LR)

Mit *Complaint Intake Follow-Up: Email Collaboration* (26R3 Limited
Release, geliefert mit 26R2.3) wird die Zuordnung feiner: nicht nur
zum Intake, sondern zum **einzelnen Follow-Up-Record**, also zur
konkreten Rueckfrage.

Mechanik:

1. Die Nachfrage geht aus einem *Complaint Intake Follow-Up*-Record
   raus; Vault erzeugt je Versand einen *Complaint Intake Follow-Up
   Email*-Record mit *Direction* = *Outbound*. **[26R3-Abgleich
   2026-11-05 - Korrektur]** Empfaenger (Feld *To*) ist primaer das
   Feld *Primary Contact* am Follow-Up-Record selbst; ist dort keiner
   gesetzt, nimmt Vault ersatzweise den *Complaint Contact* vom
   Object Type *Initial Reporter* des zugehoerigen *Complaint
   Intake*. Es ist also **nicht** pauschal immer der Initial
   Reporter, wie fruehere Fassungen dieses Dokuments nahelegten.
   Zusaetzlich waehlbar: *CC Contacts*, *Internal Recipients*
   (Person-Records, wahlweise als CC oder BCC) und *Documents to
   Send*.
2. Das **Reply-To** zeigt auf ein Postfach im **Bayer-Mailsystem**,
   nicht direkt auf Vault.
3. Die Antwort des Melders wird von dort **automatisch weitergeleitet**
   (Auto-Forward, ausdruecklich **nicht** Redirect) an eine zweite
   Inbound Email Address mit dem Processor **Complaint Intake
   Follow-Up Email Processor**.
4. Der Processor matcht ueber die **Root Message ID** - diese
   Einstellung ist hier **Pflicht**, nicht optional - und haengt die
   Antwort an den richtigen Follow-Up-Record.

Was dabei automatisch befuellt wird:

| Feld am *Complaint Intake Follow-Up Email* | Feld am *Complaint Intake Follow-Up* |
| --- | --- |
| *Complaint Intake Follow-Up* (Referenz) | - |
| *Direction* = *Inbound* | - |
| *Subject* | - |
| *Email Body Text* | *Latest Email Body Text*, optional *Latest Response Details* |
| *Email Body* (HTML, via *View Email*) | *Latest Email Body* |
| *Received Date* | *Latest Response Date* |
| *Original Sender Email* | - |

Zusaetzlich: Anhaenge der Antwort werden auf den Follow-Up kopiert
und sind ueber die Section *Follow-Up Attachments* auch am Intake
und an allen daraus erzeugten Complaints sichtbar. Der Status des
Follow-Up-Records wechselt automatisch. Treffen mehrere Antworten auf
eine Rueckfrage ein, entsteht **je Antwort ein eigener Email-Record**.
Der Bearbeiter kann ueber *Send Email Reply* direkt zurueckschreiben -
echte Zwei-Wege-Korrespondenz im Record.

Optional: *Create Complaint Contact Email Contacts from TO and CC
email Addresses* legt zusaetzlich angeschriebene Personen automatisch
als *Complaint Contact* am Intake an, damit sie in Folgemails
auswaehlbar sind.

### Grenzen der Zuordnung - das ist der Teil, der im Betrieb weh tut

- **Matching nur ueber Header.** Antwortet der Melder nicht per
  "Antworten", sondern schreibt eine neue Mail, fehlt die Root
  Message ID. Dann gibt es keinen Treffer.
- **Verhalten ohne Treffer:** Beim Follow-Up-Postfach legt Vault
  stattdessen einen **neuen *Complaint Intake*** an - der Object Type
  dafuer ist in der *Inbound Email Address Configuration* unter
  *If match not found, create Complaint Intake with this Object Type*
  zu konfigurieren. Die Antwort geht also nicht verloren, landet aber
  als Dublette in der Triage und muss manuell zusammengefuehrt werden.
  Diese Dublettenrate ist ein Mengenrisiko und sollte frueh gemessen
  werden.
- **Auto-Forward ist Pflicht**, Redirect bricht das Matching.
- **Allowed Senders am Follow-Up-Postfach** ist laut Doku *All Users
  & Persons in this Vault* - nicht *Anyone* wie beim Intake-Postfach.
  Das funktioniert, weil der tatsaechliche Absender an diesem
  Postfach das weiterleitende Bayer-System ist, nicht der externe
  Melder. Diese Konstruktion ist in DEV zu verifizieren, sie ist der
  fragilste Punkt der Kette.
- **Zwei Postfaecher noetig**: eines fuer den Erstkontakt
  (*Create Complaint*), eines fuer Follow-Up-Antworten
  (*Complaint Intake Follow-Up Email Processor*). Plus die
  Reply-To-Adresse im Bayer-Mailsystem.
- **[26R3-Abgleich 2026-11-05]** Benoetigte Rechte fuer den
  *Email Processor User* am zweiten Postfach: *Read* auf
  *Complaint Intake Followup Sent Notif*, *Edit* auf
  *Complaint Intake Follow-Up*, *Create* auf *Complaint Intake* und
  *Complaint Intake Follow-Up Email*.
- **Release-Stand:** Stufe 2 ist zum Stand dieses Dokuments
  **Limited Release**, nicht General Release. Vor einer Festlegung
  im Design ist zu klaeren, auf welchem POD und welchem Release-Track
  das IQMS-Vault laeuft und wann 26R3 dort ankommt.

### Kurzfassung fuer die Anforderungsdiskussion

Ja, Antworten sind zuordbar - sogar bis auf die einzelne Rueckfrage.
Die Zuordnung ist robust, solange der Melder antwortet statt neu zu
schreiben. Der Preis sind zwei Postfaecher, eine Weiterleitungsstrecke
im Bayer-Mailsystem und die Abhaengigkeit von einem Release, das
derzeit nur im Limited Release verfuegbar ist.

Quellen:

- Working with Complaint Email Ingestion (QMS) -
  https://quality.veevavault.help/en/gr/61887103/
- Configuring Complaint Email Ingestion (QMS) -
  https://quality.veevavault.help/en/gr/61887102/
- Configuring Complaint Intake Follow-Up (QMS), Limited Release -
  https://quality.veevavault.help/en/lr/1227595/
- Working with Complaint Intake Follow-Up (QMS), Limited Release -
  https://quality.veevavault.help/en/lr/1227594/
- New in 26R3 Limited Release (Complaint Intake Follow-Up: Email
  Collaboration; Auto-Retry; Auto-Create Complaint Contacts) -
  https://rn.veevavault.help/en/lr/new-in-26r3/

---

## Frage 6 - Welche Objekttypen sind am Complaint Handling beteiligt und wie haengen sie zusammen?

**Frage:** Welche Objekte spielen beim E-Mail-basierten Complaint
Handling eine Rolle, und wie sind sie miteinander verknuepft?

**Antwort:**

Diagramm (drawio):
[veeva-complaint-email-object-model.drawio](veeva-complaint-email-object-model.drawio)

### Die beteiligten Objekte

| Objekt | Rolle |
| --- | --- |
| **Inbound Email Address** | Vault-Konfigurationsobjekt, keine Daten-Records. Das Postfach selbst (`<name>@<subdomain>.veevavault.com`), mit Allowed-Senders-Regel und zugewiesenem Email Processor. |
| **Email** | Ein Record pro eingehender Nachricht: Original als `.EML`, Anhaenge, Status (*Received*, *Bounced*, *Failed*). Wird vom Processor gelesen, nicht vom Nutzer bearbeitet. |
| **Complaint Intake** | Die Triage-Stufe. Ein Record pro neuem Email-Thread. Pflichtfelder werden aus der Mail befuellt (siehe Frage 2, Mapping-Tabelle). |
| **Complaint Contact** | Ansprechpartner am Intake bzw. am Complaint. Fuer *Complaint Intake* ist dieser Objekttyp **Pflicht** (Object Type *Initial Reporter*, max. 1 pro Intake) - *Person* wird dort nicht unterstuetzt (siehe Frage 3). Object Type *Email Contact*: zusaetzliche Kontakte aus To/CC einer eingehenden Mail, automatisch anlegbar ueber *Auto-Create Complaint Contacts* (26R3 LR, **[26R3-Abgleich 2026-11-05]**). |
| **Person** | Alternative zu *Complaint Contact* fuer alle anderen QMS-Objekte (inkl. *Complaint*), aber **nicht** fuer *Complaint Intake*. |
| **Reported Product** | Das gemeldete Produkt/Charge, haengt am Intake und wird beim Promote mit uebernommen; kann *Split by Batch* zu mehreren Complaints fuehren. |
| **Complaint Intake Follow-Up** | Ab 26R3 LR das Korrespondenzobjekt fuer Rueckfragen (davor reine Dokumentationsablage, siehe Frage 3). Ein Record pro Rueckfrage. Felder *Retry?*/*Retry Frequency*/*Remaining Retries* steuern optional *Auto-Retry* (26R3 LR, siehe Frage 9). |
| **Complaint Intake Follow-Up Email** | Ein Record pro gesendeter oder empfangener Nachricht zu einer Follow-Up (Feld *Direction* = *Outbound*/*Inbound*). |
| **Complaint Intake Followup Sent Notif** | **[26R3-Abgleich 2026-11-05, neu erfasst]** Zustellstatus-Tracking speziell fuer *Complaint Intake Follow-Up*-Mails (separat vom allgemeinen *Quality Event Sent Notification*). |
| **Followup Evaluation** | **[26R3-Abgleich 2026-11-05, neues Objekt]** Automatisch erzeugter Impact-Bewertungs-Record pro betroffenem *Complaint*, wenn ein *Complaint Intake Follow-Up* neue, bewertungspflichtige Informationen erhaelt (26R3 LR). Siehe Frage 8. |
| **Complaint / Quality Event (Object Type Complaint)** | Der regulierte Ziel-Record, erzeugt durch *Promote to Complaint*. Referenziert den urspruenglichen *Complaint Intake* und macht damit dessen Contacts, Reported Products und Follow-Ups sichtbar. |
| **Quality Event Sent Notification / Email (Tracked Emails)** | Zustellstatus-Tracking fuer versendete External Notifications (allgemein, nicht Follow-Up-spezifisch). |

### Die Kernverknuepfungen

1. **Inbound Email Address -> Email -> Complaint Intake**: Der
   *Create Complaint*-Processor liest den *Email*-Record und legt
   (bzw. aktualisiert) daraus den *Complaint Intake* an. Steuerung ueber
   *Email Thread Detection* (Message ID / Root Message ID).
2. **Complaint Intake -> Complaint Contact (1:N, Pflicht)** und
   **-> Reported Product (1:N)**.
3. **Complaint Intake -> Complaint Intake Follow-Up (1:N)** - eine
   Rueckfrage pro Follow-Up-Record.
4. **Complaint Intake Follow-Up -> Complaint Intake Follow-Up Email
   (1:N)** - je Versand bzw. je Antwort ein eigener Email-Record.
5. **Complaint Intake -> Complaint (1:N via Promote to Complaint)** -
   der Complaint referenziert den Intake zurueck und "erbt" damit
   dessen Contacts/Products/Follow-Ups fuer die Anzeige.
6. **Complaint Intake -> "kein Promote"**: Spam, Werbung oder
   Fehlsendungen werden im Intake-Status erledigt (siehe Frage 7,
   Abschnitt e) und nie zum *Complaint*.
7. **[26R3-Abgleich 2026-11-05, neu]** **Complaint Intake Follow-Up ->
   Followup Evaluation (1:N, automatisch, nur nach Promote)** - je
   aktivem, nicht stornierten *Complaint* aus dem zugehoerigen
   *Complaint Intake* ein eigener *Followup Evaluation*-Record; dieser
   referenziert sowohl den *Complaint* als auch den *Complaint Intake*
   und den ausloesenden *Complaint Intake Follow-Up*. Siehe Frage 8.

Quellen:

- Configuring Complaint Email Ingestion (QMS) -
  https://quality.veevavault.help/en/gr/61887102/
- Working with Complaint Email Ingestion (QMS) -
  https://quality.veevavault.help/en/gr/61887103/
- Configuring Complaint Intake & Promote to Complaint (QMS) -
  https://quality.veevavault.help/en/gr/928400/
- Using Complaint Intake & Promote to Complaint (QMS) -
  https://quality.veevavault.help/en/gr/28400/
- Configuring External Notifications (QMS) -
  https://quality.veevavault.help/en/gr/77672/
- Configuring Complaint Intake Follow-Up (QMS), Limited Release -
  https://quality.veevavault.help/en/lr/1227595/
- Working with Complaint Intake Follow-Up (QMS), Limited Release -
  https://quality.veevavault.help/en/lr/1227594/
- Setting Up Object Types -
  https://platform.veevavault.help/en/gr/32857/

---

## Frage 7 - Ende-zu-Ende: Eingang, Rueckfrage, Antwort, Promotion, Nicht-Complaint-Mails

**Frage:** Wie werden eingehende Mails, Rueckfragen, Antworten auf
Rueckfragen und die Ueberfuehrung von Intake zu echtem Complaint im
Detail gehandhabt - und was passiert mit Mails, die gar keine
Complaints sind (z. B. Werbung)?

**Antwort:**

### a) Eingehende Mail (Erstkontakt)

1. Absender schreibt an die oeffentliche Inbound Email Address.
   Vault prueft **Allowed Senders** (bei Complaints: *Anyone*) und bei
   aktiviertem **Authenticate Sender** SPF/DKIM.
2. Besteht die Mail die Pruefung, legt Vault einen *Email*-Record an;
   der konfigurierte Processor **Create Complaint** laeuft, bei
   unbekanntem Absender unter dem **Email Processor User**.
3. Der Processor prueft **Message ID / References** im Header
   (*Email Thread Detection*). Kein Treffer -> neuer *Complaint
   Intake*-Record, Felder automatisch befuellt (siehe Frage 2,
   Mapping-Tabelle), Anhaenge + Original-`.EML` in die
   Attachments-Section.
4. Scheitert die Pruefung (unbekannter/nicht erlaubter Absender,
   SPF/DKIM-Fehler), wird die Mail abgewiesen; der *Email*-Record
   bekommt Status *Bounced*/*Failed*.
5. Details zur Konfiguration: siehe Frage 2.

### b) Rueckfrage (Outbound Follow-Up)

1. Der Bearbeiter oeffnet den *Complaint Intake* und loest
   **Send External Notification** aus (General Release) bzw. ab
   26R3 LR die Aktion am *Complaint Intake Follow-Up*-Record.
2. Empfaenger ist immer ein **Complaint Contact** vom Type
   *Initial Reporter* (nicht *Person*) - Voraussetzung: *Consent to
   Contact* = Yes, gueltige *Email*, *Status* = Active.
3. General Release: Text kommt vollstaendig aus dem Template
   (Tokens werden ersetzt), Betreff/Body sind nicht frei editierbar.
   Ab 26R3 LR: freier Text in Betreff/Body moeglich, Boilerplate
   bleibt erhalten; Vault legt dazu einen *Complaint Intake Follow-Up
   Email*-Record mit *Direction* = *Outbound* an.
4. **Reply-To** zeigt (ab 26R3 LR) auf ein Postfach im
   Bayer-Mailsystem, nicht direkt auf Vault - das ist die Grundlage
   fuer Teil c).
5. Details: siehe Frage 3 (Mechanik) und Frage 4 (Templates/Review).

### c) Antwort auf die Rueckfrage (Inbound Follow-Up Reply)

1. Antwortet der Melder, landet die Mail zunaechst im
   Bayer-Mailsystem (Reply-To) und wird von dort per
   **Auto-Forward** (nicht Redirect) an eine **zweite** Inbound Email
   Address mit dem Processor **Complaint Intake Follow-Up Email
   Processor** weitergeleitet.
2. Dieser Processor matcht **zwingend ueber die Root Message ID**
   und haengt die Antwort an den passenden *Complaint Intake
   Follow-Up*-Record (General Release ohne dieses Feature: die
   Antwort haengt nur am *Complaint Intake* selbst, nicht an der
   einzelnen Rueckfrage - siehe Frage 5, Stufe 1 vs. Stufe 2).
3. Kein Treffer (z. B. weil der Melder eine neue Mail statt einer
   Antwort schreibt) -> Vault legt einen **neuen Complaint Intake**
   an (konfigurierter Fallback-Object-Type). Das ist der dokumentierte
   Dublettenfall, siehe Frage 5, Abschnitt "Grenzen der Zuordnung".
4. Details inkl. Feldbefuellung: siehe Frage 5.

### d) Ueberfuehrung Intake -> echter Complaint (Promote to Complaint)

1. Bevor promoted werden kann, muessen alle Pflichtfelder des
   Ziel-*Complaint*-Object-Types auf *Complaint Intake* und
   *Reported Product* befuellt sein.
2. Der Bearbeiter (oder eine Entry/Workflow-Action) loest
   **Promote to Complaint** aus. Optional **Split by Batch** (ein
   Complaint je Produkt/Charge-Kombination) und **Copy Attachments**.
3. Vault erzeugt den *Complaint*- bzw. *Quality Event*-Record im
   gewaehlten Object Type und setzt die Rueckreferenz **Complaint
   Intake** - dadurch werden Contacts, Reported Products und
   Follow-Ups (inkl. deren Attachments) auch am Complaint sichtbar.
4. Die Action laeuft **nur einmal** pro Intake; ein zweiter Aufruf
   erzeugt einen Systemfehler - es gibt also keinen Weg, versehentlich
   zwei Complaints aus einem Intake zu erzeugen.
5. Details: siehe Frage 2, Schritt 8.

### e) Nicht-Complaint-Mails (Werbung, Spam, Fehlsendungen)

Das ist der Teil, den die Veeva-Standardfunktion **nicht** automatisch
loest:

- *Create Complaint* ist ein reiner **Transkriptions-Processor**: er
  liest Absender, Betreff, Body und Anhaenge und schreibt sie in
  Felder - er bewertet den **Inhalt** nicht. Jede angenommene Mail
  (die Allowed-Senders- und SPF/DKIM-Pruefung besteht) erzeugt einen
  *Complaint Intake*-Record, unabhaengig davon, ob es sich tatsaechlich
  um eine Beschwerde, eine Werbemail, eine Produktanfrage oder Spam
  handelt.
- Genau dafuer ist *Complaint Intake* als **Triage-Stufe** gedacht
  (siehe Frage 2, Abschnitt 3): Ein Bearbeiter - oder eine
  vorgeschaltete Klassifizierung - muss jeden Intake-Record pruefen
  und entscheiden, ob er ein echter Complaint ist.
- Wird ein Intake als Nicht-Complaint erkannt (Werbung, Spam,
  Produktfrage ohne PTC-Bezug, Fehlsendung etc.), wird er **nicht
  promoted**. Stattdessen wird er ueber den Lifecycle des *Complaint
  Intake* geschlossen bzw. abgelehnt (z. B. Status *Rejected* /
  *Closed - Not a Complaint*, je nach Lifecycle-Konfiguration des
  Projekts). Es entsteht **kein** *Complaint*-Record, und der Vorgang
  verlaesst damit den regulierten Complaint-Prozess, bleibt aber als
  Intake-Record (mit Audit Trail) im Vault erhalten.
- Diese Entscheidung (Complaint ja/nein, und bei "ja" welcher
  Complaint-Typ) ist in diesem Projekt **nicht Veeva-nativ geloest**,
  sondern Gegenstand der eigenen Klassifizierungslogik (siehe
  `docs/05-design-spec/prompts-classification/` und
  `docs/templates/assets/classification-decisions.drawio` in diesem
  Repo) - dort wird exakt diese Vorpruefung (PTC-relevant? Spam?
  Werbung? Malware? Produktanfrage?) als vorgelagerter
  Entscheidungsbaum beschrieben. Veeva liefert die Triage-*Buehne*
  (*Complaint Intake*), die Klassifizierungs-*Logik*, was auf dieser
  Buehne mit einem konkreten Record passiert, muss das Projekt selbst
  bauen (manuell oder KI-gestuetzt vor bzw. nach dem Promote-Schritt).
- Wichtig fuer die Spam-/Werbung-Abwehr auf Mailebene (bevor ueberhaupt
  ein Intake entsteht): **Authenticate Sender** (SPF/DKIM, siehe
  Frage 1) faengt gefaelschte Absender ab, aber keine legitim
  versendete Werbung von echten Absendern - das filtert nur
  Spoofing, nicht Inhalt.

Quellen:

- Configuring Complaint Email Ingestion (QMS) -
  https://quality.veevavault.help/en/gr/61887102/
- Working with Complaint Email Ingestion (QMS) -
  https://quality.veevavault.help/en/gr/61887103/
- Configuring Complaint Intake & Promote to Complaint (QMS) -
  https://quality.veevavault.help/en/gr/928400/
- Using Complaint Intake & Promote to Complaint (QMS) -
  https://quality.veevavault.help/en/gr/28400/
- Configuring External Notifications (QMS) -
  https://quality.veevavault.help/en/gr/77672/
- Using External Notifications (QMS) -
  https://quality.veevavault.help/en/gr/77669/
- Configuring Complaint Intake Follow-Up (QMS), Limited Release -
  https://quality.veevavault.help/en/lr/1227595/
- Working with Complaint Intake Follow-Up (QMS), Limited Release -
  https://quality.veevavault.help/en/lr/1227594/
- Configuring Email to Vault -
  https://platform.veevavault.help/en/gr/74285/
- Email Processing -
  https://platform.veevavault.help/en/gr/74665/
- New in 26R3 Limited Release (Complaint Intake Follow-Up: Email
  Collaboration; Auto-Retry; Auto-Create Complaint Contacts) -
  https://rn.veevavault.help/en/lr/new-in-26r3/

---

## Frage 8 - Followup Evaluation: automatische Impact-Bewertung (26R3 LR)

**Frage:** Was passiert, wenn eine Antwort auf eine Rueckfrage neue,
sicherheits- oder qualitaetsrelevante Informationen enthaelt, obwohl
der zugehoerige Complaint schon promoted (und ggf. schon in
Bearbeitung oder geschlossen) ist?

**Antwort:** Dafuer liefert 26R3 Limited Release ein komplett neues
Objekt samt Automatik: **Followup Evaluation**. Ohne diese Funktion
muesste ein Bearbeiter manuell erkennen und nachverfolgen, dass eine
neu eingetroffene Rueckfrage-Antwort Auswirkungen auf einen bereits
erzeugten *Complaint* haben koennte.

### Ausloeser

Vault erzeugt einen *Followup Evaluation*-Record, sobald an einem
*Complaint Intake Follow-Up*-Record **beide** Bedingungen erfuellt
sind:

1. Das Feld *Latest Response Details* wird bei Erzeugung befuellt,
   oder bei einem bestehenden Record aktualisiert/befuellt.
2. Das Feld *Followup Evaluation Type* steht auf
   *Followup Evaluation Needed* (nicht auf *No Impact* - damit lassen
   sich z. B. reine Tippfehlerkorrekturen bewusst ausnehmen).

Zusaetzliche Bedingung: Der uebergeordnete *Complaint Intake* muss
bereits **mindestens einen** *Complaint* via *Promote to Complaint*
erzeugt haben. Ohne Promote entsteht keine *Followup Evaluation* -
konsistent mit dem Rest des Modells: Die Bewertung existiert nur in
Bezug auf bereits regulierte Faelle.

### Was automatisch passiert

- Vault legt **einen eigenen** *Followup Evaluation*-Record **pro
  verbundenem, aktivem Complaint** an - bei mehreren Complaints aus
  demselben Intake (z. B. durch *Split by Batch*) entsprechend
  mehrere. Stornierte (*Cancelled*) Complaints werden ausgenommen,
  **geschlossene jedoch nicht** - die Bewertung findet also auch nach
  Abschluss eines Complaints noch statt.
- Jeder *Followup Evaluation*-Record referenziert: den *Complaint*,
  den (urspruenglichen) *Complaint Intake* und den ausloesenden
  *Complaint Intake Follow-Up*.
- Felder *Response Date* und *Response Details* werden als
  Zeitpunkt-Schnappschuss aus *Latest Response Date* bzw.
  *Latest Response Details* des Follow-Up-Records uebernommen.
- Ein konfigurierbarer Workflow startet automatisch, weist dem
  *Complaint Owner* (ueber Quality Teams oder Dynamic Access Control
  zugewiesen) eine Pruefaufgabe zu und benachrichtigt die relevanten
  Personen.

### Einschraenkungen

- **Nicht unterstuetzt**, wenn das Vault Complaints ueber die
  *Quality Event*-Object-Types *Complaint* bzw. *MedTech Complaint*
  abbildet, statt ueber das eigenstaendige *Complaint*-Objekt. Fuer
  dieses Projekt ist also zuerst zu klaeren (siehe Frage 2, Schritt 1),
  welches Datenmodell genutzt wird - das entscheidet, ob diese Funktion
  ueberhaupt nutzbar ist.
- Erfordert Admin-Konfiguration: *Followup Evaluation Type*-Feld
  aktivieren und auf dem *Complaint Intake Follow-Up* Layout
  einblenden, Related-Object-Sections fuer *Followup Evaluation* auf
  *Complaint* und *Complaint Intake Follow-Up* (empfohlen auch auf
  *Complaint Intake*) ergaenzen, Rollenzuweisung per Quality Teams
  oder Dynamic Access Control konfigurieren, und bei Bedarf einen
  eigenen Bewertungs-Workflow bauen.
- Release-Stand: **26R3 Limited Release**, nicht General Release -
  dieselbe Einschraenkung wie beim uebrigen Follow-Up-Korrespondenz-
  Feature (siehe Frage 5, Stufe 2).

Quellen:

- New in 26R3 Limited Release (Complaint Intake Follow-Up Evaluation) -
  https://rn.veevavault.help/en/lr/new-in-26r3/
- Configuring Complaint Intake Follow-Up (QMS), Limited Release -
  https://quality.veevavault.help/en/lr/1227595/
- Working with Complaint Intake Follow-Up (QMS), Limited Release -
  https://quality.veevavault.help/en/lr/1227594/

---

## Frage 9 - Auto-Retry fuer unbeantwortete Rueckfragen (26R3 LR)

**Frage:** Lassen sich unbeantwortete Rueckfragen automatisch
wiederholen, statt dass ein Bearbeiter das manuell nachverfolgen muss?

**Antwort:** Ja, ueber das 26R3-LR-Feature **Complaint Intake
Follow-Up: Auto-Retry** - ein Admin-konfigurierter, planmaessig
laufender Job (typischerweise stuendlich), der unbeantwortete
Follow-Ups automatisch erneut anstoesst.

### Steuerfelder am *Complaint Intake Follow-Up*

| Feld | Bedeutung |
| --- | --- |
| *Retry?* | Muss auf *Auto* stehen, damit der Job den Record ueberhaupt aufgreift. |
| *Retry Frequency* | Abstand in Tagen zwischen zwei automatischen Versuchen. |
| *Retry Due On* | Datum, an dem der naechste automatische Versuch faellig ist. |
| *Remaining Retries* | Verbleibende automatische Versuche; sinkt bei jedem Auto-Retry um 1. |

### Ablauf

1. Der Job prueft periodisch *Complaint Intake Follow-Up*-Records
   gegen vom Admin konfigurierte Bedingungen (u. a. erlaubte
   *Contact Methods*, zulaessige Status von Follow-Up **und**
   zugehoerigem *Complaint Intake*, optional ein
   *Previous Attempt End State*).
2. Bei Treffer legt Vault einen **neuen** *Complaint Intake
   Follow-Up*-Record mit denselben Daten wie der Vorversuch an - das
   ist der naechste Versuchs-Record, kein Update des alten.
3. Optional (**Auto-Send External Email**) verschickt der Job dazu
   automatisch eine Email an dieselben Complaint Contacts wie beim
   Erstversand.
4. Scheitert der Versand, setzt Vault den neuen Follow-Up-Record auf
   Status *Error* und schreibt die Ursache in *Error Message*.
5. Trifft waehrenddessen doch noch eine Antwort ein, beendet Vault den
   Retry-Zyklus automatisch: *Retry Rule* wird auf *None* und
   *Retry Due On* geleert.

### Einschraenkungen

- Dokumentanhaenge werden im Auto-Retry **nicht** unterstuetzt - nur
  Links in der Email moeglich.
- Auto-Retry unterstuetzt fuer *Internal Recipients* und
  *Role Recipients* nur **CC**: war der Erstversand an diese
  Empfaenger als BCC adressiert, gehen automatische Wiederholungen an
  sie als CC statt BCC raus - eine stille Verhaltensaenderung, die vor
  Go-Live zu pruefen ist.
- Fuer manuelles statt automatisches Nachfassen (*Retry?* = *Manual*)
  laesst sich stattdessen ein eigener Job plus Statuswechsel auf
  *Retry Due* und eine Benachrichtigung bei diesem Statuswechsel
  konfigurieren.
- Release-Stand: **26R3 Limited Release**.

Quellen:

- New in 26R3 Limited Release (Complaint Intake Follow-Up: Auto-Retry) -
  https://rn.veevavault.help/en/lr/new-in-26r3/
- Configuring Complaint Intake Follow-Up (QMS), Limited Release -
  https://quality.veevavault.help/en/lr/1227595/
- Working with Complaint Intake Follow-Up (QMS), Limited Release -
  https://quality.veevavault.help/en/lr/1227594/

---

## Aenderungsprotokoll 26R3-Abgleich (2026-11-05)

Nachdem der Vault-Documentation-MCP-Server wieder erreichbar war,
wurde dieses Dokument komplett gegen die aktuelle Veeva-Doku (General
Release und 26R3 Limited Release) geprueft. Uebersicht aller
inhaltlichen Aenderungen:

| Stelle | Vorher | Jetzt | Status |
| --- | --- | --- | --- |
| Frage 2, Schritt 4 (Rechte) | Pauschal *Read* auf *Email*, *Person*, *Complaint*, *Complaint Intake*, *Quality Event* | Objektscharf: *Complaint Intake Email* / *Complaint Intake Sent Notif* bzw. *Complaint Email* / *Complaint Sent Notification*, je nach Zielobjekt | Korrigiert |
| Frage 3, Contact-Erzeugung | "Doku sagt nicht zu, ob automatisch" | Automatisch moeglich via *Auto-Create Complaint Contacts* (26R3 LR), zwei Checkboxen an der Inbound Email Address Configuration, Object Type *Email Contact* noetig | Offene Frage beantwortet |
| Frage 5, Stufe 2, Empfaenger | Pauschal *Initial Reporter* | Primaer Feld *Primary Contact* am Follow-Up, Fallback *Initial Reporter* | Korrigiert |
| Frage 5, Follow-Up-Tracking | Nur allgemein *Quality Event Sent Notification* erwaehnt | Eigenes Objekt *Complaint Intake Followup Sent Notif* fuer Follow-Up-spezifisches Tracking, inkl. Rechte-Detail | Ergaenzt |
| Frage 6, Objekttabelle | Kein *Followup Evaluation*, kein *Complaint Intake Followup Sent Notif*, *Email Contact* nicht erwaehnt | Beide Objekte ergaenzt, *Complaint Contact* Object Type *Email Contact* ergaenzt | Ergaenzt |
| Frage 6, Kernverknuepfungen | 6 Verknuepfungen | 7. Verknuepfung *Complaint Intake Follow-Up -> Followup Evaluation* ergaenzt | Ergaenzt |
| Neu: Frage 8 | nicht vorhanden | *Followup Evaluation* (automatische Impact-Bewertung, 26R3 LR) komplett neu dokumentiert | Neu |
| Neu: Frage 9 | nicht vorhanden | *Auto-Retry* fuer unbeantwortete Rueckfragen (26R3 LR) komplett neu dokumentiert | Neu |
| Release-Stand 26R3 insgesamt | Als Limited Release markiert | **Bestaetigt weiterhin Limited Release**, nicht General Release (Konfigurationsartikel liegen weiterhin nur unter `/lr/`-Pfaden) | Bestaetigt, keine Aenderung |
| Diagramm | Objektmodell ohne Followup Evaluation | *Followup Evaluation* und *Complaint Intake Followup Sent Notif* als Knoten ergaenzt | Ergaenzt (siehe [veeva-complaint-email-object-model.drawio](veeva-complaint-email-object-model.drawio)) |

**Nicht veraendert** (durch den Abgleich bestaetigt, keine
Abweichung zur bisherigen Doku gefunden): Fragen 1, 2 (ausser der
genannten Rechte-Praezisierung), 4, 7 sowie alle uebrigen Aussagen in
Frage 3 und Frage 5.
