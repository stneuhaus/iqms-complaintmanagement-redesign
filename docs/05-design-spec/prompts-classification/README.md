# Classification prompt

Status: In progress — criteria incomplete by design  
Last reviewed: 2026-10-12

The prompt that classifies a complaint **after** it has been translated to English ([FR-008](../../02-requirements/functional-requirements.md)). It consumes the Markdown output of the [translation prompt](../promtpts%20for%20text%20recogniztion/README.md) and emits a JSON classification proposal for the Complaint Manager.

This is the **categorization** step of the MVP chain agreed in [ADR-002](../../06-decisions/adr-002-mvp-slice.md): translation → extraction → **categorization** → confidence → HITL.

## Files

| File | Role |
| --- | --- |
| `prompt.de.md` | **German master.** Edited in place. All changes start here. |
| `prompt.classification.0.1.md` | Current English version — the one to use. |

Versioning follows the same rule as the translation prompt, with an **independent version count**: this prompt changes for different reasons than the OCR one.

**Every change to the English prompt creates a new file.** Never edit a released prompt file — it may already be referenced by an n8n workflow or a test record, and editing it in place would silently change what those runs were based on.

Workflow for a change: edit `prompt.de.md` → copy the English file to the next version (`0.1` → `0.2` for a new business feature; keep the number and append `_bugfix` for a pure fix) → apply the same changes → set `$prompt_file_version` in **both** files → add one changelog row in each → update the table above.

## The three classification axes

The axes are deliberately separate. A single flat list of "complaint types" cannot represent this process, because the decisions are made at different points by different people.

```
AXIS 1 — Intake gate
  Is this PTC-relevant? ──yes──> Axis 2
                        └─no───> SPAM | ADVERTISEMENT | MALWARE |
                                 NON_PTC_PRODUCT_QUESTION | STABILITY_ISSUE |
                                 REIMBURSEMENT_REQUEST | DIVESTED_PRODUCT_INQUIRY
                              + follow-up / duplicate detection

AXIS 2 — Case type (only where PTC-relevant)
  PTC | PTC+AE | UI (USE_ERROR | CUSTOMER_SATISFACTION_ISSUE)
     | SUSPECTED_FALSIFICATION_COUNTERFEIT (6 subtypes)

AXIS 3 — Adverse event flag   true | false | UNKNOWN
```

### What is deliberately out of scope

| Not classified here | Why |
| --- | --- |
| AE seriousness (serious / non-serious) | Decided by Pharmacovigilance in ARGUS, not by the Complaint Manager. The CM only sets the `Adverse Event Reported?` flag. |
| Initial Risk Classification (High / Medium / Low) | Requires product risk knowledge that is not present in the complaint text. Stays with the CM for now. |
| Defect Category (packaging, labeling, missing components, device defect) | A post-investigation field — marked `**` in the IQMS field catalogue. Usually not decidable at intake. |
| `Complaint Type` (the IQMS field of that name) | Only holds `external` / `internal`, and is always `external` in this process. The field name is misleading — it is not the taxonomy. |

## Open criteria

The prompt carries `<!-- TO BE COMPLETED -->` markers. These are **intentional gaps**, not omissions: the criteria behind them exist today only as Complaint Manager experience and have to be collected before they can be written down.

| Gap | Why it is open |
| --- | --- |
| Duplicate / follow-up recognition | URS REQ-008 gives three rough criteria and notes detection is "completely based on experience". REQ-020 and REQ-028 also contradict each other on whether related reports become one case or several linked ones. |
| Falsification / counterfeit criteria | **URS REQ-056 is empty** — it says "This can be assessed by the following criteria:" and then stops. |
| `USE_ERROR` vs `CUSTOMER_SATISFACTION_ISSUE` | The SOP definition is abstract ("no allegation that product fails to meet claims"); practitioners need worked examples. |
| Non-PTC subtype criteria | Only `ADVERTISEMENT` has written criteria (REQ-054). The rest are named but not defined. |
| AE signal phrases | Not documented anywhere. |

Collect them with the [decision card](../../templates/classification-decision-card.md) and the [workshop format](../../templates/classification-workshop.md); see the [filled example](../../templates/classification-decision-card.example.md) for the expected level of detail. Completed results go to `docs/01-current-process/sources/`.

Also still missing, and needed before IQMS field population can work at all: the allowed values of the `Feedback Type`, `Report Source`, `Product Type` and `Error codes` pick-lists. They are mandatory IQMS fields whose value lists appear in no document in the project set.

## How a filled decision card becomes prompt text

Each card section has a fixed destination. The mapping is mechanical — no interpretation needed when transferring.

