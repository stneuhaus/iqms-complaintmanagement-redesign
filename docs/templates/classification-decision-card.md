# Classification decision card — <CATEGORY NAME>

One card per category. Fill one card for **every** category you are assigned.

The purpose of this card is to turn what you already do from experience into criteria someone else — or an automated pre-check — can apply and get the same answer. Write what you **observe in the message**, not what you conclude after an investigation.

How to fill this in:

- Write criteria a colleague could apply **without asking you**.
- Prefer concrete wording over abstract rules: "sender domain is a company, not a person" beats "looks commercial".
- If you cannot give a rule, give an example. Examples are more useful than a vague rule.
- Say **how the criteria combine**, not just what they are. A list alone does not tell us whether all of them are required or only some — see sections 4 and 5.
- If you genuinely don't know, write it under **Open questions**. An honest gap is more valuable than a guess — it tells us where a human must decide.
- Anonymize all examples: no patient names, no reporter names, no addresses. Product, batch and wording may stay.

---

## 1. Identification

| Field | Value |
| --- | --- |
| Classification result | The category this card describes, e.g. `Advertisement`, `PTC+AE`, `Use Error` |
| Which decision | `Decision 1 — Intake gate` / `Decision 2 — Case type` / `Decision 3 — Adverse event` |
| Filled in by (role, site) | |
| Date | |

The three decisions are made one after another on every incoming message:

| | Decision | The question behind it |
| --- | --- | --- |
| 1 | Intake gate | Does this belong in the PTC process at all? |
| 2 | Case type | If yes — which kind of case is it? |
| 3 | Adverse event | Is a health effect on a person mentioned? |

Decision 3 is made **even when** decision 1 says "not a PTC": a pure adverse event report does not enter IQMS, but it still has to reach Pharmacovigilance.

## 2. Short definition

One or two sentences, in your own words. How would you explain this category to a new colleague on their first week?

> 

## 3. SOP basis

| Field | Value |
| --- | --- |
| SOP / User Letter reference | e.g. `SSC-PTC-SOP-001 §5.2.1.1`, `GSOP 115 §4.1.1`, `IQMS UL 40` |
| Is the rule written down anywhere? | `written in SOP` / `local practice, not written` / `unsure` |
| Country-specific? | `global` / `applies only to: <countries>` |

If the rule is **local practice**, say so plainly. It is not a problem — but it must be visible, because an unwritten rule cannot be validated the same way a written one can.

## 4. Decide YES if …

Positive criteria. One observable signal per line. Aim for 3–8 lines.

**Not every criterion has to be met.** Mark each one as either:

- `[REQUIRED]` — if this is absent, it cannot be this category
- `[SUPPORTING]` — points this way, but is not required on its own

Then say how they combine, e.g. "all `[REQUIRED]` plus at least two `[SUPPORTING]`".

- `[REQUIRED]` 
- `[REQUIRED]` 
- `[SUPPORTING]` 
- `[SUPPORTING]` 

How they combine: 

## 5. Decide NO if …

Negative criteria — what looks like this category but isn't. One per line.

**Any single one of these is enough to rule the category out**, even if every criterion in section 4 is met. If that is not true for one of your lines, it belongs in section 4 as `[SUPPORTING]` instead, or in section 9 as a case for human review.

- 
- 
- 

## 6. Signal phrases

Actual wording you look for in incoming messages. Original language is welcome and useful — write the language in brackets.

| Phrase | Language | Points to |
| --- | --- | --- |
| | | |
| | | |

## 7. Signals in attachments

What in a photo, scan, form or PDF points to this category?

- 
- 

## 8. How is the decision made?

| Field | Value |
| --- | --- |
| Hard rule or judgement? | `hard rule — always the same answer` / `judgement — depends on the case` |
| If hard rule: state it as IF … THEN … | Use only the `[REQUIRED]` criteria from section 4, joined with AND. If that sentence does not hold on its own, it is not a hard rule — say `judgement` instead. |
| How long does the decision usually take? | `seconds` / `a few minutes` / `I often have to ask someone` |
| Do you need anything outside the message? | e.g. product list, SynApps, previous cases, a colleague |

## 9. When must a human decide?

Under which conditions would you **not** trust an automated pre-classification and insist on reviewing it yourself?

- 
- 

> This section directly shapes the solution. Everything listed here becomes a mandatory human review in the automated process — the Complaint Manager stays the final decision authority either way (SOP 1937, GenAI does not make GxP decisions autonomously).

## 10. Confused with

| Often confused with | How do you tell them apart? |
| --- | --- |
| | |
| | |

## 11. Examples

Three anonymized real cases. These are the most valuable part of the card.

### 11a. Clear YES

> Message extract:
>
> Why it is clearly this category:

### 11b. Clear NO — but looks like it

> Message extract:
>
> Why it is **not** this category, and what it is instead:

### 11c. Borderline — you had to think about it

> Message extract:
>
> What made it hard:
>
> What you decided in the end, and why:

> If you had to ask a colleague, or if you are still not sure the decision was right, say so. Borderline cases are exactly where the automation needs to hand over to a human.

## 12. Frequency and impact

| Field | Value |
| --- | --- |
| How often? | `several times a day` / `daily` / `weekly` / `rarely` |
| Roughly what share of your inbox? | e.g. `~20 %` |
| What happens if it is classified **wrongly**? | |
| Is a wrong decision easy or hard to correct later? | |

## 13. Open questions

Anything you are unsure about, where colleagues disagree, or where the SOP does not give you an answer.

- 

---

Save completed cards together with the workshop notes under
`docs/01-current-process/sources/YYYY-MM-DD-cm-classification-workshop-<site>.md`,
or as individual files next to it if there are many.
