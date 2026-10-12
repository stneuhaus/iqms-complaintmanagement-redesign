# Classification decision card — ADVERTISEMENT (filled example)

> **This is a worked example, not a real card.** It shows the level of detail we need.
> It was pre-filled from URS REQ-054 and the as-is notes — the criteria still have to be
> confirmed and corrected by the Complaint Managers. Where something is uncertain, it is
> written into **Open questions** rather than guessed. Please do the same.
>
> Blank template: [classification-decision-card.md](classification-decision-card.md)

---

## 1. Identification

| Field | Value |
| --- | --- |
| Classification result | Advertisement |
| Which decision | `Decision 1 — Intake gate` |
| Filled in by (role, site) | Pre-filled from documentation — to be confirmed by GBS PTC team |
| Date | 2026-10-12 |

## 2. Short definition

Unsolicited commercial mail that reached a PTC inbox. Somebody is selling something — they are not reporting a problem with a Bayer product. The product, if one is mentioned at all, is described as working fine.

> Rule of thumb: an advertisement wants something **from** us. A complaint wants something **about** a product.

## 3. SOP basis

| Field | Value |
| --- | --- |
| SOP / User Letter reference | URS REQ-054; `SSC-PTC-SOP-001 §5.2.1.1` (general non-PTC gate) |
| Is the rule written down anywhere? | `written in SOP` — but only two criteria are given (intact product, commercial sender) |
| Country-specific? | `global` |

REQ-054 says: *"Advertisements are recognized by the following criteria: Description of an intact product. Senders are commercial companies."* That is the whole written rule — everything below it is the practical reading that needs confirming.

## 4. Decide YES if …

Not every criterion has to be met. Each one is marked as:

- `[REQUIRED]` — if this is absent, it cannot be this category
- `[SUPPORTING]` — points this way, but is not required on its own

Criteria:

- `[REQUIRED]` The sender is a company, not a private person or healthcare professional — check the mail domain and the signature block
- `[REQUIRED]` A product is described as **intact and functioning** — no defect, no damage, no deviation is alleged
- `[REQUIRED]` No batch number, no lot number, no expiry date — the identifiers a real complaint almost always carries
- `[SUPPORTING]` No Bayer product is named at all, or one is named only as a reference ("we also supply packaging for …")
- `[SUPPORTING]` The message offers goods or services: supplies, logistics, lab services, consulting, conference slots, software
- `[SUPPORTING]` There is no patient, no reporter and no incident — nobody was affected by anything
- `[SUPPORTING]` It is a mass mailing: generic salutation, unsubscribe link, marketing footer, tracking pixels

How they combine: **all three `[REQUIRED]` must be met.** The `[SUPPORTING]` criteria raise confidence but none of them is needed on its own — a personally written sales mail with no unsubscribe link is still an advertisement. If the three `[REQUIRED]` hold but not a single `[SUPPORTING]` one does, send it to human review rather than to junk.

## 5. Decide NO if …

Any one of these rules the category out on its own, even where all of section 4 is met.

- A defect, damage, deviation or suspicion is described — **even if the sender is a company**. A wholesaler reporting crushed cartons is a PTC, not an advertisement
- The sender is a pharmacy, hospital, doctor's practice or wholesaler **and** refers to a concrete delivery, batch or product
- The product's authenticity is questioned, even in passing → that is a suspected falsification/counterfeit and is handled as a **PTC** (SSC-PTC-SOP-001 §5.2.1.2 remark)
- It is a reply inside an existing thread → follow-up, not advertisement
- The message contains an attachment that looks like a complaint form, a photo of a product, or a delivery note
- A third party advertises a product that imitates a Bayer product → that is a **trademark violation / fraudulent generic**, which is a counterfeit case, not junk

> Note the asymmetry, and why it is deliberate: the positive criteria need several signals together, a single negative one is enough to stop. Wrongly treating junk as a complaint costs a few minutes. Wrongly discarding a real complaint as junk is invisible — nobody reviews the junk folder while the 5-day intake clock runs.

## 6. Signal phrases

| Phrase | Language | Points to |
| --- | --- | --- |
| "we are a leading supplier of …" | EN | Advertisement |
| "request a quote" / "our price list" | EN | Advertisement |
| "unsubscribe" / "click here to opt out" | EN | Advertisement (mass mailing) |
| "Angebot" / "unverbindliches Angebot" | DE | Advertisement |
| "Abmelden" / "Newsletter" | DE | Advertisement |
| "oferta" / "cennik" | PL | Advertisement |
| "we would like to introduce our company" | EN | Advertisement |
| — but: "we received a damaged delivery" from a company sender | EN | **PTC**, not advertisement |

## 7. Signals in attachments

