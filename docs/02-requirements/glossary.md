# Glossary

Shared terms for this project. Link here instead of redefining elsewhere.

Inventory provenance: [enterprise extract (2026-09-18)](../01-current-process/sources/2026-09-18-enterprise-extract-actors-systems-data-interactions.xlsx).

| Term | Meaning |
| --- | --- |
| AE | Adverse event |
| Argus | Safety / AE reporting system; today notified manually from the complaint process; ARGUS–IQMS interface exists for misroutes |
| Awareness Date | Date when Bayer (QA or GBS) becomes aware of the complaint in a language that is understood (IQMS mandatory field) |
| CM | Complaint Manager — human-in-the-loop before fachliche Übergabe to IQMS/ARGUS |
| Complaint Type | **IQMS field name, not the taxonomy.** Holds only `external` / `internal`, and is always `external` in this process. For the actual classification see PTC, PTC+AE, UI, Suspected falsification / counterfeit |
| CoQ | Confirmation of Quality Request — a reporter, authority or PV asks for a quality confirmation; makes a case PTC+AE (GSOP 115 §3) |
| Counterfeit | Trademark violation (unauthorized use of tradename, trademark or icon) or fraudulent product (imitating a "generic" of a Bayer product). Distinct from Falsification (SSC-PTC-SOP-001 §3, Annex 3) |
| CQH / CGH | Country Quality Head — reviews some closure emails; escalation target for suspected counterfeit (URS) |
| CQU | Country Quality Unit — communication with health authorities (URS) |
| CSI | Customer Satisfaction Issue — dissatisfaction **without** an allegation that the product fails to meet claims (e.g. handling, unclear instructions); a subgroup of UI |
| Defect Category | IQMS field set **after** investigation (packaging, labeling, missing components, device defect …). Not an intake classification |
| Falsification | False representation of identity/packaging/labelling/composition, manipulation of genuine product, diversion, or theft. A *lost* product (no intent) is **not** falsification — it is a regular PTC quantity issue |
| FastTrack / Safetrack 2.0 | Planned / successor electronic submission form; must not auto-enter IQMS without assessment (URS) |
| FMD | Falsified Medicines Directive — FMD alerts arrive pre-filled in the complaint database (GSOP 1581) |
| GBS | Global Business Services (country–product lists on SharePoint in as-is notes) |
| HITL | Human-in-the-loop — Complaint Manager is final decision authority before transfer |
| Impacted organisation | Organisation impacted by / manufacturing the complained product (lookup from batch / Synaps / lists) |
| IQMS | Quality / complaint case system used to register PTCs |
| Local Closure | Case registered and closed locally after unsuccessful contact attempts; 30-day timeline, no investigation step (SSC-PTC-SOP-001 §4.1.2) |
| LODE / LOE | Lack of Drug Effect / Lack of Effect — failure to produce the expected action. May be treated as PTC+AE; PV decides |
| MedInfo | Phone intake channel (Conduent / Miidas) |
| Miidas | Interface / platform that can create IQMS cases and attachments; also phone/form intake |
| n8n | Workflow automation platform planned for this project |
| Non-Justified | Final risk classification only: non-defective product, or the investigation did not confirm the alleged defect. Never used as an initial classification |
| Owning organisation | Site / organisation responsible for investigation / registration of investigation results |
| PTC | Product technical complaint — any report of a potential or alleged failure of a product in its quality (identity, durability, reliability, safety, efficacy, performance) |
| PTC+AE | PTC or UI that includes adverse event information or is associated with a PV case; six qualifying criteria in SSC-PTC-SOP-001 §3 |
| PV | Pharmacovigilance |
| Risk Classification | High / Medium / Low, set initially and finally; plus Non-Justified for the final one only (GSOP 115 §4.1.1). Separate from case type |
| RQU | Responsible Quality Unit — notified when investigation starts with minimum data (URS) |
| ServiceNow | Ticket tool named in the URS for email intake, sorting, and CM allocation (see also SSF) |
| SSF | Service request / ticket tool used for triage, follow-up, and subprocesses in shadowing notes (confirm vs ServiceNow) |
| Synaps / SynApps | Consumer Health application / site and organisation master data (spelling varies by source) |
| Translation hub | As-is: machine translation with human check; original and translation stored as attachment |
| UE | Use Error — act or omission with a result different from that intended by the manufacturer or expected by the operator; includes slips, lapses, mistakes. An unexpected physiological response is **not** a use error. A subgroup of UI |
| UI | Usability issue (URS triage category; longer process time than PTC). Entered into IQMS even with no suspected quality defect. Subgroups: UE and CSI |
