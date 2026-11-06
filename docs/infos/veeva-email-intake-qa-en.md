# Veeva Vault Email Intake - Questions & Answers

Log of questions about Veeva Vault "Email to Vault" / Email Intake.
Answers are based on the official Veeva Vault Platform Help
(General Release). As of: 2026-10-27. Questions 4 and 5 additionally
draw on the 26R3 Limited Release documentation; this is marked where
it applies.

> **Update 2026-11-05 (part 1):** Questions 6 and 7 and the object-model
> diagram were added. A cross-check against the current live
> documentation (via the Vault Documentation MCP server) was attempted,
> but the server was unreachable at the time of this update (connection
> error). The content was therefore still based on the state already
> captured in questions 1-5 (26R2 General Release / 26R3 Limited
> Release).
>
> **Update 2026-11-05 (part 2) - 26R3 cross-check completed:** The MCP
> server was reachable this time; every question was checked against
> current General and Limited Release documentation. Result: all prior
> release assignments (26R2 GR / 26R3 LR) were correct, and 26R3 is
> still **not** General Release as of this update. New or corrected
> (each marked **[26R3 cross-check 2026-11-05]**):
>
> - New object/process **Followup Evaluation** (automated impact
>   assessment when new follow-up information arrives, 26R3 LR) - see
>   [Question 8](#question-8---followup-evaluation-automated-impact-assessment-26r3-lr).
> - New feature **Complaint Intake Follow-Up: Auto-Retry** (automatic
>   resending of unanswered follow-up requests, 26R3 LR) - see
>   [Question 9](#question-9---auto-retry-for-unanswered-follow-ups-26r3-lr).
> - New feature **Complaint Email Ingestion: Auto-Create Complaint
>   Contacts** (26R3 LR) - this answers the question left open in
>   Question 3, whether *Complaint Contact* records are created
>   automatically from the inbound email: **yes**, when configured.
> - Correction in Question 5: the recipient of a follow-up reply is
>   primarily the *Primary Contact* field on the follow-up record, not
>   unconditionally the *Initial Reporter*.
> - Permission details in Question 2 were made more precise
>   (object-specific names rather than generic ones: *Complaint Intake
>   Email* / *Complaint Intake Sent Notif* vs. *Complaint Email* /
>   *Complaint Sent Notification*).
>
> A full before/after changelog is at the end of this document under
> [26R3 cross-check changelog](#26r3-cross-check-changelog-2026-11-05).

German original: [Veeva Email Intake QA.md](<Veeva Email Intake QA.md>)

---

## Question 1 - Who may send email to the intake?

**Question:** Who can send emails to the intake? Can this be anyone, or
does the sender address have to be known to Vault as an allowed sender?

**Answer:**

This is configurable. Every *Inbound Email Address* (Admin >
Configuration > Inbound Email Addresses) has a mandatory
**Allowed Senders** field. Vault only accepts a message if the sender
address matches the selected group - otherwise the message is rejected
and stored as an *Email* record in *Bounced* / *Failed* state.

Options for **Allowed Senders**:

| Option | Who may send |
| --- | --- |
| All Users & Persons in this Vault | Any address attached to a *User* or *Person* record |
| All Users in this Vault | Only addresses attached to *User* records |
| Specific Groups | Only *User* addresses from 1-5 selected *Allowed Sender Groups* |
| Anyone | Any sender (referenced only indirectly in the docs, via Email Processor User) |

Practical consequences:

- Default expectation: the sender must be known to Vault (as *User* or
  *Person*). Arbitrary external senders only work with "Anyone".
- Externals without a Vault login can be covered through *Person*
  records, without consuming a licence.
- With "Anyone" or "All Users & Persons" an **Email Processor User**
  can be set - processing runs as that user when the sender is not a
  Vault user, and the audit trail attributes the actions to them.
- **Always Run as Email Processor User** forces that user even when
  the sender is a Vault user.
- **Authenticate Sender** (optional, recommended) validates SPF and
  DKIM and thus prevents sender spoofing. It can only be disabled for
  certain application-provided processors and doing so is risky.
- Recommended route for corporate addresses: auto-forward / redirect
  from an address in your own domain to the
  `<name>@<subdomain>.veevavault.com` address. Most enterprise mail
  systems preserve the original sender, so the allowed-sender check
  still evaluates the real person.

Related constraints:

- Max. 250 inbound email addresses per Vault.
- Max. 40 MB per email including attachments (applies to .EML, not
  .MSG).
- A test mail with subject `Email to Vault Test` only creates an
  *Email* record without running the processor.

Sources:

- Configuring Email to Vault -
  https://platform.veevavault.help/en/gr/74285/
- Email Processing -
  https://platform.veevavault.help/en/gr/74665/

---

## Question 2 - Receiving complaints from unknown senders

**Question:** We want to receive and process complaints. Therefore the
sender addresses are not known to us. How can such emails be received?

**Answer:**

Vault QMS provides exactly this capability: **Complaint Email
Ingestion**. The setup has two parts: opening up sender acceptance,
and configuring the QMS *Create Complaint* processor.

### 0. What "Complaint Email Ingestion" actually is

Not a separate product and not something to purchase, but a
**standard Vault QMS feature** already included in IQMS that only
needs to be configured. It consists of three parts:

1. **A mailbox owned by Vault.** Vault gets a real email address of
   the form `complaints@<subdomain>.veevavault.com` - the *Inbound
   Email Address*. You publish that address externally, or forward a
   Bayer address to it.
2. **An email processor called `Create Complaint`.** An email
   processor in Vault is the logic that decides what happens to an
   incoming message. Veeva ships several: the generic *Create
   Document from Email* turns the message into an unclassified
   document, while the QMS-specific *Create Complaint* creates a
   *Complaint* or *Complaint Intake* record instead. One processor is
   selected per mailbox.
3. **A mapping from email to object fields.** The processor parses
   the message and writes sender, subject, date, body and attachments
   into defined fields on the record (see the mapping table below).
   The original message as `.EML` and all attachments go into the
   Attachments section.

The flow in one sentence: a customer writes to
`complaints@...veevavault.com`, Vault accepts the message,
*Create Complaint* automatically produces a record with all data and
attachments, and a processor sees it in their triage list - with
nobody retyping or uploading anything.

Why this answers the question asked: the generic route assumes the
sender is known to Vault. Complaint Email Ingestion is Veeva's
intended exception, built for reports from outside. That is why it
has the *Email Processor User* (someone has to create the record when
the sender is not a Vault user), thread detection (follow-up
questions and replies belong to the same case) and the *Complaint
Intake* stage (triage unvetted input first).

For contrast: without this feature you could still receive email, but
it would only produce unclassified documents - no complaint record,
no field population, no QMS process. Everything else would have to be
built in-house.

### 1. Opening up sender acceptance

On the *Inbound Email Address*:

- **Allowed Senders** = *Anyone*. This removes the check against
  *User*/*Person* records, so arbitrary complainants can send.
- An **Email Processor User** then becomes mandatory in practice:
  processing runs and is audited under this service user because the
  sender is not a Vault user. It needs *Read* on *Email*, *Person*,
  *Complaint*, *Complaint Intake*, *Quality Event*, plus Create/Edit
  on the target object.
- Keep **Authenticate Sender** (SPF/DKIM) enabled. With an open inbox
  it is the only protection against spoofing. Veeva only allows
  disabling it for certain application-provided processors and warns
  explicitly against it.
- Alternative if "Anyone" is organisationally unacceptable: operate a
  Bayer address (e.g. `complaints@bayer.com`) as the public contact
  address and **auto-forward** it to the
  `...@<subdomain>.veevavault.com` address. The original sender is
  preserved; access control then sits with the Bayer mail system
  (spam / malware filtering) rather than with Vault. Caveat:
  forwarding can break SPF/DKIM - the forwarder must support
  SRS/ARC, otherwise *Authenticate Sender* fails.

### 2. Configuring Complaint Email Ingestion

- Create a dedicated *Inbound Email Address* per complaint type and
  select the **Create Complaint** email processor there.
- For each address create an **Inbound Email Address Configuration**
  (Admin > Configuration > Inbound Email Address Configurations)
  with: Label, Status (Inactive = no complaints are created),
  Inbound Email Address, target object (*Complaint*, *Complaint
  Intake* or *Quality Event*) and Object Type.
- **Email Thread Detection**: *Match on Message ID* (default) or
  *Match on Root Message ID*. Reporter replies then attach to the
  existing record instead of creating a new one.
- Optionally disable: body/text parsing, and email/attachment
  parsing.
- The **Email Body** section or field must be added to the page
  layout of the *Complaint Email* object type.

### 3. Recommendation for unknown senders: Complaint Intake

For a public inbox the target object should be **Complaint Intake**
rather than *Complaint* directly. *Complaint Intake* is designed as a
triage stage: potential complaints are captured and only promoted to
real *Complaint* records after review. This catches spam and
misdirected mail before it enters the regulated complaint process.

### Automatic field population

| Email | Field on Complaint / Complaint Intake |
| --- | --- |
| Original sender | `initial_reporter_details__v` |
| From address | `sender_email_address__v` |
| Sent date | `initial_report_date__v` |
| Subject | `title__v` (150 characters by default) |
| Body | `email_body__v` (rendered, up to 32,000 characters) |
| Body as text | `email_text__v` |
| Attachments | Attachments section, original .EML plus files |
| Metadata | `initial_contact_method__v` = `email__v`, `vault_email_inbox_address__v`, `message_id__v`, `root_message_id__v` |

### 4. Step-by-step configuration guide

Keep the order: the data objects must exist before the mailbox can
reference them. All steps are performed in Vault under **Admin**,
first in DEV/sandbox, then migrated to QA/PROD.

**Step 1 - Determine the complaint data model.**
Establish whether the Vault uses the standalone *Complaint* object or
*Quality Event* with object type *Complaint*. Every following step
depends on this. If unclear, check Admin > Configuration > Objects.

**Step 2 - Activate and set up the *Complaint Intake* object.**
(The recommended triage stage for unknown senders.)

1. **Activate the object type** - *Complaint Intake* for pharma, or
   *MedTech Complaint Intake* for medtech.

   "Activate" here does **not** mean create: both object types ship
   as part of the standard QMS data model but have status
   *Inactive*. While an object type is inactive, neither users nor
   the email processor can create records of that type. Click path:

   1. **Admin > Configuration > Objects > Complaint Intake**.
   2. Open the **Object Types** tab. If that tab is missing, object
      types are not yet enabled on the object: go to **Details >
      Edit >** tick **Enable Object Types** **> Save**. Vault then
      creates the base type automatically and shows the tab.
   3. Open the desired object type via its label.
   4. Click **Edit**, set **Status** to *Active*, click **Save**.

   If the required object type is unexpectedly absent, it can be
   created in the same tab via **Create** (Label, Plural Label,
   optionally Name/Description, Status). A maximum of 50 object
   types per object applies.

2. **Activate object fields and assign them to the object type** -
   every field the target complaint object type requires as
   mandatory. Otherwise *Promote to Complaint* will fail later.

   Again, two distinct things:

   - *Activating a field*: Admin > Configuration > Objects >
     [Object] > **Fields**, open the field, **Edit**, set status to
     *Active*, **Save**.
   - *Assigning a field to the object type*: **Object Types** tab >
     Actions menu > **Edit Object Type Fields**. Vault shows a
     matrix of object types and fields; tick the relevant checkboxes
     and **Save**.

   Notes: fields marked mandatory at object level automatically
   apply to all object types and cannot be deselected there. Newly
   created fields are initially assigned to the base type only and
   must be assigned manually.

3. Create a page layout for the object type.
4. **Important:** add the special **Email Body** section or field to
   the layout. Without it the email content is not visible on the
   record.
5. Extend the layout with related-object sections: created
   *Complaints*, *Reported Products*, optionally *Complaint Contacts*
   and *Complaint Intake Follow-Ups*.
6. Optional: create a dedicated *Complaint Intake* tab so the triage
   list is easy to reach.
7. Configure Quality Teams for *Complaint Intake*.

**Step 3 - Prepare the target complaint object.**
On the *Complaint* or *Quality Event Complaint* layout, expose the
**Complaint Intake** field. Only when that reference is populated
will the complaint display contacts, follow-ups and their
attachments.

**Step 4 - Create the service user for processing.**
Create a dedicated *Email Processor User* (not a personal account).
Required permissions per current documentation
**[26R3 cross-check 2026-11-05 - made more precise; previously only
generic "Complaint"/"Quality Event" names were given]**:

- *Read* on *Email*.
- If the target object is *Complaint Intake*: additionally *Read* on
  *Complaint Intake Email* and *Complaint Intake Sent Notif*, plus
  *Edit* and *Create* on *Complaint Intake*.
- If the target object is *Complaint* (or the *Complaint* object type
  of *Quality Event*): additionally *Read* on *Complaint Email* and
  *Complaint Sent Notification*, plus *Edit* and *Create* on the
  respective target object/object type.
- *Complaint Intake Email* / *Complaint Email* are the object-type-
  specific variants of the generic *Email* record for the respective
  ingestion path; *Complaint Intake Sent Notif* / *Complaint Sent
  Notification* are the tracked-email records for outbound
  notifications (separate from *Complaint Intake Followup Sent
  Notif*, see question 5).

**Step 5 - Create the Inbound Email Address.**
Admin > Configuration > Inbound Email Addresses > **Create**, one per
complaint type:

1. Set **Name** and **Label**.
2. **Email Address**: the local part only; the full address becomes
   `<name>@<vault-subdomain>.veevavault.com`.
3. **Email Processor**: *Create Complaint*.
4. **Allowed Senders**: *Anyone* (this is the core of the solution
   for unknown senders).
5. **Email Processor User**: the service user from step 4.
6. Enable **Always Run as Email Processor User** so processing runs
   consistently under the service user even for incidentally known
   senders.
7. Keep **Authenticate Sender** enabled (SPF/DKIM).
8. Decide **Send Bounce Notification** deliberately - with a public
   inbox Vault would otherwise reply to arbitrary addresses.

**Step 6 - Test the first mailbox before continuing.**
The *first* inbound email address in a Vault takes several hours to
become active. Send a test mail with the exact subject
`Email to Vault Test`: Vault creates only an *Email* record and does
not run the processor. Once that record appears, the address is
ready. Subsequent addresses are usable immediately.

**Step 7 - Create the Inbound Email Address Configuration.**
Admin > Configuration > Inbound Email Address Configurations >
**Create**, one per address:

1. Set a **Label**.
2. **Status**: start as *Inactive* - while inactive Vault creates no
   records. Switch to *Active* only after the end-to-end test.
3. Select the **Inbound Email Address** (the list only shows
   addresses not already bound to another configuration; the
   processor is filled in automatically).
4. **Object**: *Complaint Intake* (recommended), alternatively
   *Complaint* or *Quality Event*.
5. Select the **Object Type** - this type is created per email.
6. **Email Thread Detection**: *Match on Message ID* (default) or
   *Match on Root Message ID* if the whole thread should map to one
   case.
7. Only set the parsing options if body or attachments should
   deliberately not be carried over - for complaints normally leave
   both enabled.
8. **Save**.

**Step 8 - Configure Promote to Complaint.**
On the *Complaint Intake* lifecycle, set up the *Promote to
Complaint* action - as a user action, entry action or workflow step:

- Select the **Object Type** of the *Complaint* to be created.
- **Split by Batch** optional (off by default): creates one complaint
  per product/batch combination.
- **Copy Attachments** optional (on by default).
- The action runs **once only** per intake record; a second
  invocation produces a system error.
- Before it runs, every mandatory field of the *Complaint* must be
  populated on the intake and *Reported Product* records.

**Step 9 - Test end to end.**
Set the configuration to *Active* and send a mail with an attachment
from an external address (deliberately one Vault does not know).
Verify: the intake record is created, fields are populated, the .EML
and attachments are in the Attachments section, a reply to the same
mail does not create a second record, and *Promote to Complaint*
produces the complaint.

**Step 10 - Migrate to QA/PROD.**
Transfer the configuration via VPK / migration package.
**The email address differs per Vault**
(`<name>@<subdomain>.veevavault.com`) - in each environment the
address must be created anew and the externally communicated address
or auto-forwarding set accordingly.

### Limits and failure behaviour

- Max. 40 MB per email including attachments.
- Max. 50 attachments per record; anything beyond is dropped and the
  sender receives a warning.
- Same file name with different content creates a new attachment
  version.
- A body over 32,000 characters is truncated in the field; the full
  content is only in the .EML attachment.
- Failures notify the sender via
  `qms_email_processing_failed__v`, partial success via
  `qms_email_processing_warning__v`. With a public inbox this means
  Vault replies to potentially arbitrary addresses - confirm this is
  acceptable beforehand.
- The generic *Create Document from Email* processor does not support
  encrypted emails.

Sources:

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

## Question 3 - Follow-up email from a Complaint Intake

**Question:** Can I send a follow-up email to the sender from within
Vault on a Complaint Intake? It may happen that not all relevant data
is present and a follow-up question has to be asked.

**Answer:**

Yes. The feature is **Quality External Notifications** with the
*Send External Notification* action, and *Complaint Intake* is
explicitly one of the supported objects. Veeva names this very use
case as an example: correspondence to the reporter or complainant
during the complaint and complaint intake process.

### Important distinction: not Complaint Intake Follow-Up

Tempting but wrong: the *Complaint Intake Follow-Up* object sounds
like the follow-up mechanism but **does not send email**. It serves
purely as manual documentation: the processor follows up through
whatever channel they choose and then records the request as a
follow-up record. Veeva states that external notification support for
this object is planned for a future release.

This implies a configuration warning: several fields on the
*Complaint Intake Follow-Up* object already exist but are intended
for a future release and must not be used yet - among them *Email
Body Custom Text*, *Email Sent?*, *Email Subject Custom Text*,
*From*, *Reply To*, *Send Email on Create?*, *Complaint Contacts*,
*Email Template*. Veeva recommends hiding them via permissions, along
with the *Auto* value on the *Retry?* field.

So the sending mechanism is External Notifications; the follow-up
object is only the documentation trail alongside it.

> **Update (as of 2026-10-27):** This section describes the General
> Release. With **26R3 Limited Release** (feature *Complaint Intake
> Follow-Up: Email Collaboration*) the opposite holds: *Complaint
> Intake Follow-Up* becomes the central correspondence object with
> genuine two-way email. See
> [Question 4](#question-4---templates-for-replies-filling-them-in-review-before-sending)
> and [Question 5](#question-5---can-replies-to-a-follow-up-be-mapped-to-an-intake).

### Prerequisite: Complaint Contacts, not Person

*Complaint Intake* has a peculiarity that is easily missed:

| Object | Person | Complaint Contact |
| --- | --- | --- |
| Complaint Intake | not supported | **required** |
| Complaint / Quality Event Complaint | optional | optional |
| Complaint Intake Follow-Up (future) | not supported | required |
| all other objects | required | not supported |

The recipient of a follow-up from an intake is therefore **always a
*Complaint Contact* record**, never a *Person* record. That fits the
unknown-sender scenario: the reporter does not have to be created as
a *Person* in the Vault.

For a contact to be contactable at all, three fields must be right:

- *Consent to Contact* = **Yes**
- *Email* = a valid address
- *Status* = **Active**

Further rules: only **one** contact of object type *Initial
Reporter* is allowed per intake. Either *First Name* or *Last Name*
is required. Parentheses or an email address inside the name field
prevent delivery - a documented trap.

**[26R3 cross-check 2026-11-05 - answers a question left open
before]** Whether the contact is created automatically from the
inbound email was not documented at General Release level. With the
26R3 Limited Release feature **Complaint Email Ingestion:
Auto-Create Complaint Contacts**, this is now clearly answered: yes,
when configured. The *Inbound Email Address Configuration* for the
*Complaint Intake* target object provides two checkboxes for this:

- **Create Initial Reporter Contact from sender email**: creates a
  *Complaint Contact* of object type *Initial Reporter* from the
  original sender, if the intake does not already have one.
- **Create additional Complaint Contacts from To/CC emails**: creates
  a *Complaint Contact* of object type *Email Contact* for each
  additional address in the To/CC fields.

Prerequisite on the *Complaint Contact* object: the *Email Contact*
object type must be activated (Admin > Configuration > Objects >
Complaint Contact > Object Types). Without the 26R3 LR feature, or
without activation, General Release behaviour applies: the *Create
Complaint* processor only populates `initial_reporter_details__v`
and `sender_email_address__v` as text fields on the intake record,
and creating the structured *Complaint Contact* record is then a
manual or action-trigger task. **Verify in DEV which mode is active**,
otherwise sending follow-ups becomes a manual step in operation. To
simplify it, action triggers can populate contacts from a *Master
Complaint Contact*.

### Configuration in brief

1. **Create the action:** on the *Complaint Intake* object,
   **Actions > Create > Send External Notification > Continue >
   Save**. Do **not** tick *Available in All Lifecycle States* - the
   action does not work correctly with it. Optionally also create
   *Create Distribution Group Memberships*.
2. **Extend the layout:** add the *Notification Recipients* section
   and a *Complaint Contacts* related-object section to the intake
   layout. Optionally add *Sent Notification* as a related object to
   see sent messages on the record.
3. **Create an object message template** for the follow-up text.
   Note: replace the token prefix `Object` manually with `Custom`,
   i.e. `${Object.name__v}` -> `${Custom.name__v}`. For `Custom`
   tokens `name__v` is limited to 40 characters, and formula fields
   are not supported.
4. **Create a Quality External Notification:**
   Admin > Configuration > Quality External Notifications >
   **Create**, select object *Complaint Intake*.
5. **Add a notification template:** here select **Complaint Contact
   Types** instead of the *Recipients* field - e.g. *Initial
   Reporter*. This is where the follow-up is addressed to the
   reporter.
6. **Anchor the action in the lifecycle:** *Send External
   Notification* as a user action on a state such as "follow-up
   pending", or as an entry/event action if it should go
   automatically.

### Operational flow

The processor opens the intake record, runs **Send External
Notification**, selects the follow-up template, adjusts recipients if
needed (with complaint contacts the field is labelled *Complaint
Contacts* rather than *Additional Recipients*), can inspect the mail
under *Preview Email*, and sends.

### The key point: the reply comes back into the record

When the reporter replies to the follow-up, the email processor
recognises via message ID or root message ID that a record already
exists. Vault then does **not** create a new intake but attaches the
reply to the existing record. The loop closes automatically -
provided the *Email Thread Detection* configured in question 2,
step 7 is in place.

### Further useful options

- **Tracked emails:** for *Complaint* and *Complaint Intake*, Vault
  tracks delivery status and stores it in *Email* and *Quality Event
  Sent Notification* records - reportable, so it can drive chasing
  when no answer arrives. **[26R3 cross-check 2026-11-05]** For
  sending/receiving specifically through *Complaint Intake Follow-Up*
  there is a dedicated tracking object: *Complaint Intake Followup
  Sent Notif* (the *Complaint Intake Follow-Up Email Processor* needs
  *Read* permission on it, see question 5).
- **Reply To:** add the field to the layout so replies reach the
  right person. Caveat: some mail clients ignore Reply-To.
- **From:** the sender of the follow-up can be controlled; requires
  configured and verified *Outbound Email Domains* and *From Email
  Address Persons* - relevant for using a Bayer sender address rather
  than `veevavault.com`.
- **Communication Language:** the field can be activated so
  follow-ups go out in the reporter's language; requires templates in
  every language (bulk translation under Admin > Settings > Language
  & Region Settings).
- **Do Not Include Headers and Footers:** can be deselected for
  complaint object types if the standard Vault header should not go
  out externally.
- **Sending documents:** either as a link into an external viewer or
  as a real attachment (the latter requires an application setting).

### Limitation on automatic sending

If *Send External Notification* is configured as an entry or event
action and a recipient is skipped (missing email, inactive, *Consent
to Contact* blank or *No*), the action continues for the remaining
recipients - but **no sent-notification record is created for the
skipped ones**. There is then no trace that someone was not reached.
For mandatory follow-ups, prefer a user action plus a check.

Sources:

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

## Question 4 - Templates for replies, filling them in, review before sending

**Question:** Can replies be pre-formulated, i.e. can templates be
stored, filled in, and the email put through a review before it is
sent?

**Answer in one sentence:** Templates yes, filling them in depends on
the release, and a genuine four-eyes review of the concrete email is
**not a standard feature** - it has to be built via the lifecycle or
via an approved Vault document.

The three parts of the question separate cleanly:

| Sub-question | Answer |
| --- | --- |
| Store templates | Yes, standard (object message templates per notification template), any number, multilingual |
| Fill the template in | Token merge always; **free text** only from *Complaint Intake Follow-Up* and only from 26R3 LR |
| Review before sending | Self-check only (*Preview Email*). No approval step on the email; only indirectly via lifecycle or document |

### 1. Storing templates - yes, standard

The follow-up text lives as an *Object Message Template* and is
referenced by a *Notification Template* inside the *Quality External
Notification*. Any number of templates can be created per object; a
user action can offer several of them and the processor picks one
when sending. Translations run via *Communication Language* and bulk
translation.

Templates can contain tokens (prefix `Custom` rather than `Object`)
and thus merge record field values - reporter name, complaint number,
product. That is "filling in" in the automated sense.

### 2. Adding free text - release-dependent

This is the actual constraint:

- **General Release (26R2, currently in production):** In the *Send
  External Notification* dialog the processor can adjust
  **recipients and documents**, but **not subject or body**. The mail
  text is exactly what the template produces after token merge.
  Individual questions ("please send the batch number and a photo of
  the damage") therefore either need their own template, or have to
  be entered into a field on the record that the template pulls in
  via a token. The latter is the usual workaround.
- **From 26R3 Limited Release (feature *Complaint Intake Follow-Up:
  Email Collaboration*, shipped with 26R2.3):** From a *Complaint
  Intake Follow-Up* record the action opens a dialog in which the
  processor can **freely enter subject and body** while the
  boilerplate text of the selected template is preserved. Plus
  To/CC/BCC and documents. This is the capability closest to what the
  question asks for.

This also changes the statement in question 3: *Complaint Intake
Follow-Up* is **no longer** merely a documentation object. From
26R3 LR it is the actual correspondence object with two-way email.

### 3. Review before sending - not a standard feature

Vault QMS has **no "email in review" state** and no approval on the
individual message. What does exist:

- **Preview Email** (26R2): the *Allow user to preview email?*
  checkbox on the *Send External Notification* **user action** (there
  only, not on entry/event actions). The dialog then shows the full
  HTML rendering with merged tokens and, where applicable, the
  translated template. This is a **self-check by the sender**, not a
  second pair of eyes. Known limits: links and document tokens are
  partly not rendered correctly in the preview, although they are in
  the sent mail.

Anyone who needs a genuine review has three viable routes:

**Route A - approval via the lifecycle (lightweight).**
*Send External Notification* is made available as a **user action in
one specific state only**, e.g. *Follow-up approved*. Ahead of it
sits a workflow step "review follow-up" on the *Complaint Intake* or
*Complaint Intake Follow-Up*. The reviewer sees the intended text -
in the free-text variant in *Latest Email Body Text* or a draft
field, in the template variant in the template itself - and moves the
state on. Only then does the action appear.
Caveat: whatever the processor types into the dialog from 26R3 on
goes out unreviewed. The lifecycle secures the timing and the
template choice, not the free text.

**Route B - send an approved document (regulatory clean).**
The substantive part is authored as a **Vault document**
(correspondence letter, questionnaire) and runs through the normal
document lifecycle with review and approval. The email itself remains
a short, immutable covering note from the template; the approved
document goes out as a link into an external viewer or - from 26R2 -
as a real attachment (application setting *Enable Document
Attachments on External Notifications*, max. 5 attachments,
15,360 KB total).
This is Veeva's intended route for content that needs approval, and
the only one with a clean approval audit trail.

**Route C - combination.** Lifecycle gate for the send timing,
approved document for the content requiring approval, template for
the frame. For a regulated complaint process this is the realistic
target architecture.

### Consequence for the project

If "review before sending" is a hard requirement, the follow-up text
must not be composed freely in the dialog. Either it is fully
pre-formulated in the template (in which case the template is
reviewed once as a configuration object, not every mail), or the
part requiring approval moves into an approved document. This needs
to be fixed as an `FR-` or an ADR before the lifecycle configuration
is built.

Sources:

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

## Question 5 - Can replies to a follow-up be mapped to an intake?

**Question:** Can replies to a follow-up question be mapped concretely
to a Complaint Intake object?

**Answer:** Yes. The mapping runs automatically via the email headers
(message ID / root message ID), not via text search or manual
linking. There are two maturity levels with different granularity.

### Level 1 - mapping to the Complaint Intake (General Release)

For every incoming message the *Create Complaint* email processor
checks the **message ID and References in the header**. If it finds
an existing *Complaint* or *Complaint Intake* record from that
thread, it creates **no new record** but attaches the reply to the
existing one. This explicitly covers replies to an external
notification sent from Vault.

It is controlled by *Email Thread Detection* on the *Inbound Email
Address Configuration*:

- *Match on Message ID* (default) - mapping via the individual
  message.
- *Match on Root Message ID* - mapping across the whole thread. If
  several records share a root message ID, Vault takes the **most
  recently created** one.

Granularity at this level: the reply lands on the right **intake**.
Which specific follow-up question was answered is not machine-readable
from it.

### Level 2 - mapping to the individual follow-up (26R3 LR)

With *Complaint Intake Follow-Up: Email Collaboration* (26R3 Limited
Release, shipped with 26R2.3) the mapping becomes finer: not just to
the intake, but to the **individual follow-up record**, i.e. the
specific question.

Mechanics:

1. The follow-up goes out from a *Complaint Intake Follow-Up* record;
   Vault creates one *Complaint Intake Follow-Up Email* record per
   send, with *Direction* = *Outbound*. **[26R3 cross-check
   2026-11-05 - correction]** The recipient (*To* field) is primarily
   the *Primary Contact* field on the follow-up record itself; if
   none is set there, Vault falls back to the *Complaint Contact* of
   object type *Initial Reporter* on the associated *Complaint
   Intake*. So it is **not** unconditionally the Initial Reporter, as
   earlier versions of this document implied. Also selectable: *CC
   Contacts*, *Internal Recipients* (Person records, optionally as CC
   or BCC), and *Documents to Send*.
2. The **Reply-To** points at a mailbox in the **Bayer mail system**,
   not directly at Vault.
3. The reporter's reply is **auto-forwarded** from there (explicitly
   **not** redirected) to a second inbound email address using the
   **Complaint Intake Follow-Up Email Processor**.
4. The processor matches on the **root message ID** - this setting is
   **mandatory** here, not optional - and attaches the reply to the
   right follow-up record.

What gets populated automatically:

| Field on *Complaint Intake Follow-Up Email* | Field on *Complaint Intake Follow-Up* |
| --- | --- |
| *Complaint Intake Follow-Up* (reference) | - |
| *Direction* = *Inbound* | - |
| *Subject* | - |
| *Email Body Text* | *Latest Email Body Text*, optionally *Latest Response Details* |
| *Email Body* (HTML, via *View Email*) | *Latest Email Body* |
| *Received Date* | *Latest Response Date* |
| *Original Sender Email* | - |

In addition: attachments on the reply are copied to the follow-up and
are visible through the *Follow-Up Attachments* section on the intake
and on every complaint created from it. The follow-up record's state
changes automatically. If several replies arrive for one follow-up,
**each reply becomes its own email record**. The processor can reply
directly via *Send Email Reply* - genuine two-way correspondence
inside the record.

Optional: *Create Complaint Contact Email Contacts from TO and CC
email Addresses* automatically creates additionally copied people as
*Complaint Contacts* on the intake so they can be selected in
subsequent mails.

### Limits of the mapping - the part that hurts in operation

- **Matching is header-only.** If the reporter does not use "reply"
  but writes a fresh email, the root message ID is missing and there
  is no match.
- **Behaviour on no match:** at the follow-up mailbox Vault instead
  creates a **new *Complaint Intake***  - its object type is
  configured on the *Inbound Email Address Configuration* under
  *If match not found, create Complaint Intake with this Object Type*.
  The reply is therefore not lost, but lands as a duplicate in triage
  and has to be merged manually. This duplicate rate is a volume risk
  and should be measured early.
- **Auto-forwarding is mandatory**; redirecting breaks the matching.
- **Allowed Senders on the follow-up mailbox** is documented as *All
  Users & Persons in this Vault* - not *Anyone* as on the intake
  mailbox. That works because the actual sender at this mailbox is
  the forwarding Bayer system, not the external reporter. This
  construction must be verified in DEV; it is the most fragile point
  in the chain.
- **Two mailboxes are required**: one for first contact
  (*Create Complaint*), one for follow-up replies (*Complaint Intake
  Follow-Up Email Processor*). Plus the reply-to address in the Bayer
  mail system.
- **[26R3 cross-check 2026-11-05]** Required permissions for the
  *Email Processor User* on the second mailbox: *Read* on *Complaint
  Intake Followup Sent Notif*, *Edit* on *Complaint Intake Follow-Up*,
  *Create* on *Complaint Intake* and *Complaint Intake Follow-Up
  Email*.
- **Release status:** as of this document, level 2 is **Limited
  Release**, not General Release. Before fixing this in the design,
  clarify which POD and release track the IQMS Vault runs on and when
  26R3 reaches it.

### Short version for the requirements discussion

Yes, replies are mappable - down to the individual follow-up
question. The mapping is robust as long as the reporter replies
rather than writing afresh. The price is two mailboxes, a forwarding
path in the Bayer mail system, and a dependency on a release
currently only available in Limited Release.

Sources:

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

## Question 6 - Which object types are involved in complaint handling, and how are they connected?

**Question:** Which objects play a role in email-based complaint
handling, and how are they linked to each other?

**Answer:**

Diagram (drawio):
[veeva-complaint-email-object-model.drawio](veeva-complaint-email-object-model.drawio)

### The objects involved

| Object | Role |
| --- | --- |
| **Inbound Email Address** | Vault configuration object, not a data record. The mailbox itself (`<name>@<subdomain>.veevavault.com`), with its allowed-senders rule and assigned email processor. |
| **Email** | One record per incoming message: the original as `.EML`, attachments, status (*Received*, *Bounced*, *Failed*). Read by the processor, not edited by users. |
| **Complaint Intake** | The triage stage. One record per new email thread. Mandatory fields are populated from the message (see question 2's mapping table). |
| **Complaint Contact** | The point of contact on the intake or on the complaint. For *Complaint Intake* this object type is **mandatory** (object type *Initial Reporter*, max. 1 per intake) - *Person* is not supported there (see question 3). Object type *Email Contact*: additional contacts from the To/CC of an inbound email, creatable automatically via *Auto-Create Complaint Contacts* (26R3 LR, **[26R3 cross-check 2026-11-05]**). |
| **Person** | Alternative to *Complaint Contact* for all other QMS objects (including *Complaint*), but **not** for *Complaint Intake*. |
| **Reported Product** | The reported product/batch, attached to the intake and carried over on promote; can drive *Split by Batch* into multiple complaints. |
| **Complaint Intake Follow-Up** | From 26R3 LR the correspondence object for follow-up questions (before that, pure documentation storage, see question 3). One record per follow-up question. Fields *Retry?*/*Retry Frequency*/*Remaining Retries* optionally drive *Auto-Retry* (26R3 LR, see question 9). |
| **Complaint Intake Follow-Up Email** | One record per message sent or received for a follow-up (*Direction* field = *Outbound*/*Inbound*). |
| **Complaint Intake Followup Sent Notif** | **[26R3 cross-check 2026-11-05, newly captured]** Delivery-status tracking specifically for *Complaint Intake Follow-Up* emails (separate from the general *Quality Event Sent Notification*). |
| **Followup Evaluation** | **[26R3 cross-check 2026-11-05, new object]** Automatically created impact-assessment record per affected *Complaint* when a *Complaint Intake Follow-Up* receives new information requiring assessment (26R3 LR). See question 8. |
| **Complaint / Quality Event (object type Complaint)** | The regulated target record, created by *Promote to Complaint*. References the originating *Complaint Intake*, which exposes its contacts, reported products and follow-ups. |
| **Quality Event Sent Notification / Email (Tracked Emails)** | Delivery-status tracking for sent external notifications (general, not follow-up specific). |

### The core connections

1. **Inbound Email Address -> Email -> Complaint Intake**: the
   *Create Complaint* processor reads the *Email* record and creates
   (or updates) the *Complaint Intake* from it. Controlled by *Email
   Thread Detection* (message ID / root message ID).
2. **Complaint Intake -> Complaint Contact (1:N, mandatory)** and
   **-> Reported Product (1:N)**.
3. **Complaint Intake -> Complaint Intake Follow-Up (1:N)** - one
   follow-up question per follow-up record.
4. **Complaint Intake Follow-Up -> Complaint Intake Follow-Up Email
   (1:N)** - one email record per send or per reply.
5. **Complaint Intake -> Complaint (1:N via Promote to Complaint)** -
   the complaint references the intake back, thereby "inheriting" its
   contacts/products/follow-ups for display.
6. **Complaint Intake -> "no promote"**: spam, advertisements or
   misdirected mail are resolved at the intake stage (see question 7,
   section e) and never become a *Complaint*.
7. **[26R3 cross-check 2026-11-05, new]** **Complaint Intake
   Follow-Up -> Followup Evaluation (1:N, automatic, only after
   promote)** - one *Followup Evaluation* record per active,
   non-cancelled *Complaint* originating from the same *Complaint
   Intake*; it references the *Complaint*, the *Complaint Intake*, and
   the triggering *Complaint Intake Follow-Up*. See question 8.

Sources:

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

## Question 7 - End to end: intake, follow-up, reply, promotion, non-complaint mail

**Question:** In detail, how are incoming emails, follow-up questions,
replies to follow-up questions, and the promotion of an intake to a
real complaint handled - and what happens to mail that is not a
complaint at all (e.g. advertising)?

**Answer:**

### a) Incoming email (first contact)

1. The sender writes to the public inbound email address. Vault
   checks **Allowed Senders** (for complaints: *Anyone*) and, if
   **Authenticate Sender** is enabled, SPF/DKIM.
2. If the message passes, Vault creates an *Email* record; the
   configured **Create Complaint** processor runs, under the **Email
   Processor User** if the sender is unknown.
3. The processor checks **message ID / References** in the header
   (*Email Thread Detection*). No match -> a new *Complaint Intake*
   record is created, fields are populated automatically (see
   question 2's mapping table), attachments plus the original `.EML`
   go into the Attachments section.
4. If the check fails (unknown/disallowed sender, SPF/DKIM failure),
   the message is rejected; the *Email* record gets status
   *Bounced*/*Failed*.
5. Configuration details: see question 2.

### b) Follow-up question (outbound)

1. The processor opens the *Complaint Intake* and runs **Send
   External Notification** (General Release), or from 26R3 LR the
   action on the *Complaint Intake Follow-Up* record.
2. The recipient is always a **Complaint Contact** of type *Initial
   Reporter* (never *Person*) - prerequisite: *Consent to Contact* =
   Yes, a valid *Email*, *Status* = Active.
3. General Release: the text comes entirely from the template (tokens
   are merged), subject/body are not freely editable. From 26R3 LR:
   free text in subject/body is possible while the boilerplate is
   preserved; Vault creates a *Complaint Intake Follow-Up Email*
   record with *Direction* = *Outbound*.
4. **Reply-To** (from 26R3 LR) points at a mailbox in the Bayer mail
   system, not directly at Vault - that is the basis for part c).
5. Details: see question 3 (mechanics) and question 4
   (templates/review).

### c) Reply to the follow-up question (inbound)

1. If the reporter replies, the message first lands in the Bayer mail
   system (Reply-To) and is **auto-forwarded** from there (not
   redirected) to a **second** inbound email address using the
   **Complaint Intake Follow-Up Email Processor**.
2. That processor matches **mandatorily on the root message ID** and
   attaches the reply to the matching *Complaint Intake Follow-Up*
   record (on General Release without this feature: the reply only
   attaches to the *Complaint Intake* itself, not to the individual
   follow-up question - see question 5, level 1 vs. level 2).
3. No match (e.g. because the reporter writes a fresh email instead of
   replying) -> Vault creates a **new Complaint Intake** (configured
   fallback object type). This is the documented duplicate case, see
   question 5, "Limits of the mapping".
4. Details including field population: see question 5.

### d) Promoting an intake into a real complaint (Promote to Complaint)

1. Before promotion, every mandatory field of the target *Complaint*
   object type must be populated on the *Complaint Intake* and
   *Reported Product*.
2. The processor (or an entry/workflow action) runs **Promote to
   Complaint**. Optional **Split by Batch** (one complaint per
   product/batch combination) and **Copy Attachments**.
3. Vault creates the *Complaint* or *Quality Event* record in the
   chosen object type and sets the back-reference **Complaint
   Intake** - this makes contacts, reported products and follow-ups
   (including their attachments) visible on the complaint as well.
4. The action runs **once only** per intake; a second invocation
   produces a system error - so there is no way to accidentally
   create two complaints from one intake.
5. Details: see question 2, step 8.

### e) Non-complaint mail (advertising, spam, misdirected mail)

This is the part the Veeva standard feature does **not** solve
automatically:

- *Create Complaint* is a pure **transcription processor**: it reads
  sender, subject, body and attachments and writes them into fields -
  it does **not** evaluate the content. Every accepted message (one
  that passes the allowed-senders and SPF/DKIM check) produces a
  *Complaint Intake* record, regardless of whether it is actually a
  complaint, an advertisement, a product inquiry, or spam.
- This is exactly what *Complaint Intake* is designed for as a
  **triage stage** (see question 2, section 3): a processor - or an
  upstream classification step - has to review every intake record
  and decide whether it is a genuine complaint.
- If an intake is identified as not a complaint (advertising, spam, a
  product question with no PTC relevance, misdirected mail, etc.), it
  is **not promoted**. Instead it is closed or rejected via the
  *Complaint Intake* lifecycle (e.g. status *Rejected* / *Closed -
  Not a Complaint*, depending on the project's lifecycle
  configuration). **No** *Complaint* record is created, so the item
  leaves the regulated complaint process, while the intake record
  (with its audit trail) remains in the Vault.
- This decision (complaint yes/no, and if yes which complaint type) is
  **not solved natively by Veeva** in this project; it is the subject
  of the project's own classification logic (see
  `docs/05-design-spec/prompts-classification/` and
  `docs/templates/assets/classification-decisions.drawio` in this
  repo) - which describes exactly this upstream check (PTC-relevant?
  spam? advertisement? malware? product inquiry?) as a decision tree.
  Veeva provides the triage *stage* (*Complaint Intake*); the
  classification *logic* for what happens to a given record on that
  stage has to be built by the project itself (manually or AI-assisted,
  either before or after the promote step).
- Important for spam/advertising defence at the mail level (before an
  intake is even created): **Authenticate Sender** (SPF/DKIM, see
  question 1) catches spoofed senders, but not legitimately sent
  advertising from real senders - it filters spoofing, not content.

Sources:

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

## Question 8 - Followup Evaluation: automated impact assessment (26R3 LR)

**Question:** What happens if a reply to a follow-up question
contains new safety- or quality-relevant information, even though the
associated complaint has already been promoted (and may already be in
progress or closed)?

**Answer:** 26R3 Limited Release delivers an entirely new object plus
automation for this: **Followup Evaluation**. Without this feature, a
processor would have to manually recognise and track that a newly
received follow-up reply could affect an already-created *Complaint*.

### Trigger

Vault creates a *Followup Evaluation* record as soon as **both**
conditions are met on a *Complaint Intake Follow-Up* record:

1. The *Latest Response Details* field is populated on creation, or
   updated/populated on an existing record.
2. The *Followup Evaluation Type* field is set to *Followup
   Evaluation Needed* (not *No Impact* - which lets you deliberately
   exclude things like typo corrections).

Additional condition: the parent *Complaint Intake* must already have
created **at least one** *Complaint* via *Promote to Complaint*.
Without a promote, no *Followup Evaluation* is created - consistent
with the rest of the model: the assessment only exists in relation to
already-regulated cases.

### What happens automatically

- Vault creates **its own** *Followup Evaluation* record **per
  related, active Complaint** - if multiple complaints originate from
  the same intake (e.g. via *Split by Batch*), there will be multiple
  evaluation records accordingly. Cancelled complaints are excluded,
  but **closed ones are not** - so the assessment still happens even
  after a complaint has been closed.
- Each *Followup Evaluation* record references: the *Complaint*, the
  originating *Complaint Intake*, and the triggering *Complaint
  Intake Follow-Up*.
- The *Response Date* and *Response Details* fields are copied as a
  point-in-time snapshot from the *Latest Response Date* and *Latest
  Response Details* of the follow-up record.
- A configurable workflow starts automatically, assigns a review task
  to the *Complaint Owner* (assigned via Quality Teams or Dynamic
  Access Control), and notifies the relevant people.

### Limitations

- **Not supported** if the Vault represents complaints via the
  *Quality Event* object types *Complaint* or *MedTech Complaint*
  rather than the standalone *Complaint* object. For this project,
  you therefore first need to clarify (see question 2, step 1) which
  data model is in use - that decides whether this feature is usable
  at all.
- Requires Admin configuration: activate the *Followup Evaluation
  Type* field and expose it on the *Complaint Intake Follow-Up*
  layout, add related-object sections for *Followup Evaluation* to
  *Complaint* and *Complaint Intake Follow-Up* (recommended also on
  *Complaint Intake*), configure role assignment via Quality Teams or
  Dynamic Access Control, and build a dedicated evaluation workflow if
  required.
- Release status: **26R3 Limited Release**, not General Release - the
  same constraint as the rest of the follow-up correspondence feature
  (see question 5, level 2).

Sources:

- New in 26R3 Limited Release (Complaint Intake Follow-Up Evaluation) -
  https://rn.veevavault.help/en/lr/new-in-26r3/
- Configuring Complaint Intake Follow-Up (QMS), Limited Release -
  https://quality.veevavault.help/en/lr/1227595/
- Working with Complaint Intake Follow-Up (QMS), Limited Release -
  https://quality.veevavault.help/en/lr/1227594/

---

## Question 9 - Auto-Retry for unanswered follow-ups (26R3 LR)

**Question:** Can unanswered follow-up requests be automatically
retried, instead of a processor having to chase them manually?

**Answer:** Yes, via the 26R3 LR feature **Complaint Intake
Follow-Up: Auto-Retry** - an Admin-configured, scheduled job
(typically hourly) that automatically re-triggers unanswered
follow-ups.

### Control fields on *Complaint Intake Follow-Up*

| Field | Meaning |
| --- | --- |
| *Retry?* | Must be set to *Auto* for the job to pick up the record at all. |
| *Retry Frequency* | Interval in days between two automatic attempts. |
| *Retry Due On* | The date on which the next automatic attempt is due. |
| *Remaining Retries* | Remaining automatic attempts; decreases by 1 on each auto-retry. |

### Flow

1. The job periodically checks *Complaint Intake Follow-Up* records
   against Admin-configured conditions (among others: allowed contact
   methods, allowed states of the follow-up **and** its parent
   *Complaint Intake*, optionally a *Previous Attempt End State*).
2. On a match, Vault creates a **new** *Complaint Intake Follow-Up*
   record with the same details as the previous attempt - this is the
   next attempt record, not an update of the old one.
3. Optionally (**Auto-Send External Email**) the job also
   automatically sends an email to the same complaint contacts as the
   initial send.
4. If sending fails, Vault sets the new follow-up record to *Error*
   state and records the cause in *Error Message*.
5. If a reply arrives in the meantime anyway, Vault automatically ends
   the retry cycle: *Retry Rule* is set to *None* and *Retry Due On*
   is cleared.

### Limitations

- Document attachments are **not** supported by Auto-Retry - only
  links in the email are possible.
- Auto-Retry only supports **CC** for *Internal Recipients* and *Role
  Recipients*: if the initial send addressed these recipients as BCC,
  automatic retries go out to them as CC instead of BCC - a silent
  behaviour change that should be checked before go-live.
- For manual rather than automatic chasing (*Retry?* = *Manual*), you
  can instead configure a separate job plus a state change to *Retry
  Due* and a notification on that state change.
- Release status: **26R3 Limited Release**.

Sources:

- New in 26R3 Limited Release (Complaint Intake Follow-Up: Auto-Retry) -
  https://rn.veevavault.help/en/lr/new-in-26r3/
- Configuring Complaint Intake Follow-Up (QMS), Limited Release -
  https://quality.veevavault.help/en/lr/1227595/
- Working with Complaint Intake Follow-Up (QMS), Limited Release -
  https://quality.veevavault.help/en/lr/1227594/

---

## 26R3 cross-check changelog (2026-11-05)

Once the Vault Documentation MCP server was reachable again, this
document was checked in full against current Veeva documentation
(General Release and 26R3 Limited Release). Overview of all content
changes:

| Location | Before | Now | Status |
| --- | --- | --- | --- |
| Question 2, step 4 (permissions) | Generic *Read* on *Email*, *Person*, *Complaint*, *Complaint Intake*, *Quality Event* | Object-specific: *Complaint Intake Email* / *Complaint Intake Sent Notif* vs. *Complaint Email* / *Complaint Sent Notification*, depending on target object | Corrected |
| Question 3, contact creation | "Documentation does not confirm whether automatic" | Automatic creation possible via *Auto-Create Complaint Contacts* (26R3 LR), two checkboxes on the Inbound Email Address Configuration, requires object type *Email Contact* | Open question answered |
| Question 5, level 2, recipient | Unconditionally *Initial Reporter* | Primarily the *Primary Contact* field on the follow-up, falling back to *Initial Reporter* | Corrected |
| Question 5, follow-up tracking | Only the general *Quality Event Sent Notification* mentioned | Dedicated object *Complaint Intake Followup Sent Notif* for follow-up-specific tracking, including permission detail | Added |
| Question 6, object table | No *Followup Evaluation*, no *Complaint Intake Followup Sent Notif*, *Email Contact* not mentioned | Both objects added, *Complaint Contact* object type *Email Contact* added | Added |
| Question 6, core connections | 6 connections | 7th connection *Complaint Intake Follow-Up -> Followup Evaluation* added | Added |
| New: Question 8 | not present | *Followup Evaluation* (automated impact assessment, 26R3 LR) newly documented in full | New |
| New: Question 9 | not present | *Auto-Retry* for unanswered follow-ups (26R3 LR) newly documented in full | New |
| 26R3 release status overall | Marked as Limited Release | **Confirmed still Limited Release**, not General Release (configuration articles still only live under `/lr/` paths) | Confirmed, no change |
| Diagram | Object model without Followup Evaluation | *Followup Evaluation* and *Complaint Intake Followup Sent Notif* added as nodes | Added (see [veeva-complaint-email-object-model.drawio](veeva-complaint-email-object-model.drawio)) |

**Unchanged** (confirmed by the cross-check, no deviation found from
the existing documentation): questions 1, 2 (apart from the
permission refinement noted above), 4, 7, and all remaining
statements in questions 3 and 5.
