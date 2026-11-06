# Constraints and assumptions

## Constraints

| ID | Constraint |
| --- | --- |
| C-001 | Existing systems of record (IQMS, ticket/SSF/ServiceNow, Argus, Synaps/SynApps, Pharma lists) stay in place unless a later decision says otherwise |
| C-002 | Implementation platform for this repository is **n8n** (Node-RED / Veeva automation demo of 2026-05-13 is exploratory only until an ADR says otherwise) |
| C-003 | Sensitive personal data in attachments must not be copied into this git repo |
| C-004 | No automatic IQMS entry from Safetrack / FastTrack 2.0 without an assessment gate (URS REQ-007; GBS duplicate concern) |
| C-005 | Complaint Manager remains final decision authority before fachliche Übergabe (Zielprozess HITL note) |
| C-006 | Source Draw.io binaries stay in Bayer SharePoint; link, do not duplicate, unless explicitly asked |
| C-007 | Veeva QMS has **no standard four-eyes review on an outbound email**. *Preview Email* is sender self-check only. A review gate must be built via lifecycle state or via an approved Vault document ([QA Q4](../infos/veeva-email-intake-qa-en.md)) |
| C-008 | In General Release (26R2), the *Send External Notification* dialog allows changing **recipients and documents only** — not subject or body. Free-text follow-up requires 26R3 LR or a token-fed record field ([QA Q4](../infos/veeva-email-intake-qa-en.md)) |
| C-009 | Reply-to-intake matching is **header-based only** (message ID / root message ID). A reporter who writes a fresh mail instead of replying produces a new record, not a match ([QA Q5](../infos/veeva-email-intake-qa-en.md)) |
| C-010 | Follow-up reply ingestion requires **auto-forwarding** from the Bayer mail system; redirect breaks thread matching. Forwarding may also break SPF/DKIM unless the forwarder is SRS/ARC-capable |

## Assumptions

| ID | Assumption | Validate by |
| --- | --- | --- |
| A-001 | First automation slice is translation / categorization / extraction (SharePoint MVP drawio) with HITL before IQMS/ARGUS | Product owner |
| A-002 | Pharma and Consumer Health need the same case information; Synaps for CH master data, Pharma lists for Pharma | Process owners |
| A-003 | SSF (shadowing) and ServiceNow (URS) refer to the same ticket platform | Process / IT owner |
| A-004 | Existing ARGUS–IQMS and Miidas–IQMS interfaces remain the integration path for those channels (<10% of submissions per URS) | Integration owners |
| A-005 | Minimum data to start investigation includes product name, batch number, and documentation (SOP 001-115 §5.3.1.1 per URS) | Quality / SOP owner |
| A-006 | PTC transfer rule hypothesis: complete data **or** transfer at latest after 5 days — regulatory deadlines still open on the Zielprozess diagram | Quality / regulatory |
| A-007 | Follow-up correspondence per individual question (not just per intake) requires **26R3**, currently Limited Release only. Assumed reachable within project timeline | Veeva / IQMS platform owner — confirm POD and release track |
| A-008 | Two inbound mailboxes are acceptable operationally: one for first contact (*Create Complaint*), one for follow-up replies (*Complaint Intake Follow-Up Email Processor*), plus a reply-to address in the Bayer mail system | IT / mail operations |
| A-009 | *Allowed Senders* = *All Users & Persons in this Vault* works on the follow-up mailbox because the actual sender is the forwarding Bayer system, not the external reporter | **Verify in DEV** — most fragile link in the chain |
| A-010 | Duplicate rate from unmatched replies (reporter writes fresh mail) is low enough for manual merge in triage | Measure in pilot before go-live |

## Open questions

- Confirm official ticket tool name (SSF vs ServiceNow) and APIs
- In-scope countries and products for MVP
- Final confidence thresholds and which steps may be straight-through vs always HITL
- Regulatory transfer deadlines and final AE/PTC transfer rules
- Whether reimbursement / DHL / pharmacy email stay out of first automation slice (FR-021)
- n8n vs any Veeva/Node-RED platform reuse (ADR)
- **Is four-eyes review of outbound follow-up emails a hard requirement?** Decides the whole design: fully pre-formulated templates (review the template once as configuration) vs approved Vault document for the content needing approval. Blocks lifecycle configuration — see C-007, C-008 and [QA Q4](../infos/veeva-email-intake-qa-en.md). Candidate for an ADR
- **Which release track does the IQMS Vault run on, and when does 26R3 arrive?** Determines whether follow-up replies can be mapped to the individual question (26R3 LR) or only to the intake (GR) — see A-007 and [QA Q5](../infos/veeva-email-intake-qa-en.md)
- Acceptable handling for unmatched replies that create duplicate intakes (manual merge vs detection rule) — see A-010
