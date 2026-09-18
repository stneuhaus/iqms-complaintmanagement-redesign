# Agent instructions

This repository is **iqms-complaintmanagement-redesign**, a documentation-first project for the IQMS complaint-management redesign and later n8n automation. Implementation comes after the as-is process and requirements are agreed.

## Where to put work

| Kind of change | Location |
| --- | --- |
| Project purpose and scope | `docs/00-overview/` |
| As-is process, systems, interview sources | `docs/01-current-process/` |
| Stakeholders, FRs, NFRs, constraints, glossary | `docs/02-requirements/` |
| Architecture diagrams and C4-style notes | `docs/03-architecture/` |
| Functional specification | `docs/04-functional-spec/` |
| Design specification (how it will be built) | `docs/05-design-spec/` |
| Architecture / product decisions (ADRs) | `docs/06-decisions/` |
| Interview / meeting templates | `docs/templates/` |
| Exported n8n workflows | `workflows/` |
| Env examples and connection notes | `config/` |

## Rules

- Do not invent to-be architecture or n8n workflows until requirements in `docs/02-requirements/` are agreed.
- Do not mix as-is and to-be in the same file. As-is stays in `docs/01-current-process/`.
- Prefer Markdown. Use mermaid for process and architecture diagrams.
- Link glossary terms instead of redefining them in every file.
- Never commit secrets, credentials, PHI/PII dumps, or production complaint data.
- Source Draw.io files remain in the Bayer SharePoint folder; link them, do not copy binaries unless explicitly asked.
- New process interviews go in `docs/01-current-process/sources/` using `docs/templates/process-interview.md`.
