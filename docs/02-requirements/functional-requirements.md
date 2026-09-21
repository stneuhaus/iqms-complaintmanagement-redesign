# Functional requirements

Status: collecting. IDs are stable; wording will be refined until this folder is **Agreed**.

Sources: as-is shadowing, URS (`nonGMP-URS-FS-RA- URS for Autoamtion platform.xlsx`, REQ-001…063), MVP Zielprozess draw.io. Capability inventory also in the [enterprise extract](../01-current-process/sources/2026-09-18-enterprise-extract-actors-systems-data-interactions.xlsx).

When writing a requirement: one capability, testable, no n8n node names.

| ID | Requirement | URS / source | Priority | Status |
| --- | --- | --- | --- | --- |
| FR-001 | Receive complaints from country-specific and grouped email inboxes; consolidate into processable intake without losing country-of-origin signal | REQ-003…005, REQ-010; as-is | Must | Draft |
| FR-002 | Accept complaints already created via ARGUS–IQMS and Miidas–IQMS interfaces into the same processing path | REQ-001, REQ-002; Costa Rica | Must | Draft |
| FR-003 | Support future Safetrack / FastTrack 2.0 electronic submission (structured email, IQMS interface, or XML/JSON/CSV) **without** automatic IQMS entry; stage for spam / ads / cyber assessment | REQ-006, REQ-007 | Should | Draft |
| FR-004 | Detect and flag potential duplicates and follow-ups (wording, photo, patient+product+batch, or related emails weeks later); require human assessment before IQMS entry | REQ-008, REQ-020, REQ-022, REQ-024, REQ-028, REQ-031 | Must | Draft |
| FR-005 | Create or update a ticket / service request; attach or version inbound email content; enable CM assignment and follow-up | REQ-041; as-is SSF; Zielprozess | Must | Draft |
| FR-006 | Translate non-English complaint text and attachments (PDF, photo, scan, screenshot, handwriting) to English; retain original and translation | REQ-011…018; Poland; Zielprozess | Must | Draft |
| FR-007 | Extract structured complaint data from email body, attachments, and forms for IQMS field population | REQ-039, REQ-058; Zielprozess | Must | Draft |
| FR-008 | Classify inbound items (at least PTC, AE, PTC+AE, Spam; also ads, non-PTC product question, stability, reimbursement, divested product, UI per URS) and prevent non-PTC from entering IQMS | REQ-019, REQ-021, REQ-023, REQ-026; Zielprozess | Must | Draft |
| FR-009 | Route non-PTC product-related items to the correct function (AE→PV, questions→MedInfo, stability→CQ, reimbursement→Sales); escalate malware to Cyber Security; escalate suspected counterfeit to CQH | REQ-027, REQ-054…057 | Must | Draft |
| FR-010 | Assess completeness against IQMS mandatory intake fields; score / expose confidence for CM review | REQ-025; Zielprozess confidence bands | Must | Draft |
| FR-011 | Provide HITL review of category, extracted data, and completeness before transfer to IQMS or ARGUS | Zielprozess; URS HITL for PII ambiguity | Must | Draft |
| FR-012 | When mandatory data is missing, generate template-based follow-up emails (up to 3 attempts, timing rules), track attempts and 5-day intake due date; CM reviews and sends | REQ-032, REQ-042…043, REQ-050…053; Zielprozess | Must | Draft |
| FR-013 | Transfer approved PTC cases into IQMS with mapped fields; write IQMS ID (and ARGUS ID when applicable) back to the ticket; set transferred flag | REQ-058, REQ-063; as-is ID round-trip; Zielprozess | Must | Draft |
| FR-014 | Enrich product / org fields from Synaps (Consumer Health) and Pharma lists (owner, division, product type, legal manufacturer, owning organisation, material / catalog) | REQ-059…061; Poland | Must | Draft |
| FR-015 | Distinguish patient vs reporter personal data; detect sensitive PII in attachments; store in IQMS personal/confidential section; HITL if ambiguous | REQ-035…037, REQ-040; Costa Rica | Must | Draft |
| FR-016 | Upload email body and attachments to the correct IQMS sections; store files for long-term availability in IQMS | REQ-038, REQ-048, REQ-063; Costa Rica rename-to-IQMS-ID | Must | Draft |
| FR-017 | Transfer AE and PTC+AE per defined rules to ARGUS (and IQMS when both); use existing ARGUS–IQMS interface where applicable | REQ-001; Zielprozess; as-is manual Argus today | Must | Draft |
| FR-018 | Allow local closure / incomplete registration after unsuccessful contact attempts when information remains insufficient; start investigation and notify RQU when minimum data is present within regulatory timing | REQ-033, REQ-034 | Should | Draft |
| FR-019 | Generate SOP-template communications (acknowledgement, missing info, closure feedback); support CQH pre-review where required by country list; keep conversation thread | REQ-042…047, REQ-049 | Should | Draft |
| FR-020 | Communicate with CQU for regulatory reporting obligations | REQ-044 | Should | Draft |
| FR-021 | Support ticket-side subprocesses still in as-is scope for MVP boundary decision: pharmacy email, reimbursement, DHL sample label | as-is Poland | Could | Draft |

## Out of scope for FR wording (track elsewhere)

- Training / change management for electronic form adoption (URS REQ-009) — organisational, not system FR
- Choosing n8n vs Node-RED runtime — ADR when decided
