# Architecture

Status: not started.

## Context

_Who uses the system, and which external systems it talks to._

```mermaid
flowchart LR
  users[Handlers_and_approvers]
  n8n[n8n_TBD]
  iqms[IQMS]
  ssf[SSF_ticket]
  other[Translation_Argus_Synaps_TBD]
  users --> n8n
  n8n --> iqms
  n8n --> ssf
  n8n --> other
```

## Containers

_TBD_

## Environments

_TBD_

## Open architecture questions

- Where n8n runs (Bayer-hosted vs other)
- How n8n authenticates to IQMS, SSF, mail, translation
- Human approval gates
