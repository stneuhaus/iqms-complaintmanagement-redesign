# Classification rules matrix (PTC)

Status: Draft
Last reviewed: 2026-10-26

Answers the URS requirement:

> *"The solution must support classification of PTCs using the controlled categories and
> decision rules defined in the applicable approved SOP."*

This file is the **evidence base** for that requirement: for every classification axis it
lists the controlled values, the rule that assigns a value, the role that is allowed to
assign it, and the SOP clause it comes from.

Scope note: this is a *rules inventory*, not a design. It says what the SOPs require, not
how the automation implements it. The type hierarchy itself is in
[complaint-types.md](complaint-types.md); terms are defined once in the
[glossary](glossary.md). Classification capability is tracked as
[FR-008](functional-requirements.md).

---

## 1. Source documents and precedence

All documents are in `docs/07-sop/SOP Complaint Management (Country-Global)/`.

| Rank | Document | Version | Effective | Role in classification |
| --- | --- | --- | --- | --- |
| 1 | **GSOP 115** — Manage PTC and Suspected Falsification and Counterfeit | 15.0 | 2026-01-01 | Global master. Risk classes, definitions, timelines, local closure, Annex 1 examples |
| — | GSOP 115 | 14.0 | 2024-11-01 — **superseded** | Delta only; do not classify from this version |
| 2 | **SSC-PTC-SOP-001** — Manage PTC … in GBS | 6.0 | 2025-04-10 | GBS intake duties, IQMS key data, Annex 3 counterfeit picklist. Written against GSOP 115 **V14** — see [§13](#13-conflicts-and-open-points) |
| 3 | **SSC-PTC-BP-001** — Initial Risk Classification | — | — | **Not in this repo.** Named as the normative source for initial risk class and error codes in SSC-PTC-SOP-001 §1.2 / §5.3.1 |
| 4 | **BP 1429** — IUS Technical Complaints Guidance | 5.0 | 2025-07-15 | Error-code and initial-risk table for IUS products |
| 5 | Country SOPs `SSC-PTC-SOP-<ISO>-nnn` | various | various | Escalation triggers, reimbursement, data privacy, response letters. Index: `SSC_PTC_Country_SOP_Matrix.xlsx` |
| 6 | IQMS User Letters 38, 40, 46, 50, 51, 63, 69, 70, 71, 72, 73, 74 | various | various | Product- and case-specific overrides; each one wins over the general rule **for its scope only** |

**Precedence rule:** a User Letter overrides GSOP 115 only inside its declared
"Applicable to" scope. Outside that scope GSOP 115 V15 applies unchanged. Country SOPs add
local obligations; they never relax a global rule.

---

## 2. The classification axes

A complaint does not carry *one* classification. It carries a value on each of seven
independent axes, assigned at different moments by different roles.

| # | Axis | Controlled values | Assigned at | Assigned by |
| --- | --- | --- | --- | --- |
| A | Intake gate | in scope / out of scope | on reading the message | GBS/CQU |
| B | Case type (Feedback Type) | PTC · PTC+AE · UI (UE / CSI) · Suspected Counterfeit / Falsification · Documentation | at entry | GBS/CQU |
| C | Adverse event reported | yes / no | at entry | GBS/CQU, informed by PV |
| D | **Initial risk classification** | High · Medium · Low | after entry, within 3 days of task receipt | **RQU** (not GBS) |
| E | Error codes | Level 1 object type → Level 2 error code → Level 3 sub-code | initial at entry / by RQU | RQU; GBS for Consumer Health |
| F | Final risk classification | High · Medium · Low · **Non-Justified** | after investigation | RQU |
| G | Final classification (conclusion) | Confirmed quality defect · Unconfirmed · Unconfirmed but plausible | after investigation | RQU |

Axes A–C are intake decisions and are the ones an intake automation can support.
Axes D–G happen after the case leaves intake. **Axis D is explicitly an RQU task** since
GSOP 115 V14 — this is the single most common misreading of the process.

---

## 3. Axis A — Intake gate: does it enter IQMS at all?

### A.1 Out of scope — no IQMS entry

| Rule | Condition | Route to | Source |
| --- | --- | --- | --- |
| A-01 | General statement on a Bayer product, no alleged quality failure | CQU / applicable function | UL 70 §1 |
| A-02 | Product question without allegation of defect (ingredients, storage, temperature excursion) | CQU / MedInfo | SSC-PTC-SOP-001 §5.2.1.1 |
| A-03 | Usability issue (UE or CSI) on a **drug product, cosmetic or food supplement** | not processed | UL 70 §1 |
| A-04 | Relevant product information missing (brand name, presentation, strength) **and** reporter not contactable | no entry | UL 70 §1 |
| A-05 | Bayer is neither MAH nor legal manufacturer | handle per QAA | GSOP 115 V15 §1; SSC-PTC-SOP-001 §1.1 |
| A-06 | Clinical trials phase 1, 2, 3 | out of scope | SSC-PTC-SOP-001 §1.1 |
| A-07 | Internal complaint (Bayer site → Bayer site) | cross-organizational deviation, **not** a complaint category any more | GSOP 115 V15 change history |
| A-08 | Eylea PFS: unintentional mishap not related to use/handling (dropped, bumped) or contamination by patient activity (sneezing, coughing) | not processed in IQMS — does **not** qualify as Use Error | UL 50 §2.1 |
| A-09 | IUS: AE only, without reference to breakage, deformation, malfunction or usability issue | no IQMS entry, no investigation | UL 40 Table 1; BP 1429 §5 |
| A-10 | IUS: "threads not visible / unable to feel" without breakage or malfunction | no IQMS entry, no investigation | UL 40 Table 2 |
| A-11 | IUS LODE: no sample provided (with or without batch) | no IQMS entry | BP 1429 §6 |

### A.2 In scope — always enters IQMS

| Rule | Condition | Source |
| --- | --- | --- |
| A-20 | Any report of a potential or **alleged** failure of a product in its quality — identity, durability, reliability, safety, efficacy or performance | GSOP 115 V15 §3 |
| A-21 | Any suspected falsification or counterfeit | GSOP 115 V15 §3 |
| A-22 | Message explicitly questioning authenticity ("is this genuine?") — handled as PTC | SSC-PTC-SOP-001 §5.2.1.2 Remark |
| A-23 | Usability issue on a **medical device** or the device constituent of a combination product — even with no suspected quality defect | GSOP 115 V15 §5.1.1; UL 70 §1 |
| A-24 | Expired product — still entered | SSC-PTC-SOP-001 §5.3.1 |
| A-25 | FMD alerts (pre-filled in IQMS by alert operators) | SSC-PTC-SOP-001 §5.1; GSOP 1581 |
| A-26 | Nova T / Nova T 380 (class III device): **all** cases, including UI and cases with no sample and no batch | UL 51 §1 |

### A.3 Follow-up vs new case

| Rule | Condition | Result | Source |
| --- | --- | --- | --- |
| A-30 | Information relates to an already reported, still open PTC | add to communication protocol — no new case | SSC-PTC-SOP-001 §5.2.1.2 |
| A-31 | New relevant information after the case was **closed** | new follow-up case, awareness date clock restarts | GSOP 115 V15 §4.1.2; SSC-PTC-SOP-001 §5.5 |
| A-32 | Correction / adding pertinent information to an open case | amendment — awareness date **unchanged** | GSOP 115 V15 §4.1.2 |
| A-33 | Change to batch/material/part, impacted organisation, root cause, complainant, reference CAPA, investigation, immediate action, sample, root cause analysis, effectiveness check, CAPA action, extension request | amendment **not permitted** — must be a follow-up | SSC-PTC-SOP-001 §4.1.2 |
| A-34 | Breelib: new error on the same device / serial number at a later time | new PTC | UL 38 §3 |

---

## 4. Axis B — Case type

| Value | Decision rule | Source |
| --- | --- | --- |
| **PTC** | Alleged quality failure; no AE information; no counterfeit suspicion | GSOP 115 V15 §3 |
| **PTC+AE** | Any one of the criteria in [§5](#5-axis-c--adverse-event-and-ptcae-triggers) is met | GSOP 115 V15 §3 |
| **UI — Use Error** | Act or omission with a different result than intended by the manufacturer or expected by the operator. Includes slips, lapses, mistakes. An unexpected physiological response is **not** a use error | GSOP 115 V15 §3 |
| **UI — Customer Satisfaction Issue** | Expression of dissatisfaction where there is **no allegation** that the product fails to meet claims (handling problems, instructions hard to follow) | GSOP 115 V15 §3 |
| **Suspected Counterfeit / Falsification** | Per the Annex 3 / Annex 2 picklist — see [§4.1](#41-falsification-and-counterfeit-subtypes) | SSC-PTC-SOP-001 Annex 3; GSOP 115 V15 Annex 2 |
| **Documentation** | Missing or non-sendable documents, e.g. FSCA documents; Betaconnect route | UL 73 §2; UL 72 |

### 4.1 Falsification and counterfeit subtypes

| Subtype | Observable signal | Title convention | Source |
| --- | --- | --- | --- |
| Falsification — false representation | False identity, packaging, labelling, name or composition (other than unintentional quality defect) | `<product>: Suspected falsification` | GSOP 115 V15 §3, Annex 2 |
| Falsification — manipulation of genuine product | Changed variable data, removed/exchanged content, returned and resold used product | `<product>: Suspected manipulation` | GSOP 115 V15 Annex 2 |
| Falsification — diverted (smuggling) | Genuine product rerouted out of its legal supply chain by unauthorized action | `<product>: Suspected diversion` | GSOP 115 V15 Annex 2 |
| Falsification — theft / stolen | Genuine product taken without authorization, by force, misappropriation or deception | `<product>: Suspected theft/stolen product` | GSOP 115 V15 Annex 2 |
| Counterfeit — trademark violation | Unauthorized use of tradename, trademark, icon owned by Bayer | `<product>: Trademark violation` | GSOP 115 V15 §3; UL 63 |
| Counterfeit — fraudulent product | Imitation of a "generic" of a genuine Bayer product by visual aspects, close naming, or same-API claim | `<product>: Fraudulent product` | GSOP 115 V15 §3; UL 63 |

**Boundary rules — regularly misclassified:**

| Reported as | Actually classified as | Source |
| --- | --- | --- |
| Lost product (accidental, no intent) | regular PTC, **quantity issue** — not falsification | GSOP 115 V15 §3 Remarks |
| Suspected falsification, later assessed genuine/registered | regular PTC process | GSOP 115 V15 Annex 2 footnote ** |
| Trademark violation where the product is known not to be a Bayer product | assessment by GBS/CQU; local closure permitted | GSOP 115 V15 Annex 2 footnote *; UL 63 |

### 4.2 Fixed field values for trademark violation / fraudulent generic

UL 63 prescribes the complete field set — the clearest example of a fully deterministic rule:

| IQMS attribute | Value |
| --- | --- |
| Feedback Type | Suspected Counterfeit / Falsification |
| Short description | `Product / Trademark Violation / Fraudulent Generic` |
| Batch / Serial Number Status | Unknown batch / serial number — do **not** create a batch manually |
| Material Number | `UNKNOWN FRAUDULENT` |
| Impacted Organization | Fraud/Trademark violation |
| Counterfeit / Falsification Confirmed? | Yes |
| Immediate Escalation Required? | Yes — to CQH |
| Local Closure | Yes, rationale `Per Guidance Document` |
| Initial error codes L1/L2/L3 | Documentation / Documentation / Documentation |

---

## 5. Axis C — Adverse event and PTC+AE triggers

A case becomes **PTC+AE** if **any one** of these is true (GSOP 115 V15 §3):

| Rule | Trigger |
| --- | --- |
| C-01 | A PV case references a potential or alleged technical product defect |
| C-02 | A PV case relates to a suspected falsification or counterfeit |
| C-03 | A PV case or cluster questions product quality → Confirmation of Quality Request |
| C-04 | A PV case refers to a **medical device** — regardless of incident category or lifecycle status |
| C-05 | A PV case refers to the device constituent or component of a combination product with an alleged technical/quality defect |
| C-06 | A PTC constitutes a medical device complaint with potential serious health impact — **even without** an AE or special circumstances |

Additional routes into PTC+AE (SSC-PTC-SOP-001 §5.3.2; GSOP 115 V15 §5.1.1):

| Rule | Trigger | Note |
| --- | --- | --- |
| C-10 | Technical product defect reported with a PV case | regardless of whether batch or sample is available |
| C-11 | Suspicion of counterfeit, theft or diversion with a PV case | as above |
| C-12 | Use error **directly associated** with a PV case (off-label use, misuse, medication error) | |
| C-13 | LODE / LOE, **only if** PV raises a Confirmation of Quality Request | pure LODE with no sample and no batch does **not** require PTC+AE |

### 5.1 Confirmation of Quality Request — pre-requisites

A CoQ needs at least one of: batch number · complaint sample · monitoring observation
(e.g. AE cluster detected by PV). Exception: critical safety/quality cases with a suspicion
of causal relationship to a product quality issue (GSOP 115 V15 §3).

### 5.2 Product-specific AE rules

| Product | Rule | Source |
| --- | --- | --- |
| IUS (Mirena, Jaydess/Skyla, Kyleena, Fleree, Janess, LNG-IUS) | AE alone (perforation, embedment, expulsion, bleeding, infection, medication error, dislocation, pain, pregnancy, lack of effect) **without** reference to breakage, deformation, malfunction or usability issue → no IQMS entry, no investigation | UL 40 Table 1 |
| IUS | Failed insertion / complication of insertion without breakage or malfunction → IQMS entry **yes**, investigation **no**, closed as unprocessable | UL 40 Table 2 |
| Breelib, patient < 18 | PTC of device only → IQMS yes / Argus no. PTC + AE → both. PTC + off-label use of Ventavis → IQMS PTC only **and** Argus PV-only case, **not linked** | UL 38 §4 |
| Eylea PFS | Increased IOP / ocular hypertension reported as AE → PV may request PTC investigation regardless of causality | UL 50 §2.2 |
| Radiology medical devices | PTC, PTC+AE and AE processed in IQMS **only** — not in the PV safety database | GSOP 115 V15 §5.1.1; UL 73 |

---

## 6. Axis D — Initial risk classification

**Controlled values: High · Medium · Low.** `Non-Justified` is explicitly *"not to be
used"* for the initial classification (GSOP 115 V15 §4.1.1).

**Assigned by RQU**, within three days of receiving the task. GBS/CQU is informed via a
report if the initial class is High or Medium (GSOP 115 V15 §5.2.1).

| Value | Decision rule (initial) | Source |
| --- | --- | --- |
| **High** | Complaints regarding **potential** defects which are potentially life-threatening or could cause a serious risk to health | GSOP 115 V15 §4.1.1 |
| **Medium** | Complaints regarding potential defects which could cause illness or mistreatment with potentially non-serious medical consequences, but are not classified as High | GSOP 115 V15 §4.1.1 |
| **Low** | Complaints regarding potential defects which may not pose a significant hazard to health | GSOP 115 V15 §4.1.1 |

### 6.1 Worked examples (GSOP 115 V15 Annex 1)

Most examples are taken from *EMA — Compilation of Union Procedures on Inspections and
Exchange of Information, EMA/369583/2023 Rev 19.1*.

| High | Medium | Low |
| --- | --- | --- |
| Wrong product (label and contents are different products) | Mislabeling (wrong or missing text or figures) | Unclear labelling, minor labelling errors (wrong/missing batch number or expiry date) |
| Correct product, wrong strength, with serious medical consequences | Missing or incorrect information on labels, leaflets, pack inserts | Over-labelling of expiry dates executed incorrectly |
| Microbial contamination of sterile injectable or ophthalmic products, or of any product administered to immuno-compromised patients | Microbial contamination of products intended to be non-sterile, non-serious consequence | Faulty closures with no increased risk to product quality |
| Chemical contamination with serious medical consequences | Chemical/physical contamination (significant impurities, cross contamination, particles) | Contamination, e.g. microbial spoilage, dirt, detritus, particulate matter |
| Mix-up of products **within a pack** (two blister strips in one carton; two tablets in one strip) | Mix-up of very similar products where the mix-up poses no clinical risk | Broken immediate container identified **before** application |
| Wrong active substance in a multi-component product, serious consequences | Non-compliance with specification (assay, stability, fill/weight) with risk of lack of efficacy or toxicity | Under-/over-filled containers posing no clinical risk |
| Presence of particles in injectable medicinal products | Unsecured closure with non-serious medical consequences | Single case of mislabeling; occasional empty blister; occasional lack of printed material |
| Batch- or product-related **serious adverse reactions** (new in V15) | | Damaged or contaminated secondary packaging; insignificant printing error; insignificant occasional device defect |
| High environment risk | | Diverted genuine or fraudulent products **without** potentially significant health risk |
| High risk to those who may administer the product | | |

Note the Medium column uses the phrase *"not classified as critical"* while the definition
table says *"not classified as high"* — see [§13](#13-conflicts-and-open-points).

### 6.2 Product-specific initial-risk decision tables

These tables assign the initial risk class deterministically from the complaint reason —
the only place in the SOP set where that is the case.

| Product family | Document | What it fixes |
| --- | --- | --- |
| Copper IUD — Nova T / Nova T 380 | UL 51 Table 1 | Complaint reason → L1/L2/L3 error codes → **initial risk class** → AE type incl. incident category |
| IUS — Mirena, Jaydess/Skyla, Kyleena | BP 1429 §4.3 | Complaint reason → object type / error code / sub-code → sample required → **initial risk category** |
| Eylea 2 mg / 8 mg PFS | UL 50 Tables 1–2 | Reported complaint → L1/L2/L3 → picture required → sample return → **initial risk class** → manufacturing site |
| Breelib | UL 38 Table 2 | Complaint as reported → key terms for Title → L1/L2/L3 error coding (no risk class) |

Illustrative rows from UL 51 — note how the *same* defect changes class with the moment it occurred:

| Complaint reason | L1 | L2 | L3 | Initial risk | AE type / incident category |
| --- | --- | --- | --- | --- | --- |
| T-body loop breakage during loading, insertion, use in situ or removal | Copper IUD | Damage to T-body loop | (respective phase) | **Medium** | Serious incident |
| T-body loop breakage during loading, patient not involved | Copper IUD | Damage to T-body loop | During loading / Other | **Low** | Non-serious incident |
| Contamination inside package, **not** used for insertion | Copper IUD | Contamination / Foreign matter | Contamination or foreign material in package/device | **Low** | Non-serious incident |
| Contamination inside package, **used** for insertion | Copper IUD | Contamination / Foreign material | Contamination or foreign material in package/device | **Medium** | Serious incident |
| Blister damaged / lack of sterility, not used for insertion | Copper IUD | Received damaged | Sterile packaging, other damages / seam open | **Low** | Non-serious incident |
| Blister damaged / lack of sterility, **used** for insertion | Copper IUD | Received damaged | as above | **Medium** | Serious incident |
| LOE (lack of effect) | — | — | — | **Medium** | Serious incident — pregnancy incl. ectopic |

Override rule from UL 50: *if PV reports a serious incident, the case must be categorised
as **Medium***, regardless of the table value (UL 50 Table 1 footnote a).

---

## 7. Axis E — Error codes

Three levels, in this order (BP 1429 §4.3; UL 38 §6; UL 51 Table 1):

| Level | Name | Example |
| --- | --- | --- |
| Level 1 | Object type | `Copper IUD`, `Folding box`, `Syringe`, `Blister`, `Administration Device` |
| Level 2 | Error code | `Damage to T-body loop`, `Handling issue`, `Malfunction`, `Print/Labelling`, `Quantity`, `Use error`, `Customer Satisfaction Issue` |
| Level 3 | Error sub-code | `Threads broke during insertion`, `Power Up Fault`, `Variable data missing`, `Leaflet missing` |

| Rule | Condition | Source |
| --- | --- | --- |
| E-01 | Error codes are entered by the **RQU** | BP 1429 §4.3; GSOP 115 V15 §5.2.1 |
| E-02 | **Exception — Consumer Health:** GBS classifies initial error codes at entry, from the drop-down, per complaint description. Multiple codes may be added | SSC-PTC-SOP-001 §5.3.1 |
| E-03 | Normative source for initial error codes and risk class is **SSC-PTC-BP-001** | SSC-PTC-SOP-001 §1.2, §5.3.1 |
| E-04 | Select the most specific code available | BP 1429 §7.2 |
| E-05 | Final error code is set after investigation, based on its results | SSC-PTC-SOP-001 §5.5 |
| E-06 | Medical devices: FDA / IMDRF evaluation codes reviewed for cases with potential serious health impact. Device Problem codes **no longer** required as of V15 | GSOP 115 V15 §5.3.1 and change history |

---

## 8. Axes F and G — Final classification

Both are set after investigation and are **out of scope for intake automation**. Listed for
completeness, since the same controlled vocabulary appears in IQMS at intake time.

### F — Final risk classification

| Value | Rule | Source |
| --- | --- | --- |
| High | Defects which are potentially life-threatening or could cause a serious risk to health | GSOP 115 V15 §4.1.1 |
| Medium | Defects which could cause illness or mistreatment with potentially non-serious medical consequences, not classified as High | GSOP 115 V15 §4.1.1 |
| Low | Defects **or alleged defects** which may not pose a significant hazard to health | GSOP 115 V15 §4.1.1 |
| **Non-Justified** | Non-defective product, or the investigation did not confirm the alleged defect. Defect reports which could not be substantiated. **Final classification only**, and only for unconfirmed defects | GSOP 115 V15 §4.1.1, Annex 1; SSC-PTC-SOP-001 §5.5 |

Radiology special rule: a radiology medical device complaint determined to be an
unconfirmed quality defect is marked `Non-justified`; the severity category always depends
on the final patient outcome (GSOP 115 V15 §4.1.1).

### G — Conclusion

| Value | Rule | Source |
| --- | --- | --- |
| Confirmed quality defect | The alleged defect could be confirmed **and** the root cause is within Bayer responsibility | GSOP 115 V15 §4.1.4 |
| Unconfirmed quality defect | The alleged defect is unconfirmed, **or** the root cause is not within Bayer responsibility | GSOP 115 V15 §4.1.4 |
| Unconfirmed quality defect, but plausible | Can neither be confirmed nor ruled out by the RQU as within Bayer responsibility, but a quality issue is considered plausible | GSOP 115 V15 §4.1.4 |

---

## 9. Process-type classification (drives the timeline)

Not a quality classification, but a controlled choice made at intake that sets the due date.

| Process type | Condition | Initiation | Investigation | Approval/closure | Total |
| --- | --- | --- | --- | --- | --- |
| **Standard** | default | 5 d | 20 d | 5 d | **30 d** |
| **Non-standard** | third party / CMO / external lab involved · sample requested but not received within the data-entry timeline · sample shipment is difficult · extension of investigation or testing required | 5 d | 50 d | 5 d | **60 d** |
| **Local closure** | see [§10](#10-local-closure) | 30 d | — | — | **30 d** |

All days are **calendar days** from the awareness date (GSOP 115 V15 §4.1.2).

| Rule | Condition | Source |
| --- | --- | --- |
| T-01 | Immediate escalation within 24 h for serious public health threats, potentially life-threatening cases, cases potentially requiring a FAR | GSOP 115 V15 §4.1.2 fn 4 |
| T-02 | Radiology medical devices: immediate escalation to RQU if the complaint alleges **Death, Air Injection or Extravasation** | GSOP 115 V15 §4.1.2 fn 4; UL 73 §1 |
| T-03 | Awareness date = the day the Bayer Quality function becomes aware of the initial complaint or of follow-up information | GSOP 115 V15 §4.1.2 |
| T-04 | Non-hosted languages: awareness date starts when the GBS team acknowledges the **translated** text. Translation office delivers within max 6 h; translations are prioritised over new mail | SSC-PTC-SOP-001 §4.1.2 |
| T-05 | Cases via Argus / MIIDAS interface: the interface sets the awareness date from the system timestamp. GBS/CQU **may adjust** it to the first applicable working day of the intake organisation (weekends, public holidays, out-of-hours) | UL 74 |
| T-06 | No batch and no photos, but complainant agrees to keep the sample: the case may stay in `Initiated` until sufficient information arrives; the awareness date is then updated and a comment added to the communication protocol | GSOP 115 V15 §4.1.2 fn 5; UL 70 §3 |
| T-07 | Due date extension allowed with interim report and justification — but every complaint must be finally closed after **90 days** at the latest. Beyond 90 days the case is overdue and GBS/CQU is notified | GSOP 115 V15 §4.1.2 |
| T-08 | Emails are read first-in–first-out | SSC-PTC-SOP-001 §4.1.2 |

---

## 10. Local closure

A routing decision, not a type. GSOP 115 V15 §5.1.1.1 permits it only for cases associated
with **(a)** usability issues, **(b)** documentation, **(c)** PTC or suspected falsification
/ counterfeit, or **(d)** trademark violation / fraudulent generic.

| Rule | Condition | Source |
| --- | --- | --- |
| L-01 | Legal manufacturer was informed | GSOP 115 V15 §5.1.1.1 |
| L-02 | **or**: no complaint sample available **and** no photo of the sample can be sent **and** no batch/serial data reported after three documented attempts **and** no AE was reported | GSOP 115 V15 §5.1.1.1 |
| L-03 | (d) Trademark violation / fraudulent generic confirmed **not** to be a Bayer product or produced by any Bayer site or third party on Bayer's behalf | GSOP 115 V15 §5.1.1.1 d; UL 63 |
| L-04 | A rationale for the local closure must be recorded, with the three documented attempts | GSOP 115 V15 §5.1.1.1 |
| L-05 | A locally closed complaint still gets a **risk classification according to its criticality** | GSOP 115 V15 §5.1.1.1 Remark |
| L-06 | **Not permitted:** all class III device cases (Essure, Nova T) must be assigned to the RQU | SSC-PTC-SOP-001 §5.3.1.1 |
| L-07 | **Not permitted:** Breelib — do not close locally (including use errors), so that reporting to Vectura stays possible | UL 38 §3 |
| L-08 | **Required:** Betaconnect — PTC closed locally; PTC+AE forwarded to PV, Global Safety Database number referenced, then closed locally without investigation | UL 72 |
| L-09 | Eylea 2 mg PFS: "condensation in the blister" and "air bubbles in solution" are known UE/CSI — no investigation, local closure with justification `Per Guidance Document`. **Not applicable** to 8 mg PFS (OcuClick) | UL 50 §2.3 |

---

## 11. Bundling

| Rule | Condition | Source |
| --- | --- | --- |
| B-01 | Suspected falsification/counterfeit from test purchases or serialization alerts, **initial classification Low**, related to one single product, one single batch, one single country (multi-country pack located in "EU" counts as one country), received on the same day | GSOP 115 V15 §5.1.1 |
| B-02 | Social-media-triggered complaints or complaints from marketing studies: same defect, short time frame, one single country, assessed as unconfirmed quality defect, in alignment with the divisional quality function | GSOP 115 V15 §5.1.1 |
| B-03 | Bundled cases are collected under **one** case for one product with a short description. Alert operators create the daily entry for falsification/counterfeit; GBS/CQU for social media | GSOP 115 V15 §5.1.1 |

Note: SSC-PTC-SOP-001 §5.3.1 still names classification **Medium and Low** for serialization
alerts and offers three handling options including "aggregate monitoring". GSOP 115 V15
narrows this to **Low** and removes the third option — see [§13](#13-conflicts-and-open-points).

---

## 12. Escalation and routing triggers at intake

These are classification-driven actions, not classifications. Included because the intake
decision and the routing decision are made in the same moment.

| Trigger | Action | Source |
| --- | --- | --- |
| PTC or suspected falsification/counterfeit carries information of a (potential) PV case / AE / LODE | forward to PVCH **immediately** | GSOP 115 V15 §5.1.2 |
| Medical device complaint with potential serious health impact | forward to PVCH immediately, with the IQMS case number and all follow-up information | GSOP 115 V15 §5.1.2 |
| Case potentially life-threatening or could cause serious risk to health | escalate immediately to the divisional **Gatekeeper** | GSOP 115 V15 §5.1.2 |
| PV case involves a PTC; CoQ raised; local authorities involved; potential falsification/counterfeit | inform the **CQU** immediately | GSOP 115 V15 §5.1.2 |
| Suspected falsification and counterfeit; complaints from local health authorities; complainant intends to inform the health authorities | inform **CQH and CQU** immediately via IQMS | SSC-PTC-SOP-001 §5.3.5 |
| Suspected counterfeit (incl. trademark violation / fraudulent generic) | forward to the named contacts — PH: Christian Schalk; CH: Max Wenger / Kristina Kersten; social media PH/CH: Petra Luh | UL 63 |
| Country-specific additions (example Germany) | notify CQH/CQU for: suspected counterfeit and FMD cases · any case involving health authorities · **final risk category High or Medium** · any case involving a lawyer or lawsuit · any case involving media. Global Anti-Counterfeit Team `acf@bayer.com` and local PV also notified for counterfeit cases | SSC-PTC-SOP-DE-012 §4.1.3 |
| Malware / dangerous email | Bayer Cyber Security Center | URS REQ-055 (not in the SOPs) |

Country-specific escalation rules differ per country. The index of all 35 country SOPs is
`SSC_PTC_Country_SOP_Matrix.xlsx` in the SOP folder; the escalation column is **not yet
extracted** for most countries.

---

## 13. Conflicts and open points

| # | Issue | Impact | Proposed resolution |
| --- | --- | --- | --- |
| O-01 | **SSC-PTC-BP-001 "Initial Risk Classification" is not in this repo.** It is named by SSC-PTC-SOP-001 §1.2 and §5.3.1 as the normative source for initial risk class and error codes | The single most important document for axis D and axis E is missing. Any rule set built without it is incomplete | Request the document from Quality before the classification design is frozen |
| O-02 | **SSC-PTC-SOP-001 V6.0 is written against GSOP 115 V14**, which was superseded on 2026-01-01 | Risk of classifying from a stale rule | Treat GSOP 115 V15 as authoritative wherever the two differ. Ask Quality when SSC-PTC-SOP-001 V7 is due |
| O-03 | **Local closure condition logic.** SSC-PTC-SOP-001 §5.3.1.1 reads as *legal manufacturer informed **AND** no sample AND no photo AND no batch AND no AE*. GSOP 115 V15 §5.1.1.1 reads as *legal manufacturer informed **OR** (no sample AND no photo AND no batch AND no AE)* — the V15 change history confirms "separate possibility … in case of informing the legal manufacturer" | Changes which cases may be closed locally | Confirm the V15 reading (OR) with Quality and record it as an assumption |
| O-04 | **Bundling threshold.** SSC-PTC-SOP-001 §5.3.1 says Medium **and** Low; GSOP 115 V15 §5.1.1 says Low only. SSC-PTC-SOP-001 also keeps a third option ("aggregate monitoring") that V15 does not list | Affects how serialization alerts are grouped | Follow V15 (Low only, two options) |
| O-05 | **"not classified as critical" vs "not classified as high"** in the Medium definition — Annex 1 of GSOP 115 V15 uses "critical", the §4.1.1 table uses "high". `Critical` is not a controlled value anywhere | Wording only, but it reads as a fourth class | Treat as an editorial defect in V15; use "high". Report to the document owner |
| O-06 | **Country-specific classification deltas are not extracted.** Only Germany was read for this matrix; 34 further country SOPs exist | A country may carry additional escalation or entry rules that change the intake decision | Extract the escalation and entry columns of `SSC_PTC_Country_SOP_Matrix.xlsx` for all countries that the first slice covers |
| O-07 | **IQMS `Feedback Type` picklist is not reproduced in any SOP.** Confirmed values so far: `Suspected Counterfeit / Falsification`, `Documentation` | The controlled vocabulary for axis B cannot be fully stated from the SOPs | Export the picklist from the IQMS configuration |
| O-08 | **Error-code catalogues are per product family and not global.** UL 50 references an external "Eylea PFS Defect Catalogue" not included here | Level 1–3 values cannot be enumerated completely | Obtain the IQMS error-code catalogue export; treat the product-specific tables as overrides on top of it |
| O-09 | **Role boundary.** GSOP 115 V14 moved initial risk classification from GBS/CQU to RQU; Consumer Health initial **error codes** remain a GBS task (SSC-PTC-SOP-001 §5.3.1) | An intake automation must not propose an initial risk class as if it were a GBS output | Confirm with Quality which axes intake may pre-fill and which stay RQU-only |

---

## 14. What this means for the solution

Stated as findings, not as design. The design belongs in `docs/05-design-spec/`.

1. **Only axes A, B and C are intake decisions.** Initial risk classification (D) is an RQU
   task performed after the case is entered. A solution that proposes a risk class at
   intake is proposing something the SOP does not ask intake to produce — except for
   Consumer Health error codes (E-02) and the locally-closed-case criticality rating (L-05).
2. **Most rules are deterministic given observable facts in the message** — product family,
   whether a sample or batch is present, whether an AE is mentioned, whether insertion had
   already happened. That is what the product-specific tables in UL 50 / UL 51 / BP 1429
   encode. These are the strongest candidates for rule-based support.
3. **The exceptions are product-scoped, not global.** Any classification support has to
   resolve the product family first, then apply the matching User Letter, then fall back to
   GSOP 115 V15.
4. **Three documents are missing before the rule set can be called complete:**
   SSC-PTC-BP-001, the IQMS error-code catalogue, and the IQMS Feedback Type picklist
   (O-01, O-07, O-08).
5. **GxP constraint.** Use of AI in this GxP process is governed by `SOP 1937 — Use of AI
   for support of GxP Process` (in `docs/07-sop/`), which this matrix does not cover. The
   HITL requirement [C-005](constraints-and-assumptions.md) stands independently of how
   good the classification rules are.
