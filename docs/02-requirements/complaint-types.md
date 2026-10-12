# Complaint types

Hierarchy of case types as defined by the SOPs in the Bayer SharePoint folder
`SOP Complaint Management (Country-Global)`. This is the **intake taxonomy**: what a
Complaint Manager has to decide when a message arrives, before anything is entered in IQMS.

Terms are defined once in the [glossary](glossary.md) and not repeated here.

> Attributes that are set **after** intake — risk classification, error codes, incident
> category, final classification — are not part of this hierarchy. They are listed
> separately under [Orthogonal axes](#orthogonal-axes-not-part-of-the-type-hierarchy).

## Sources

| Document | Version / status | Used for |
| --- | --- | --- |
| GSOP 115 | V15.0, effective 2026-01-01 | scope, definitions, case types, local closure |
| GSOP 115 | V14.0, superseded 2024-11-01 | delta only (internal complaints removed) |
| SSC-PTC-SOP-001 | V6.0, effective 2025-04-10 | GBS intake, non-PTC forwarding, Annex 3 picklist |
| BP 1429 (IUS Technical Complaints Guidance) | V5.0, effective 2025-07-15 | error code levels, UI subtype examples |
| User Letter 63 | V2.0, 2025-02-24 | Trademark Violation / Fraudulent Generic |
| User Letter 70 | V2.0, 2025-09-07 | minimum requirements, out-of-scope cases |
| User Letter 72 | V1.0, 2026-01-01 | Feedback Type `Documentation` (Betaconnect) |
| User Letter 73 | V1.0, 2025-12-08 | Feedback Type `Documentation` (Radiology FSCA) |
| SSC-PTC-SOP-RAD-007 | V4.1 | radiology specifics |

## Hierarchy

```text
Incoming message
│
├── NOT PTC-relevant — no IQMS entry, forward to the responsible function
│   │   (GSOP 115 V15 §1 "Out of scope"; UL 70 §1; SSC-PTC-SOP-001 §5.2.1.1/§5.2.2)
│   │
│   ├── General statement on a Bayer product (no alleged failure)
│   ├── Product question without allegation of defect  → MedInfo / CQU
│   │       e.g. ingredients, storage, temperature excursion
│   ├── Usability issue on drug product / cosmetic / food supplement
│   │       (UI is in scope ONLY for medical devices and the device part
│   │        of combination products — UL 70 §1)
│   ├── Product information insufficient AND reporter not contactable
│   │       (brand name, presentation, strength missing)
│   └── Bayer is neither MAH nor legal manufacturer  → handle per QAA
│
└── PTC-RELEVANT — enter in IQMS
    │   PTC = any report of a potential or alleged failure of a product in its quality
    │   (identity, durability, reliability, safety, efficacy, performance)
    │   or a suspected falsification / counterfeit  (GSOP 115 V15 §3)
    │
    ├── PTC
    │       the base case: alleged quality failure, no AE, no counterfeit suspicion
    │
    ├── PTC+AE
    │   │   a PTC or UI that carries adverse-event information or is associated
    │   │   with a PV case. ANY ONE of the criteria below is sufficient
    │   │   (GSOP 115 V15 §3; SSC-PTC-SOP-001 §5.3.2)
    │   │
    │   ├── PV case references a potential / alleged technical product defect
    │   ├── PV case relates to a suspected falsification or counterfeit
    │   ├── PV case or cluster questions product quality  → Confirmation of Quality Request (CoQ)
    │   ├── PV case refers to a medical device (regardless of incident category or lifecycle status)
    │   ├── PV case refers to the device constituent of a combination product
    │   │       with an alleged technical / quality defect
    │   └── PTC constitutes a medical device complaint with potential serious health impact
    │           — even WITHOUT an AE or special circumstances
    │
    │   Additional routes into PTC+AE:
    │   ├── Use Error directly associated with a PV case
    │   │       (off-label use, misuse, medication error — GSOP 115 V15 §5.1.1)
    │   └── LODE / LOE, only if PV raises a Confirmation of Quality Request
    │           (not required for pure LODE without sample and without batch
    │            — SSC-PTC-SOP-001 §5.3.2)
    │
    ├── UI — Usability Issue
    │   │   medical devices and device constituent of combination products only;
    │   │   entered in IQMS even with NO suspected quality defect
    │   │   (GSOP 115 V15 §3 and §5.1.1)
    │   │
    │   ├── Use Error (UE)
    │   │       act or omission with a result different from that intended by the
    │   │       manufacturer or expected by the operator; includes slips, lapses,
    │   │       mistakes. An unexpected physiological response is NOT a use error.
    │   │       e.g. instructions not followed, incorrect insertion technique
    │   │
    │   └── Customer Satisfaction Issue (CSI)
    │           dissatisfaction WITHOUT an allegation that the product fails to meet
    │           its claims. e.g. handling problems, instructions hard to understand,
    │           difficulty opening the package  (BP 1429 §7.2)
    │
    ├── Suspected Falsification / Counterfeit
    │   │   IQMS Feedback Type: "Suspected Counterfeit / Falsification"
    │   │   (GSOP 115 V15 §3 and Annex 2 picklist; SSC-PTC-SOP-001 Annex 3)
    │   │   A message merely questioning authenticity is handled as a PTC
    │   │   (SSC-PTC-SOP-001 §5.2.1.2, Remark)
    │   │
    │   ├── Falsification
    │   │   ├── False representation of identity, packaging, labelling, name or composition
    │   │   ├── Manipulation of genuine product
    │   │   │       changed variable data · removed/exchanged content · resold used product
    │   │   ├── Disappeared / Diverted product  (smuggling)
    │   │   │       genuine product rerouted out of its intended legal supply chain
    │   │   └── Disappeared / Theft / Stolen product
    │   │           genuine product taken without authorization from the supply chain
    │   │
    │   └── Counterfeit
    │       ├── Trademark Violation
    │       │       unauthorized use of tradename, trademark or icon owned by Bayer
    │       └── Fraudulent Product
    │               imitation of a "generic" of a genuine Bayer product
    │
    └── Documentation
            missing or not-sendable documents, e.g. Field Safety Corrective Action
            documents, or the Betaconnect external-legal-manufacturer route.
            Logged as Feedback Type / Error Code = Documentation.
            (UL 73 §2; UL 72)
```

## Boundary cases that are regularly misclassified

| Reported as | Actually handled as | Source |
| --- | --- | --- |
| Lost product (accidental, no intent) | regular PTC — quantity issue, **not** falsification | GSOP 115 V15 §3, Remarks |
| Suspected falsification, later assessed genuine / registered | regular PTC process | SSC-PTC-SOP-001 Annex 3, footnote ** |
| Trademark Violation / Fraudulent Generic, confirmed non-Bayer product | local closure as non-processable case | UL 63; GSOP 115 V15 §5.1.1.1 d |
| Pure AE with no product-quality allegation | PV case in ARGUS — no IQMS case type of its own | GSOP 115 V15 §3 |
| AE on an IUS without reference to breakage / deformation / malfunction / usability issue | neither IQMS entry nor investigation | UL 40 Table 1 |
| Radiology medical device PTC, PTC+AE and AE | processed in IQMS **only**, not in the PV safety database | GSOP 115 V15 §5.1.1; UL 73 §1 |
| Internal complaint (Bayer site to Bayer site) | no longer a category — handled as cross-organizational deviation | GSOP 115 V15 history (removed in V15) |

## Orthogonal axes (not part of the type hierarchy)

These are separate IQMS fields. A case carries a value on each of them *in addition to*
its type; they do not subdivide the hierarchy above.

| Axis | Values | Set when |
| --- | --- | --- |
| Complaint Type (IQMS field) | external · internal · external-Non-Bayer product | at entry — see [glossary](glossary.md) |
| Product Type | drug/medicinal product · medical device · combination product · food supplement · cosmetics · API/raw material/excipient/ingredient · other | at entry |
| Risk Classification | initial: High · Medium · Low — final: additionally Non-Justified | initially at entry, finally after investigation |
| Error codes | Level 1 object type → Level 2 error code → Level 3 error sub-code | initial at entry (CH) / by RQU, final after investigation |
| Incident category (medical devices) | Serious Incident · Non-serious incident; plus Serious Public Health Threat | per case, device products only |
| Final classification | Confirmed quality defect · Unconfirmed · Unconfirmed but plausible | after investigation |
| Complaint process type | Standard (30 d) · Non-standard (60 d) · Local Closure (30 d) | at entry, revisable |

Local closure is a process route, not a type. It is available only for UI, Documentation,
PTC or suspected falsification/counterfeit cases that meet all conditions of
GSOP 115 V15 §5.1.1.1, plus the Trademark Violation / Fraudulent Generic case of UL 63.

## Open points

- Full IQMS `Feedback Type` picklist is not reproduced in any SOP. Confirmed values so far:
  `Suspected Counterfeit / Falsification`, `Documentation`. The values behind PTC, PTC+AE
  and UI need confirmation from the IQMS configuration.
- Radiology uses additional operational categories (PQT, disposables, FSR-spreadsheet cases)
  in `SSC-PTC-SOP-RAD-007` §4.1.13/§4.1.14. Clarify whether these are case types or
  intake channels.
- `Special Situation` is used colloquially for PV *special circumstances* (off-label use,
  overdose, misuse, exposure via parent, occupational exposure). These sit in the PV case
  definition (GSOP 115 V15 §3), not in the PTC type hierarchy. Confirm the intended meaning
  before adopting the term.
