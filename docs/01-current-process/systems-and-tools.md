# Systems and tools (as-is)

Systems named in shadowing notes. Confirm official names, owners, and environments before architecture work.

| System / artefact | Role in the as-is process |
| --- | --- |
| Email | Primary intake channel; attachments, scans, photos |
| Ticket / SSF tool | Service request, categorization, follow-up, subprocesses (pharmacy email, reimbursement, DHL) |
| IQMS | Complaint / PTC case; templates; IQMS ID; person and confidential attachments |
| Miidas–IQMS interface | Can create the IQMS case and attachments before SSF follow-up |
| Synaps | Consumer Health application; site database; material number, owning organisation, responsible person |
| SharePoint | Responsible-person lists; GBS country–product lists |
| Excel PTC tracking | Duplicates, complaint ratio, country–product |
| Product list | Product category |
| Translation hub | Machine translation plus human check |
| Argus | Adverse event reporting (manual notify; Argus number back into the case) |
| DHL | Sample shipping labels |
| PV | Receives usability issues that include an AE |

## Data copied between systems (pain points)

- Ticket ID, IQMS ID, Miidas number, lot / batch, Argus number
- Attachment rename to IQMS ID
- Pharmacy / physician address and other person data
- Owning and impacted organisation, responsible person, approver

## Earlier automation notes (not a decision)

A 2026-05-13 demo mentioned Veeva automation / Node-RED (building blocks, Bayer Node-RED in AWS, instances for Veeva Vault). This project’s intended implementation platform is **n8n**. Record the choice in `docs/06-decisions/` when it is confirmed.
