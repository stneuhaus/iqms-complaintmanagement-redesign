# Complaint classification workshop — YYYY-MM-DD — <site>

- Date:
- Site / GBS center:
- Participants (role, years in PTC handling — prefer role over name):
- Facilitator:
- Duration: ~90 minutes

## Purpose

Capture how Complaint Managers actually decide what kind of complaint an incoming message is, so the criteria can be written down and used for an automated pre-classification. The Complaint Manager remains the decision authority — the goal is a reliable **proposal with a visible rationale**, not an autonomous decision.

Bring: printed [decision cards](classification-decision-card.md), the case set, one set of category labels per participant.

---

## Agenda

### Part 1 — Framing (15 min)

Explain the three decisions and why the categories are split this way. Be explicit about the three points where an intuitive grouping differs from the SOPs, because participants will otherwise classify against the familiar picture:

| Common assumption | What the SOPs say |
| --- | --- |
| Adverse events are a kind of complaint, split into serious / non-serious | A pure AE is **not a PTC** (SSC-PTC-SOP-001 §5.2.1.1) and does not enter IQMS — it goes to PV. Seriousness is assessed by PV in ARGUS, not by the CM. For us, AE is a **yes/no flag**. |
| PTCs are grouped by defect: packaging, labeling, missing parts, device defect | That is the `Defect Category` field, set **after the investigation**. At intake it is usually not yet decidable. |
| Classification starts with "which complaint type is it?" | It starts one step earlier: **is this a PTC at all?** Spam, advertisements, product questions, stability, reimbursement and divested-product inquiries must never reach IQMS (URS REQ-021/023). |

The three decisions:

```text
DECISION 1 — Intake gate
  Is this PTC-relevant? ──yes──> Decision 2
                        └─no───> Non-PTC subtype
                                 (Spam | Advertisement | Malware |
                                  Non-PTC product question | Stability |
                                  Reimbursement | Divested product)
                              + special case: Follow-up / Duplicate

DECISION 2 — Case type
  PTC | PTC+AE | Usability Issue (Use Error | Customer Satisfaction Issue)
  | Suspected Falsification / Counterfeit

DECISION 3 — Adverse event   yes / no
  (seriousness is out of scope — PV / ARGUS decide that)
```

Decision 3 is made even when decision 1 says "not a PTC" — a pure adverse event report does not enter IQMS, but it still has to reach Pharmacovigilance.

Out of scope for this workshop, and worth saying so up front: Initial Risk Classification (High/Medium/Low) and Defect Category.

### Part 2 — Case sorting (40 min)

**Each participant sorts individually. No group discussion during this part.** The spread across participants is the measurement — a consensus reached in the room would destroy exactly the signal we need.

1. Hand out the case set (20–30 anonymized real messages).
2. Each participant writes, per case: the decision 1 result, the decision 2 result, the AE answer, and a confidence mark (`sure` / `unsure`).
3. Collect sheets **before** any discussion.
4. Fill the disagreement matrix below.
5. Then discuss **only** the cases where answers differed, or where several people marked `unsure`. Cases everyone agreed on need no airtime.

For each discussed case, record: what the disagreement was about, which information would have resolved it, and whether a decision was reached at all.

### Part 3 — Decision cards (25 min)

Distribute categories across participants (2–3 cards each; pair up for the rare categories). Hand out the pre-filled sample card as a reference for the expected level of detail.

Priority if time runs short — fill these first:

1. The non-PTC categories (highest volume, clearest automation benefit)
2. Follow-up / duplicate detection (today purely experience-based per URS REQ-008)
3. Use Error vs. Customer Satisfaction Issue (the SOP definition is abstract)
4. Suspected falsification / counterfeit (URS REQ-056 has **no criteria at all** — they are to be collected here)

### Part 4 — Open points (10 min)

Who supplies what, by when. Especially the pick-lists that exist in IQMS but in no document: `Feedback Type`, `Report Source`, `Product Type`, `Error codes`.

---

## Record: disagreement matrix

One row per case. Mark where participants differed — those rows become mandatory human-review rules.

| Case | CM 1 | CM 2 | CM 3 | CM 4 | Agreement | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | | | | | `full` / `partial` / `none` | |
| 02 | | | | | | |
| 03 | | | | | | |

Summary:

| Metric | Value |
| --- | --- |
| Cases with full agreement | |
| Cases with partial agreement | |
| Cases with no agreement | |
| Cases marked `unsure` by ≥2 participants | |

## Record: discussed cases

### Case <nr>

- Disagreement was about:
- What would have resolved it:
- Decision reached:
- Should this always go to a human? `yes` / `no` — why:

## Record: criteria mentioned but not in any SOP

Rules participants apply from experience, with no written basis. These need a decision: either formalize them into an SOP, or mark them as local practice in the prompt.

| Criterion | Category | Who applies it | Written down anywhere? |
| --- | --- | --- | --- |
| | | | |

## Record: country specifics

Does classification itself differ by country, or only the routing afterwards?

| Country | What differs | Source |
| --- | --- | --- |
| | | |

## Open questions and follow-ups

| Question | Owner | Due |
| --- | --- | --- |
| | | |

---

Save as `docs/01-current-process/sources/YYYY-MM-DD-cm-classification-workshop-<site>.md`.
Completed decision cards go alongside it. Then feed the criteria into the classification prompt
([prompts-classification/](../05-design-spec/prompts-classification/README.md)) and update the glossary
if new terms came up.