| Card section | Goes into | Purpose |
| --- | --- | --- |
| §3 SOP basis | `sop_reference` in the JSON output | Traceability for GxP |
| §4 Decide YES if | criteria list under the axis, `[REQUIRED]`/`[SUPPORTING]` and the combination rule preserved verbatim | positive recognition |
| §5 Decide NO if | exclusion criteria under the axis, as vetoes | prevents over-detection |
| §6 Signal phrases | phrase table under the axis | multilingual trigger wording |
| §7 Signals in attachments | criteria list under the axis | evidence from attachments |
| §9 When must a human decide | `HUMAN REVIEW` section | forced HITL cases |
| §10 Confused with | delimitation rules under the axis | the expensive confusions |
| §11 Examples | **not** into the prompt → test set | gold standard for regression testing |
| §12 Frequency and impact | prioritization; HITL threshold | where errors are costly |
| §13 Open questions | stays open, tracked | honest gap, not a guess |

Plus the workshop's disagreement matrix: every case where two Complaint Managers judged differently becomes a mandatory human-review rule. Where experts disagree, a model must not guess.

Worked example — the `ADVERTISEMENT` placeholder in section 1d today holds one table row. After the workshop it becomes:

```markdown
#### ADVERTISEMENT

Required — all of the following must hold:      <- card §4, [REQUIRED] lines
- sender is a company, not a private person or HCP
- a product is described as intact and functioning
- no batch number, no lot number, no expiry date

Supporting — raise confidence, none required:   <- card §4, [SUPPORTING] lines
- the message offers goods or services
- mass-mailing markers: generic salutation, unsubscribe link
- no patient, no reporter, no incident

If all required hold but no supporting one does, <- card §4 combination rule
request human review instead of deciding.

Rule out `ADVERTISEMENT` — any one is enough:   <- card §5 + §10
- a defect is alleged, even if the sender is a company
- authenticity is questioned -> handle as PTC (§5.2.1.2)
- a product imitating a Bayer product is offered
  -> TRADEMARK_VIOLATION / FRAUDULENT_PRODUCT, escalate to CQH

Signal phrases:                                 <- card §6
| "request a quote"          | EN | ADVERTISEMENT |
| "unverbindliches Angebot"  | DE | ADVERTISEMENT |
```

The asymmetry carries over into the prompt: positive criteria are weighted (required vs supporting), negative ones act as single vetoes. It also feeds the confidence rating — all required plus several supporting criteria is `HIGH`; required-only is at most `MEDIUM`.

The borderline example from card §11c — a distributor offering an imitation product — does **not** become prompt text. It becomes a test case: the prompt must return `FRAUDULENT_PRODUCT` there, not `ADVERTISEMENT`. That is how a later prompt version is measured against this one.

Note on wording: the Complaint Manager materials speak of **Decision 1 / 2 / 3** and `Classification result`. This prompt and its JSON keep `axis_1…` / `axis_2…` / `axis_3…`, which are machine-facing and never seen by a CM. The mapping is: decision 1 = intake gate, decision 2 = case type, decision 3 = adverse event.

## GxP constraint

Per [SOP 1937](../../07-sop/) "Use of AI for support of GxP Process", generative AI is a **supportive tool** and does not make GxP-relevant decisions autonomously. Its output must not be adopted into GxP documentation without review by the responsible person.

The prompt implements this structurally: every output is a proposal, every axis carries a rationale with an SOP reference, and the `human_review_required` list forces a Complaint Manager decision for the sensitive cases — suspected counterfeit, any AE indication, low confidence, suspected duplicates, and contradictory signals.

## Source basis

Criteria in the prompt are traceable to:

- `SSC-PTC-SOP-001` v6.0 (IQMS-50911) — §1.1 scope, §3 definitions, §5.2 intake, §5.3.1 entry rules, Annex 3 falsification pick-list
- `GSOP 115` v15.0 (IQMS-97175) — §4.1.1 classification, CoQ definition
- URS `nonGMP-URS-FS-RA- URS for Automation platform.xlsx` — REQ-008, REQ-019…031, REQ-054…057
- `IQMS-fields.xlsx` — mandatory (`*`) vs post-investigation (`**`) fields

Source documents live in the Bayer SharePoint folder `CLARA - Complaint-Management - AI Use case`. Do not copy them into this repo.

## Related

- [promtpts for text recogniztion/](../promtpts%20for%20text%20recogniztion/README.md) — the upstream translation prompt producing this prompt's input
- [manual-test.md](../manual-test.md) — how to run a prompt by hand in myGenAssist
- [glossary.md](../../02-requirements/glossary.md) — PTC, UI, UE, CSI, CoQ, LODE and the rest
