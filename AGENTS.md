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
- **Translation prompt versioning** (`docs/05-design-spec/promtpts for text recogniztion/`): `prompt.de.md` is the German master and is edited in place. Every change to the English prompt creates a **new file** `prompt.en.<version>.md` — never edit an existing `prompt.en.*.md`. Released versions are immutable, because each one may already be in use by a workflow or a test run. Bump `$prompt_file_version` and add a changelog row in both the master and the new English file. See that folder's README.
- Keep related docs in the **same change**: source notes with as-is/systems; new terms in the glossary; new capabilities as `FR-`/`NFR-` IDs; product choices as ADRs; phase status in `docs/README.md`.
- At the end of a session, list which docs you changed and which related docs you deliberately did not change (and why).

### Prompting

- Allways create a new version by incrementing the first digit after the first point in the version identifier in the name (0.9 ->0.10) in case a new business feature will be implemented
- In case it is a kind of bug fix add direct after the version number "_bugfix" to the file name
- ALLWAYS add a description to the change history in the end of the prompt file
