# iqms-complaintmanagement-redesign

Documentation-first project for the IQMS complaint-management redesign: document the as-is PTC / PV complaint process and later automate it with n8n.

We are collecting requirements and documenting the **as-is** business process. Architecture, functional specification, design specification, and n8n workflows come later.

## Working sequence

1. Document the current process (`docs/01-current-process/`)
2. Capture requirements (`docs/02-requirements/`)
3. Architecture (`docs/03-architecture/`)
4. Functional specification (`docs/04-functional-spec/`)
5. Design specification (`docs/05-design-spec/`)
6. Record decisions (`docs/06-decisions/`)
7. Implement n8n workflows (`workflows/`)

See [docs/README.md](docs/README.md) for what belongs in each folder. That file is the only status index (`Status` and `Last reviewed`).

## Contributing documentation

- Write Markdown in `docs/`.
- Keep as-is (today’s process) separate from to-be (automation).
- Add interview and meeting notes via the templates in `docs/templates/`.
- Put terms in [docs/02-requirements/glossary.md](docs/02-requirements/glossary.md) and reuse them.
- Do not commit secrets, credentials, or production data.

Before you commit, check:

- [ ] The matching row in [docs/README.md](docs/README.md) still matches folder status and last review date
- [ ] New terms are in the glossary and linked, not redefined
- [ ] Product or architecture choices have an ADR under `docs/06-decisions/`
- [ ] As-is and to-be are not mixed in the same file
- [ ] No PII, secrets, or production complaint data

Relative Markdown links can be checked with `python scripts/check-markdown-links.py` (also runs in CI). A Cursor `stop` hook reminds the agent to keep related docs in sync; it does not rewrite files.

## n8n (later)

Exported workflow JSON will live in `workflows/`. Environment and connection notes will live in `config/`. Do not add live credentials to the repository.
