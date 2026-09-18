# Constraints and assumptions

## Constraints

| ID | Constraint |
| --- | --- |
| C-001 | Existing systems of record (IQMS, SSF/ticket, Argus, Synaps) stay in place unless a later decision says otherwise |
| C-002 | Implementation platform for this repository is n8n |
| C-003 | Sensitive personal data in attachments must not be copied into this git repo |

## Assumptions

| ID | Assumption | Validate by |
| --- | --- | --- |
| A-001 | First automation slice may be translation / categorization / extraction (see SharePoint MVP drawio) | Product owner |
| A-002 | Pharma and Consumer Health need the same case information, with Synaps used for Consumer Health master data | Process owners |

## Open questions

- Official system names and integration APIs
- In-scope countries and products for MVP
- Human-in-the-loop vs straight-through processing