- Brochures, price lists, product catalogues, company presentations
- Logos and marketing imagery, no product photographs showing a defect
- No complaint form, no delivery note, no photograph of damaged goods
- Attachment names like `catalogue`, `offer`, `brochure`, `company_profile`

## 8. How is the decision made?

| Field | Value |
| --- | --- |
| Hard rule or judgement? | `hard rule` for the clear majority; a small share needs judgement |
| If hard rule: state it as IF … THEN … | IF sender is a commercial company AND no defect/damage/deviation is alleged AND no Bayer batch or product identifier is present THEN `ADVERTISEMENT` |
| How long does the decision usually take? | `seconds` — usually visible from subject line and sender alone |
| Do you need anything outside the message? | No. Decidable from the message itself. |

## 9. When must a human decide?

- The sender is a company **and** a Bayer product is named — the line between "commercial mail" and "complaint from a business partner" has to be checked
- The message mixes marketing with a product remark ("by the way, the last batch had …")
- A product resembling a Bayer product is being offered — possible trademark violation, which has to go to CQH, not to the junk folder
- The mail carries an attachment that could not be read or was flagged by the virus scanner → malware route, not junk
- Anything where discarding the message would be hard to undo

> Everything here becomes a mandatory human review. Misrouting a real complaint into junk is the expensive error in this category — see section 12.

## 10. Confused with

| Often confused with | How do you tell them apart? |
| --- | --- |
| Spam | Spam is untargeted junk or fraud with no commercial sender identity. An advertisement has an identifiable company behind it that wants to sell something. In practice both are filtered out — but they are routed to different places. |
| Non-PTC product question | A question asks something **about a Bayer product** (ingredients, storage, temperature excursion). An advertisement offers something **to** Bayer. |
| Trademark violation / fraudulent generic | If a third party advertises an imitation of a Bayer product, it is **not** junk — it is a counterfeit case and must be escalated to CQH. This is the most consequential confusion in this category. |
| Malware | If the virus scanner flags it, the malware route wins regardless of how the text reads (URS REQ-055 → Bayer Cyber Security Center). |

## 11. Examples

### 11a. Clear YES

> Message extract:
> "Dear Sir or Madam, we are a leading manufacturer of pharmaceutical packaging materials and would
> like to introduce our portfolio. Please find our current catalogue attached. We would be glad to
> provide a non-binding quote. — Unsubscribe here."
>
> Why it is clearly this category: commercial sender, no Bayer product, no defect, no batch, no patient,
> mass-mailing footer. Nothing to report, something to sell.

### 11b. Clear NO — but looks like it

> Message extract:
> "Dear colleagues, we are a pharmaceutical wholesaler. In the delivery received on 2026-09-14 we found
> that 12 cartons of [product], batch [nr], were crushed and partly open. Photographs attached. Please
> advise how to proceed."
>
> Why it is **not** this category, and what it is instead: the sender is a company — the first criterion
> matches — but a defect is alleged, a batch number is given and photographs are attached. This is a
> **PTC**. It shows that "commercial sender" alone is never sufficient.

### 11c. Borderline — you had to think about it

> Message extract:
> "We are a distributor in [country] and offer [product name very close to a Bayer brand] at competitive
> prices, same active ingredient as the original. Minimum order 500 units."
>
> What made it hard: it reads exactly like an advertisement — commercial sender, no defect, no batch.
> By the written criteria it would go to junk.
>
> What was decided in the end, and why: **not** an advertisement. A third party offering a product that
> imitates a Bayer product by name and by claiming the same API is a **fraudulent generic** under
> SSC-PTC-SOP-001 Annex 3, and has to be escalated to CQH (URS REQ-057). Discarding it as junk would
> lose a counterfeit signal.

## 12. Frequency and impact

| Field | Value |
| --- | --- |
| How often? | `daily` — to be confirmed per site |
| Roughly what share of your inbox? | unknown — **please estimate**, it drives how much this is worth automating |
| What happens if it is classified **wrongly**? | Asymmetric. Junk wrongly treated as a PTC costs a few minutes. A **real complaint wrongly discarded as junk** is a compliance issue: the 5-day intake clock runs regardless, and nobody notices the message is gone. |
| Is a wrong decision easy or hard to correct later? | Hard. Nothing triggers a review of a discarded message — the error is invisible until the complainant follows up, if they ever do. |

## 13. Open questions

- What share of the inbox is advertising? No figure exists in any document.
- Are advertisements and spam routed to the **same** place today, or to different ones? URS REQ-054 says "junk location" but does not define it.
- Does the junk folder get reviewed by anyone, or is it final? This decides how much caution the automated gate needs.
- Is there a known sender allow/deny list already in use in ServiceNow that we could reuse?
- Who decides when a borderline commercial mail turns out to be a trademark violation — the CM, or CQH directly?
