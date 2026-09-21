# ADR-001: Automation platform is n8n

- Status: proposed
- Date: 2026-09-18
- Deciders: TBD (product / technical project lead)

## Context

A 2026-05-13 demo showed Veeva automation with Node-RED (building blocks, Bayer Node-RED in AWS, Vault instances). This repository is set up for IQMS complaint-management redesign with **n8n** as the intended runtime ([C-002](../02-requirements/constraints-and-assumptions.md)). Building architecture or workflows on Node-RED without a recorded choice would fork the project.

## Decision

**Proposed:** Use **n8n** as the automation platform for this project’s workflows. Treat the Node-RED / Veeva demo as exploratory input only.

## Consequences

- Workflow JSON and design specs target n8n (`workflows/` later).
- Any reuse of Node-RED patterns must be re-expressed for n8n.
- Accept this ADR (or supersede with another platform) before design-spec / workflow implementation.
