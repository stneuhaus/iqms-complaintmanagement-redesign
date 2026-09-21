# ADR-002: MVP slice — translation, categorization, extraction + HITL

- Status: proposed
- Date: 2026-09-18
- Deciders: TBD (product owner / process owner)

## Context

As-is intake is manual across ticket tool, translation hub, IQMS, Synaps, and Argus. The system-landscape draw.io “MVP-translation, category, extraction” describes a Zielprozess: AI translate → extract → classify → confidence → CM review → route to IQMS / ARGUS / archive. URS REQ-011…039 and FR-006…013 cover the same slice. Full reimbursement / DHL / pharmacy subprocesses are as-is pain but not required for the first automation cut ([FR-021](../02-requirements/functional-requirements.md), [A-001](../02-requirements/constraints-and-assumptions.md)).

## Decision

**Proposed:** First delivery slice is:

1. Translation (text + attachments)
2. Data extraction toward IQMS fields
3. Categorization / triage labels
4. Completeness / confidence exposure
5. Complaint Manager HITL before IQMS or ARGUS transfer

Out of first slice unless explicitly pulled in: Safetrack 2.0 go-live, DHL sample labels, reimbursement voucher flows, CQU authority mail beyond stubs.

## Consequences

- Architecture and design specs stay bounded to this slice until ADR is accepted or revised.
- FR-021 remains Could / later.
- Regulatory 5-day / AE transfer rules still need agreement ([A-006](../02-requirements/constraints-and-assumptions.md)).
