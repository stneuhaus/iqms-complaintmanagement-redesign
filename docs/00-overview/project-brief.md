# Project brief

Status: Draft
Last reviewed: 2026-11-03

**Project:** iqms-complaintmanagement-redesign

## Purpose

(Project ***CLARA* Complaint **L**ifecycle **A**I-(supported) **R**eview-**A**utomation)

Complaint email  intake currently relies on the manual review and interpretation of incoming emails and a wide range of unstructured attachments, including photographs, scanned forms, and supporting documents. Project CLARA is designed to establish an automated, standardized intake process in which n8n , Bayer’s globally available automation platform, orchestrates the workflow and myGenAssist  (mGA) analyzes the submitted content.
Relevant information, including patient and reporter details, product and batch data, adverse events, and event descriptions, is identified, extracted, and converted into a structured format. The objective is to reduce manual processing effort, enhance data quality and consistency, and provide Complaint Managers with a complete, review-ready record for efficient downstream processing.
As the submitted content may include personal data and special categories of personal data, particularly patient health information, it must be processed in accordance with applicable data protection and security requirements. n8n securely transfers the emails and attachments, together with a task-specific prompt, to a Bayer-approved AI system (mGA). The AI system analyzes the submitted content and returns the relevant complaint information in a structured, machine-readable format for further processing.**

****Target architecture.** Project CLARA replaces the existing SSF ticketing tool with the Veeva Complaint Intake Module as the system of record for inbound complaint emails. At full rollout, the module will be configured with approximately 50–100 country- or group-specific intake email addresses, each forwarding into its corresponding "pond" (intake Complaint object) in IQMS. The configuration enforces a clear separation between the different intake addresses, so that Human Agents only ever see notifications for the inboxes they are responsible for. It also allows follow-up request emails to be drafted and sent directly from IQMS, with incoming replies unambiguously linked back to the originating notification.**

****Automated processing (n8n).** As soon as an intake Complaint object exists, n8n takes over its processing in the following steps:**

1. ***Structured text extraction* from the email body and attachments (photos, scans, PDFs), invoking an OCR step via Microsoft Azure Document Intelligence or a suitable LLM where required.**
2. ***Translation*: if the extracted text is not in English, the email and attachment content is translated into English by a suitable LLM to enable downstream handling by Human Agents. Original files are preserved unchanged; translations are not required to preserve layout, but must preserve the structure of the original text.**
3. ***Triage*: at the latest at this point, the AI determines whether the item is a complaint and, if so, which complaint type applies. For non-complaints, it distinguishes malware, advertising and other unwanted messages from genuine inquiries. The result is stored as a classification on the intake Complaint object.**
4. ***Data extraction and mapping*: once the text is available in English, mandatory data (e.g., country, product, batch number) is extracted and written to the corresponding fields of the intake Complaint object.**
5. ***Email drafting*: if a PTC-classified intake Complaint object is missing mandatory information, a reply email draft is generated and attached to the object; this step ends n8n's automated processing for that item.**

****Human Agent review.** From this point, a Human Agent takes over: deciding whether further information needs to be requested, and confirming or correcting the classification (PTC, PTC+AE, AE, non-PTC, or spam). For PTCs, the agent starts the Promote process in IQMS, where the standard configuration creates an IQMS Complaint object from the intake Complaint data, triggering IQMS's standard complaint process. Complaints that, based on their classification, must be handled by another system are captured through the interface and delivered to the corresponding target system.**

****MVP scope.** The initial implementation delivers a simplified requirement set (MVP): a single intake email address is configured, which exclusively receives English-language emails with English-language attachments that do not require OCR. These are PTCs of the Usability Issue subtype. The MVP is intended to demonstrate the core functioning of the Veeva Complaint Intake Module and the automated n8n processing pipeline, as the foundation for the full rollout described above.

**

**IT Project Lead: 	    Sina Sander
Business Project Lead: 	Eva Westendorf
BEAT ID:                BEAT04090962**

---

***Complaint email*: In this use case, a complaint email is an inbound message arriving in a country-specific or grouped PTC/GBS email inbox that is the primary intake channel for product-related reports, alongside the Miidas–IQMS and ARGUS–IQMS interfaces. It consists of the email with its attachments — scans, photos, screenshots or electronically filled complaint forms from varying senders, frequently non-English and partly handwritten. It is an intake item, not yet a case: classification decides whether it is PTC-relevant at all (PTC, PTC+AE, UI, suspected falsification) or non-PTC (spam, advertisement, malware, product question, stability, reimbursement), and its content is attached or versioned on the ticket before any IQMS entry.**

***PTC*: Product Technical Complaint**

***AE*: Adverse Effect**

***UI*: Usability Issue**

***n8n*: AI Workflow Automation Platform - n8n**

***mGA*: myGenAssist is Bayer's secure internal generative AI platform that any client application can call through its REST API, sending a prompt in an authenticated HTTP request and getting back the LLM-generated completion as a structured JSON response.**

***SSF*: the legacy ticketing tool used for complaint email intake prior to Project CLARA, being replaced by the Veeva Complaint Intake Module.**

***IQMS*: the complaint management system that becomes the system of record once an intake Complaint is promoted to a full Complaint object, and in which the standard complaint process then runs.**

***Promote process*: the IQMS action, triggered by a Human Agent, that creates a standard IQMS Complaint object from the data held on an intake Complaint object.**

## Related material (outside this repo)

Bayer SharePoint folder: `AI Use Case PV-Complaint-Management - AI Use case`

- `BPMN process/System Landscape/` — Draw.io drafts
- `BPMN process/PTC-shadowing/` — original shadowing notes (copied into `docs/01-current-process/sources/`)
- `Complaint process automation/automation/` — earlier automation demo notes (Node-RED / Veeva)
