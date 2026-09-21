# Systems and tools (as-is)

Systems named in shadowing notes. Confirm official names, owners, and environments before architecture work.

| System / artefact | Role in the as-is process |
| --- | --- |
| Email | Primary intake channel; country-specific and grouped PTC inboxes; attachments, scans, photos |
| Ticket / SSF / ServiceNow | Service request, categorization, follow-up, subprocesses (pharmacy email, reimbursement, DHL). Shadowing notes say SSF/ticket tool; URS names **ServiceNow** |
| IQMS | Complaint / PTC case; templates; IQMS ID; person and confidential attachments |
| Miidas / MedInfo (Conduent) | Phone / form intake; Miidas–IQMS interface can create the IQMS case and attachments before SSF follow-up |
| Synaps / SynApps | Consumer Health application; site database; material number, owning organisation, responsible person (spelling varies by source) |
| Pharma product lists | Pharma counterpart to Synaps for owner, division, product type, legal manufacturer, owning organisation, material number (URS) |
| SharePoint | Responsible-person lists; GBS country–product lists; as-is translation PDF handoff |
| Excel PTC tracking | Duplicates, complaint ratio, country–product |
| Product list | Product category |
| Translation hub | Machine translation plus human check (~6 h via agency / SharePoint in URS background) |
| Argus / Safetrack | Adverse event reporting (manual notify today; Argus number back into the case). ARGUS–IQMS interface for misroutes; Safetrack / Safetrack 2.0 as electronic submission (URS) |
| DHL | Sample shipping labels |
| PV | Receives usability issues that include an AE |

## Data copied between systems (pain points)

- Ticket ID, IQMS ID, Miidas number, lot / batch, Argus number
- Attachment rename to IQMS ID
- Pharmacy / physician address and other person data
- Owning and impacted organisation, responsible person, approver

## Earlier automation notes (not a decision)

A 2026-05-13 demo mentioned Veeva automation / Node-RED (building blocks, Bayer Node-RED in AWS, instances for Veeva Vault). Source note: [2026-05-13-Demo-Stefan.md](sources/2026-05-13-Demo-Stefan.md). This project’s intended implementation platform is **n8n** ([C-002](../02-requirements/constraints-and-assumptions.md)). Record the choice in `docs/06-decisions/` when it is confirmed.

## Related extract

Actors, systems, data objects, and interactions (as-is + to-be + URS): [2026-09-18-enterprise-extract-actors-systems-data-interactions.xlsx](sources/2026-09-18-enterprise-extract-actors-systems-data-interactions.xlsx).
