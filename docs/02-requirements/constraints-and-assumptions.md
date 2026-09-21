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

## Assumptions

| ID | Assumption | Validate by |
| --- | --- | --- |
| A-001 | First automation slice is translation / categorization / extraction (SharePoint MVP drawio) with HITL before IQMS/ARGUS | Product owner |
| A-002 | Pharma and Consumer Health need the same case information; Synaps for CH master data, Pharma lists for Pharma | Process owners |
| A-003 | SSF (shadowing) and ServiceNow (URS) refer to the same ticket platform | Process / IT owner |
| A-004 | Existing ARGUS–IQMS and Miidas–IQMS interfaces remain the integration path for those channels (<10% of submissions per URS) | Integration owners |
| A-005 | Minimum data to start investigation includes product name, batch number, and documentation (SOP 001-115 §5.3.1.1 per URS) | Quality / SOP owner |
| A-006 | PTC transfer rule hypothesis: complete data **or** transfer at latest after 5 days — regulatory deadlines still open on the Zielprozess diagram | Quality / regulatory |

## Open questions

- Confirm official ticket tool name (SSF vs ServiceNow) and APIs
- In-scope countries and products for MVP
- Final confidence thresholds and which steps may be straight-through vs always HITL
- Regulatory transfer deadlines and final AE/PTC transfer rules
- Whether reimbursement / DHL / pharmacy email stay out of first automation slice (FR-021)
- n8n vs any Veeva/Node-RED platform reuse (ADR)
