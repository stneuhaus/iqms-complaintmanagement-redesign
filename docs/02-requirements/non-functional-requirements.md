# Non-functional requirements

Status: collecting. IDs are stable.

| ID | Category | Requirement | Source / notes |
| --- | --- | --- | --- |
| NFR-001 | Privacy | Personal and health-related data must be handled per Bayer policy; sensitive attachments go to IQMS confidential / personal sections, not general attachment areas | as-is; REQ-035…037 |
| NFR-002 | Security | No secrets or production payloads in git | project rule |
| NFR-003 | Security | Malware / viruses must be blocked from IQMS processing; flagged items go to Bayer Cyber Security Center | REQ-055 |
| NFR-004 | Audit | Automated and manual steps (including CM decisions and transfers) must be traceable for GxP / inspection needs | URS quality-check GAP-04; TBD acceptance criteria |
| NFR-005 | Reliability | Failures when IQMS, ticket tool, translation, Synaps, or Argus interfaces are unavailable must be detectable and recoverable without silent data loss | TBD design |
| NFR-006 | Volume | Solution must be sized for high-volume regions (order of ~16,000 cases/year US+Canada cited); confirm MVP country scope | Costa Rica notes |
| NFR-007 | Language | Translation must cover European languages plus Russian, Arabic, and official languages of African and Asian markets in scope; tolerate slang, typos, and grammar errors | REQ-014, REQ-015 |
| NFR-008 | Quality | Translation quality must be spot-checked vs current external service during hypercare (first three months); target is to remove routine country quality language review once criteria are met | REQ-013, REQ-018 |
| NFR-009 | Timeliness | PTC intake due date of 5 days (and seriousness-based triage SLAs per SOP / REQ-030) must be visible and enforceable in the process | REQ-030, REQ-051; Zielprozess “5 days past?” |
| NFR-010 | Contact rules | Missing-information contact attempts: minimum timing (e.g. ≥48 h between attempts, at least one within 5 days); rules stop when a reply arrives | REQ-052, REQ-053 |
| NFR-011 | Confidence | AI outputs for category / extraction / completeness must expose confidence so CM can apply review thresholds (Zielprozess bands ≥95% / 80–95% / ≤80% are a design hypothesis until agreed) | Zielprozess |
| NFR-012 | Compatibility | Existing GBS / PTC email addresses and partner-facing channels must keep working without forced change management for senders | REQ-010 |
| NFR-013 | Access | Role-based access for Complaint Managers, QA reviewers, and administrators (gap noted in URS quality check) | URS GAP-07; TBD |
| NFR-014 | Cost | AI processing cost per document must be reportable so running costs can be projected against volume before rollout | translation prompt 0.8; relates to NFR-006 volume |
