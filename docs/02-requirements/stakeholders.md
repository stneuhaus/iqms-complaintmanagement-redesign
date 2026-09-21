# Stakeholders

Prefer roles over personal names. Add people only when they have agreed to be named in this repo.

Derived from PTC shadowing, URS role abbreviations, and the [enterprise extract](../01-current-process/sources/2026-09-18-enterprise-extract-actors-systems-data-interactions.xlsx).

| Role | Organisation / site | Interest | Notes |
| --- | --- | --- | --- |
| Complaint Manager (CM) | GBS / quality intake | Final HITL before IQMS/ARGUS transfer; review category, data, completeness; send emails | URS; Zielprozess swimlane |
| PTC handlers | Poland (shadowing 2026-05-07) | Case intake, IQMS, translation, approval | Names only in source notes |
| PTC handlers | Costa Rica (shadowing 2026-05-08) | High-volume US/Canada intake; Mirena templates | ~16,000 cases/year US+CA mentioned |
| Triage (interface cases) | GBS | Triage Miidas–IQMS cases; create SSF for follow-up | Costa Rica notes |
| Approver / Owner (site) | Owning organisation | IQMS approval / investigation ownership | Synaps / SharePoint lists |
| Pharmacovigilance (PV) | PV | AE and usability+AE handoff; Argus | |
| MedInfo (Conduent / Miidas) | Partner / MedInfo | Phone complaint intake | URS REQ-002 |
| RQU | Quality | Investigation start / notification when minimum data present | URS REQ-034 |
| CQU | Country quality | Authority communication | URS REQ-044 |
| CQH / CGH | Country quality leadership | Pre-send review of some closure emails; counterfeit escalation | URS REQ-045, REQ-057 |
| Quality International | Quality | Translation quality spot-checks in hypercare | URS REQ-013 |
| Sales / pharma referents / pharmacies / HCPs | External / field | Submit complaints; SafeTrack adoption audience | URS REQ-009 |
| US department | US | Reimbursement for some products | Mirena example |
| Bayer Cyber Security Center | Security | Malware / dangerous email handling | URS REQ-055 |
| Process Owner | Quality | Process accountability | URS: Helene Janzen (named in URS, not shadowed) |
| Technical project lead | Project | Automation platform delivery | URS: Sina Sander |
| Project / automation team | TBD | n8n automation | Platform choice not yet ADRed vs Node-RED demo |

## External complainants (not stakeholders of the build, but process actors)

| Actor | Interest |
| --- | --- |
| Private person / patient | Submit complaint easily (phone, email, form) |
| HCP / physician / pharmacist | Report product issues; may receive pharmacy email / voucher |
| Authority | May send documents with reference numbers |
